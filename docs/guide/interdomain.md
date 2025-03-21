# Javascript–Python bridge

_pywebview_ offers two-way communication between Javascript and Python, enabling interaction between the two languages without a HTTP server.

## Run Javascript from Python

`window.evaluate_js(code, callback=None)` allows you to execute arbitrary Javascript code with a last value returned synchronously. If callback function is supplied, then promises are resolved and the callback function is called with the result as a parameter. Javascript types are converted to Python types, eg. JS objects to dicts, arrays to lists, undefined to None. If executed Javascript code results in an error, the error is rethrown as a `webview.util.JavascriptException` in Python. `evaluate_js` wraps Javascript code in a helper wrapper and executes it using `eval`.

[See example](/examples/evaluate_js.html)

`window.run_js(code)` executes Javascript code as is without any wrapper code. `run_js` does not return a result or handle exceptions. This can be useful in scenarios, where you need to execute Javascript code with the `unsafe-eval` CSP policy set.

## Run Python from Javascript

Executing Python functions from Javascript can be done with two different mechanisms.

- by exposing an instance of a Python class to the `js_api` parameter of `create_window`. All the callable methods of the class will be exposed to the JS domain as `pywebview.api.method_name` with correct parameter signatures. Method name must not start with an underscore. Nested classes are allowed and are converted into a nested objects in Javascript. Class attributes starting with an underscore are not exposed. See an [example](/examples/js_api.html).

- by passing your function(s) to window object's `expose(func)`. This will expose a function or functions to the JS domain as `pywebview.api.func_name`. Unlike JS API, `expose` allows to expose functions also at the runtime. If there is a name clash between JS API and exposed functions, the latter takes precedence. See an [example](/examples/expose.html).

Exposed function returns a promise that is resolved to its result value. Exceptions are rejected and encapsulated inside a Javascript `Error` object. Stacktrace is available via `error.stack`. Exposed functions are executed in separate threads and are not thread-safe.

`window.pywebview.api` is not guaranteed to be available on the `window.onload` event. Subscribe to the `window.pywebviewready` event instead to make sure that `window.pywebview.api` is ready.

[See example](/examples/js_api.html).
