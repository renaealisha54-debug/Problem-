#!/bin/bash
set -e

export ANDROID_SDK_ROOT=${ANDROID_HOME:-$HOME/Android/Sdk}

echo "Installing required SDK components..."
yes | $ANDROID_SDK_ROOT/cmdline-tools/latest/bin/sdkmanager --licenses
$ANDROID_SDK_ROOT/cmdline-tools/latest/bin/sdkmanager \
    "platforms;android-34" \
    "build-tools;34.0.0" \
    "platform-tools"

echo "Making gradlew executable..."
find . -name "gradlew" -exec chmod +x {} \;

echo "All SDK components installed successfully."
