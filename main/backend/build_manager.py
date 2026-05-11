import shutil
import subprocess
import os
import uuid
from fastapi import APIRouter
from models.schemas import BuildRequest

router = APIRouter()

TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), "templates", "android_base")


def _inject_manifest(build_path: str, app_name: str, package_name: str):
    manifest_path = os.path.join(
        build_path, "app", "src", "main", "AndroidManifest.xml"
    )
    with open(manifest_path, "r") as f:
        content = f.read()
    content = content.replace("com.problemcode.app", package_name)
    content = content.replace("ProblemCode App", app_name)
    with open(manifest_path, "w") as f:
        f.write(content)


def _inject_package(build_path: str, package_name: str):
    gradle_path = os.path.join(build_path, "app", "build.gradle")
    with open(gradle_path, "r") as f:
        content = f.read()
    content = content.replace(
        'applicationId "com.problemcode.app"',
        f'applicationId "{package_name}"'
    )
    with open(gradle_path, "w") as f:
        f.write(content)

    java_src = os.path.join(
        build_path, "app", "src", "main", "java", "com", "problemcode", "app", "MainActivity.java"
    )
    if os.path.exists(java_src):
        with open(java_src, "r") as f:
            java = f.read()
        java = java.replace("package com.problemcode.app;", f"package {package_name};")
        with open(java_src, "w") as f:
            f.write(java)
        parts = package_name.split(".")
        dest_dir = os.path.join(build_path, "app", "src", "main", "java", *parts)
        os.makedirs(dest_dir, exist_ok=True)
        dest_file = os.path.join(dest_dir, "MainActivity.java")
        if dest_dir != os.path.dirname(java_src):
            shutil.move(java_src, dest_file)


@router.post("/api/build/apk")
async def build_apk(request: BuildRequest):
    project_id = f"build_{uuid.uuid4().hex[:8]}"
    build_path = os.path.join("builds", project_id)

    if not os.path.isdir(TEMPLATE_DIR):
        return {"error": f"Android template not found at: {TEMPLATE_DIR}"}

    shutil.copytree(TEMPLATE_DIR, build_path)

    assets_path = os.path.join(build_path, "app", "src", "main", "assets", "www")
    os.makedirs(assets_path, exist_ok=True)
    with open(os.path.join(assets_path, "index.js"), "w") as f:
        f.write(request.code)

    _inject_manifest(build_path, request.app_name, request.package_name)
    _inject_package(build_path, request.package_name)

    gradlew = os.path.join(build_path, "gradlew")
    if os.path.exists(gradlew):
        os.chmod(gradlew, 0o755)

    try:
        result = subprocess.run(
            ["./gradlew", "assembleDebug", "--no-daemon"],
            cwd=build_path,
            capture_output=True,
            timeout=300,
            env={**os.environ, "ANDROID_HOME": os.environ.get("ANDROID_HOME", os.path.expanduser("~/Android/Sdk"))}
        )

        apk_src = os.path.join(
            build_path, "app", "build", "outputs", "apk", "debug", "app-debug.apk"
        )

        if result.returncode == 0 and os.path.exists(apk_src):
            os.makedirs("downloads", exist_ok=True)
            apk_dest = os.path.join("downloads", f"{project_id}.apk")
            shutil.copy2(apk_src, apk_dest)
            return {"download_url": f"/downloads/{project_id}.apk"}
        else:
            return {
                "error": "Build failed",
                "log": result.stderr.decode(errors="replace") or result.stdout.decode(errors="replace")
            }

    except subprocess.TimeoutExpired:
        return {"error": "Build timed out (5 min limit)."}
    except Exception as e:
        return {"error": str(e)}
