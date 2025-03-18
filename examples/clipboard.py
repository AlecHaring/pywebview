import webview

def clipboard_test_app():
    return """
    <!DOCTYPE html>
    <html>
    <head>
      <title>Clipboard Test</title>
    </head>
    <body>
      <h1>Clipboard Copy Test</h1>

      <div>
        <button onclick="generateAndCopy()">Generate &amp; Copy New Text</button>
        <span id="copyResult"></span>
      </div>
      <div>
        <button onclick="asyncCopy()">Generate &amp; Copy After Async Operation</button>
        <span id="asyncResult"></span>
      </div>
      <h2>Generated Text:</h2>
      <div id="generatedText"></div>

      <h2>Verification:</h2>
      <p>Paste below to verify what was copied:</p>
      <textarea id="pasteArea" placeholder="Ctrl+V or Command+V to paste here"></textarea>

      <script>
        function generateRandomText() {
          const words = ['apple', 'banana', 'computer', 'data', 'elephant', 'function',
                         'guitar', 'house', 'internet', 'javascript', 'keyboard', 'laptop',
                         'mouse', 'network', 'orange', 'python', 'quality', 'router',
                         'system', 'tablet', 'umbrella', 'virtual', 'website', 'xylophone',
                         'yellow', 'zebra'];
          const length = 5 + Math.floor(Math.random() * 10);
          let result = [];
          for (let i = 0; i < length; i++) {
            result.push(words[Math.floor(Math.random() * words.length)]);
          }
          return result.join(' ');
        }

        function updateResult(id, success, message) {
          document.getElementById(id).textContent = message;
        }

        function randomizeText() {
          const text = generateRandomText();
          document.getElementById('generatedText').textContent = text;
          return text;
        }

        function generateAndCopy() {
          const text = randomizeText();
          navigator.clipboard.writeText(text)
            .then(() => updateResult('copyResult', true, '✓ Copied successfully'))
            .catch(err => updateResult('copyResult', false, `✗ Error: ${err.message}`));
        }

        document.getElementById('pasteArea').addEventListener('paste', function() {
          setTimeout(() => {
            this.style.backgroundColor = '#ffffcc';
            setTimeout(() => this.style.backgroundColor = '', 500);
          }, 0);
        });

        function asyncCopy() {
          const text = randomizeText();
          updateResult('asyncResult', false, '⟳ Simulating API call...');
          fetch('https://httpbin.org/delay/1')
            .then(() => navigator.clipboard.writeText(text))
            .then(() => updateResult('asyncResult', true, '✓ Copied after async operation'))
            .catch(err => updateResult('asyncResult', false, `✗ Error: ${err.message}`));
        }
      </script>
    </body>
    </html>
    """

if __name__ == '__main__':
    webview.settings['ALLOW_CLIPBOARD_ACCESS'] = True
    window = webview.create_window('Clipboard Testing App', html=clipboard_test_app(), width=900, height=700)
    webview.start(lambda: window.load_html(clipboard_test_app()), debug=True)
