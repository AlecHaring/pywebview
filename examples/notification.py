import webview


if __name__ == '__main__':
    class Api:
        def trigger(self):
            window.create_notification('pywebview', 'Example Title', 'Some details here')

    window = webview.create_window(
        'Notification example',
        html='''
        <!DOCTYPE html>
        <html>
            <head>
                <style>
                    body {
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        height: 100vh;
                        margin: 0;
                        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
                    }
                    button {
                        padding: 10px 20px;
                        font-size: 16px;
                        cursor: pointer;
                    }
                </style>
            </head>
            <body>
                <button onclick="pywebview.api.trigger()">Trigger Notification</button>
            </body>
        </html>
        ''',
    js_api=Api())

    webview.start()
