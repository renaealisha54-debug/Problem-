import subprocess
import os
import uuid
import sys

SAFE_TIMEOUT = 10
MAX_OUTPUT_BYTES = 65536


def _set_resource_limits():
    try:
        import resource
        resource.setrlimit(resource.RLIMIT_AS, (67108864, 67108864))
        resource.setrlimit(resource.RLIMIT_CPU, (5, 5))
        resource.setrlimit(resource.RLIMIT_NOFILE, (16, 16))
    except Exception:
        pass


def run_code_safely(code: str, language: str) -> dict:
    file_ext = "py" if language == "python" else "js"
    temp_file = f"/tmp/sandbox_{uuid.uuid4().hex}.{file_ext}"

    with open(temp_file, "w") as f:
        f.write(code)

    try:
        if language == "python":
            cmd = ["python3", "-E", "-S", temp_file]
        else:
            cmd = ["node", "--max-old-space-size=64", temp_file]

        preexec = _set_resource_limits if sys.platform != "win32" else None

        process = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=SAFE_TIMEOUT,
            preexec_fn=preexec,
        )

        stdout = process.stdout[:MAX_OUTPUT_BYTES]
        stderr = process.stderr[:MAX_OUTPUT_BYTES]
        output = stdout if stdout else stderr
        return {
            "result": output if output else "(no output)",
            "exit_code": process.returncode,
            # Always surface stderr separately if it exists
            "error": stderr if stderr else None,
        }

    except subprocess.TimeoutExpired:
        return {"error": "Execution timed out (10s limit)."}
    except FileNotFoundError as e:
        return {"error": f"Runtime not found: {e}. Make sure python3/node is installed."}
    except Exception as e:
        return {"error": str(e)}
    finally:
        if os.path.exists(temp_file):
            os.remove(temp_file)
