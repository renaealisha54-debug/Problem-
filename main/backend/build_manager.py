import shutil
import subprocess
import os
import uuid
from fastapi import APIRouter

router = APIRouter()

@router.post("/api/build/apk")
async def build_apk(code: str):
    project_id = f"build_{uuid.uuid4()}"
    build_path = f"./builds/{project_id}"

    # 1. Scaffolding
    shutil.copytree("./templates/android_base", build_path)

    # 2. Injection
    assets_path = f"{build_path}/app/src/main/assets/www"
    os.makedirs(assets_path, exist_ok=True)
    with open(f"{assets_path}/index.js", "w") as f:
        f.write(code)

    # 3. Compilation
    try:
        result = subprocess.run(
            ["./gradlew", "assembleRelease"],
            cwd=build_path,
            capture_output=True,
            timeout=300
        )
        if result.returncode == 0:
            return {"download_url": f"/downloads/{project_id}/app-release.apk"}
        else:
            return {"error": "Build failed", "log": result.stderr.decode()}
    except Exception as e:
        return {"error": str(e)}
