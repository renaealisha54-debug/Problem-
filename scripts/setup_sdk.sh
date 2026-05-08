#!/bin/bash

# Ensure the script stops on errors
set -e

echo "Accepting Android SDK Licenses..."

# Replace the path below with your actual Android SDK location
export ANDROID_SDK_ROOT=$HOME/Android/Sdk

# 2. SDK Licenses Acceptance Logic
# This pipes 'y' into the sdkmanager to accept all terms automatically
yes | $ANDROID_SDK_ROOT/cmdline-tools/latest/bin/sdkmanager --licenses

echo "✅ All licenses accepted successfully."
