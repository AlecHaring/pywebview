from time import sleep
import pytest
import webview

from .util import run_test


def test_xy():
    window = webview.create_window('xy test', x=200, y=200, width=100, height=100)
    run_test(webview, window, xy)


@pytest.mark.skip
def test_move_window():
    window = webview.create_window('Move window test', x=200, y=200, width=100, height=100)
    run_test(webview, window, move_window)


def xy(window):
    assert window.x == 200
    assert window.y == 200


def move_window(window):
    window.move(300, 300)
    sleep(1)

    assert window.x == 300
    assert window.y == 300
