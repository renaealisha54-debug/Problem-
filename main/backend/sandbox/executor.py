import subprocess
import os
import uuid
import resource

SAFE_TIMEOUT = 10
MAX_OUTPUT_BYTES = 65536  # 64KB

def run_code_safely(code: str, language: str) -> dict:
    file_ext = "py" if language == "python" else "js"
    temp_file = f"/tmp/sandbox_{uuid.uuid4()}.{file_ext}"

    with open(temp_file, "w") as f:
        f.write(code)

    try:
        if language == "python":
            cmd = ["python3", "-E", "-S", temp_file]
        else:
            cmd = ["node", "--max-old-space-size=64", temp_file]

        process = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=SAFE_TIMEOUT,
            preexec_fn=_set_resource_limits
        )

        stdout = process.stdout[:MAX_OUTPUT_BYTES]
        stderr = process.stderr[:MAX_OUTPUT_BYTES]
        return {"result": stdout if stdout else stderr, "exit_code": process.returncode}

    except subprocess.TimeoutExpired:
        return {"error": "Execution timed out (10s limit)."}
    except Exception as e:
        return {"error": str(e)}
    finally:
        if os.path.exists(temp_file):
            os.remove(temp_file)

def _set_resource_limits():
    # Max 64MB memory
    resource.setrlimit(resource.RLIMIT_AS, (67108864, 67108864))
    # Max 5 seconds CPU time
    resource.setrlimit(resource.RLIMIT_CPU, (5, 5))
    # Max 10 file writes
    resource.setrlimit(resource.RLIMIT_NOFILE, (10, 10))
