import sys
import threading

import pytest
import webview

from .util import run_test


def clipboard_test_app():
    return """
    <html>
      <body>
        <script>
          // Generate a random string and write it to the clipboard asynchronously.
          function asyncCopy() {
            const txt = Math.random().toString(36).substring(2);
            return new Promise((resolve) => {
              setTimeout(() => {
                navigator.clipboard.writeText(txt)
                  .then(() => resolve({ success: true, error: null }))
                  .catch((err) => resolve({ success: false, error: err.message }));
              }, 1000);
            });
          }
        </script>
      </body>
    </html>
    """


def async_clipboard_test(window):
    window.load_html(clipboard_test_app())
    result_container = {}
    event = threading.Event()

    def callback(val: dict):
        result_container["result"] = val
        event.set()

    window.evaluate_js("(async () => await asyncCopy())()", callback)

    # Wait up to 5 seconds for the JS callback to complete.
    event.wait(timeout=5)
    result = result_container.get("result")
    assert result and result.get("success"), (
        f"Clipboard copy failed: {result.get('error') if result else 'no result'}"
    )


@pytest.mark.skipif(sys.platform != "darwin", reason="Test only applicable on macOS")
def test_clipboard():
    webview.settings["ALLOW_CLIPBOARD_ACCESS"] = True
    window = webview.create_window("Clipboard Test",
                                   html="",  # need to load html after because clipboard only available on secure origin
                                   width=800, height=600)
    run_test(webview, window, async_clipboard_test)
