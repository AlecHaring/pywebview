import logging
import os
import sys
import threading
import time
import traceback
from multiprocessing import Queue
from typing import Any, Callable, Dict, Iterable, Optional
from uuid import uuid4

import pytest

logger = logging.getLogger('pywebview')


def run_test(
    webview: Any,
    window: Any,
    thread_func: Optional[Callable] = None,
    param: Iterable = (),
    start_args: Dict[str, Any] = {},
    no_destroy: bool = False,
    destroy_delay: float = 0,
    debug: bool = False
) -> None:
    """"
    A test running function that creates a window and runs a thread function in it. Test logic is to be placed in the
    thread function. The function will wait for the thread function to finish and then destroy the window. If the thread
    function raises an exception, the test will fail and the exception will be printed.

    :param webview: webview module
    :param window: window instance created with webview.create_window
    :param thread_func: function to run in the window.
    :param param: positional arguments to pass to the thread function
    :param start_args: keyword arguments to pass to webview.start
    :param no_destroy: flag indicating whether to destroy the window after the thread function finishes (default: False).
    If set to True, the window will not be destroyed and the test will not finish until the window is closed manually.
    :param destroy_delay: delay in seconds before destroying the window (default: 0)
    :param debug: flag indicating whether to enable debug mode (default: False)

    """
    __tracebackhide__ = True
    try:
        queue: Queue = Queue()

        if debug:
            start_args = {**start_args, 'debug': True}

        time.sleep(2)
        _create_window(
            webview, window, thread_func, queue, param, start_args, no_destroy, destroy_delay
        )

        if not queue.empty():
            e = queue.get()
            pytest.fail(e)

    except Exception as e:
        pytest.fail(e)


def assert_js(window, func_name, expected_result, *func_args):
    value_id = 'v' + uuid4().hex[:8]
    func_args = str(func_args).replace(',)', ')')

    execute_func = """
    window.pywebview.api.{0}{1}.then(function(value) {{
        window.{2} = value
    }}).catch(function() {{
        window.{2} = 'error'
    }})
    """.format(
        func_name, func_args, value_id
    )
    check_func = 'window.{0}'.format(value_id)

    window.evaluate_js(execute_func)

    result = window.evaluate_js(check_func)
    counter, MAX = 0, 50

    while result is None:
        if counter == MAX:
            raise AssertionError('assert_js timeout')
        else:
            counter += 1
            time.sleep(0.1)
            result = window.evaluate_js(check_func)

    assert expected_result == result


def _create_window(
    webview, window, thread_func, queue, thread_param, start_args, no_destroy, destroy_delay
):
    def thread():
        try:
            take_screenshot()
            move_mouse_cocoa()
            if thread_func:
                thread_func(window, *thread_param)

            destroy_event.set()
        except Exception as e:
            logger.exception(e, exc_info=True)
            queue.put(traceback.format_exc())
            destroy_event.set()

    if not no_destroy:
        args = (thread_param,) if thread_param else ()
        destroy_event = _destroy_window(webview, window, destroy_delay)

        t = threading.Thread(target=thread)
        t.start()

    webview.start(**start_args)


def get_test_name():
    return os.environ.get('PYTEST_CURRENT_TEST').split(':')[-1].split(' ')[0]


def move_mouse_cocoa():
    if sys.platform == 'darwin':
        from .util_cocoa import mouseMoveRelative

        time.sleep(1)
        mouseMoveRelative(1, 1)


def take_screenshot():
    if sys.platform == 'darwin':
        from subprocess import Popen
        from datetime import datetime

        Popen(['screencapture', '-x', f'/tmp/screenshot-{datetime.now().timestamp()}.png']).wait()

def _destroy_window(_, window, delay):
    def stop():
        event.wait()
        time.sleep(delay)
        window.destroy()

        move_mouse_cocoa()

    event = threading.Event()
    event.clear()
    t = threading.Thread(target=stop)
    t.start()

    return event
