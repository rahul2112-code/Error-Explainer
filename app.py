import os
import subprocess
from flask import Flask, request, jsonify, render_template
from pathlib import Path

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/compile', methods=['POST'])
def compile_code():
    data = request.json
    if not data or 'code' not in data:
        return jsonify({"output": "No code provided", "error": True}), 400

    code     = data['code']
    language = data.get('language', 'c')

    if language == 'java':
        TEMP_SOURCE    = "Main.java"
        # javac produces Main.class — we'll delete it with a glob after running
        compiler_script = [
            'python',
            os.path.join(os.path.dirname(__file__), 'java_compiler', 'friendlyJavaCompiler.py'),
            TEMP_SOURCE
        ]
    else:
        TEMP_SOURCE    = "user_code.c"
        TEMP_EXEC      = "user_prog.exe" if os.name == 'nt' else "user_prog"
        compiler_script = [
            'python',
            os.path.join(os.path.dirname(__file__), 'friendlyCompiler.py'),
            TEMP_SOURCE, '-o', TEMP_EXEC
        ]

    # Write code to temp file
    try:
        with open(TEMP_SOURCE, 'w', encoding='utf-8') as f:
            f.write(code)
    except Exception as e:
        return jsonify({"output": f"Error writing source file: {e}", "error": True}), 500

    # Run the friendly compiler
    try:
        result = subprocess.run(
            compiler_script,
            capture_output=True,
            text=True,
            timeout=20
        )
        output_text = result.stdout
        if result.stderr:
            output_text += "\n" + result.stderr
        success = (result.returncode == 0)

    except subprocess.TimeoutExpired:
        output_text = "Error: Compilation and explanation timed out."
        success = False
    except Exception as e:
        output_text = f"An unexpected error occurred: {e}"
        success = False

    finally:
        # Cleanup source file
        try:
            if os.path.exists(TEMP_SOURCE):
                os.remove(TEMP_SOURCE)
        except Exception:
            pass

        # Cleanup compiled artefacts
        if language == 'java':
            # Remove any .class files generated in the working directory
            for class_file in Path('.').glob('*.class'):
                try:
                    class_file.unlink()
                except Exception:
                    pass
        else:
            try:
                if os.path.exists(TEMP_EXEC):
                    os.remove(TEMP_EXEC)
            except Exception:
                pass

    return jsonify({"output": output_text.strip(), "success": success})


if __name__ == '__main__':
    app.run(debug=True, port=5000)
