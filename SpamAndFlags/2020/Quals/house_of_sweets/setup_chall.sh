#!/bin/bash
set -euxo pipefail
#~/tools/android/android-ndk-r19c-linux-x86_64/android-ndk-r19c/toolchains/llvm/prebuilt/linux-x86_64/bin/clang -target aarch64-linux-android21 -fstack-protector -z relro -z now -o house_of_sweets house_of_sweets.c
#~/tools/android/android-ndk-r19c-linux-x86_64/android-ndk-r19c/toolchains/llvm/prebuilt/linux-x86_64/bin/clang -target aarch64-linux-android21 -fstack-protector -z relro -z now -o test test.c
cd /
adb push house_of_sweets /data/local/tmp/.
adb push flag /data/local/tmp/.
adb shell "chmod +x /data/local/tmp/house_of_sweets"
adb shell "sync"
#adb shell "su -c '/data/local/tmp/house_of_sweets'"
