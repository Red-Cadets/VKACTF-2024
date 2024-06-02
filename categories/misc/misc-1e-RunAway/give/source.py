import ast
import pandas as pd
from flask import Flask, render_template, request
import sys
from io import StringIO
import numpy as np

app = Flask(__name__)

DISALLOWED_MODULES = {
    "subprocess",
    "os",
    "exec",
    "sys",
    "eval",
    "pty",
    "pathlib",
    "open",
    "importlib",
    "io",
    "builtins",
}


def execute_safe_code(code):
    stdout = StringIO()
    sys.stdout = stdout

    __import__ = __builtins__.__import__

    safe_globals = {
        "__builtins__": {
            "__import__": lambda *args, **kwargs: restricted_import(*args, **kwargs)
        },
        "print": lambda *args, **kwargs: sys.stdout.write(
            " ".join(map(str, args)) + "\n"
        ),
    }

    def restricted_import(name, *args, **kwargs):
        if name.split(".")[0] in DISALLOWED_MODULES:
            raise ImportError(f"Import of module '{name}' is not allowed.")
        return __import__(name, *args, **kwargs)

    try:
        tree = ast.parse(code)
        for node in ast.walk(tree):
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                for alias in node.names:
                    if alias.name.split(".")[0] in DISALLOWED_MODULES:
                        raise ValueError(
                            f"Import of module '{alias.name}' is not allowed."
                        )
            elif isinstance(node, ast.Call):
                if (
                    isinstance(node.func, ast.Name)
                    and node.func.id in DISALLOWED_MODULES
                ):
                    raise ValueError(
                        f"Call of function '{node.func.id}' is not allowed."
                    )

        compiled_code = compile(code, "<string>", "exec")
        exec(compiled_code, safe_globals)

        return stdout.getvalue()
    except Exception as e:
        return str(e)
    finally:
        sys.stdout = sys.__stdout__


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/execute", methods=["POST"])
def execute():
    code = request.form["code"]
    result = execute_safe_code(code)
    return result


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10041)
