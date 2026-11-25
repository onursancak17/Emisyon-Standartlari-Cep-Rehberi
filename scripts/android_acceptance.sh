#!/usr/bin/env bash
set -euo pipefail
out="$GITHUB_WORKSPACE/build-output/android-acceptance"
mkdir -p "$out"
adb shell svc wifi disable
adb shell svc data disable
adb shell settings get global wifi_on | tee "$out/wifi-state.txt"
test "$(adb shell settings get global wifi_on | tr -d '\r')" = 0
adb shell settings get global mobile_data | tee "$out/mobile-data-state.txt"
package=com.onursancak.emisyon_standartlari_cep_rehberi
adb install -r /tmp/mobile_build/build/app/outputs/flutter-apk/app-release.apk
adb logcat -c
adb shell monkey -p "$package" -c android.intent.category.LAUNCHER 1
sleep 4
adb shell pidof "$package" > "$out/release-pid.txt"
test -s "$out/release-pid.txt"
adb exec-out screencap -p > "$out/release-offline-home.png"
adb logcat -d > "$out/release-logcat.txt"
if grep -A 12 'FATAL EXCEPTION' "$out/release-logcat.txt" | grep -q "$package"; then
  echo 'Release process crashed'; exit 1
fi
cd /tmp/mobile_build
# Release ve debug anahtarları ayrı olabilir; ilk kurulum kanıtı yukarıda korunur.
adb uninstall "$package"
flutter test --help --verbose > "$out/flutter-test-help.txt"
dds_args=()
if grep -q -- '--disable-dds' "$out/flutter-test-help.txt"; then dds_args+=(--disable-dds); fi
if grep -q -- '--\[no-\]dds' "$out/flutter-test-help.txt"; then dds_args+=(--no-dds); fi
trap 'adb logcat -d > "$out/integration-logcat.txt" || true' EXIT
flutter test integration_test/offline_app_test.dart -d emulator-5554 --timeout 8m --reporter expanded --verbose "${dds_args[@]}" 2>&1 | tee "$out/integration-test.txt"
adb exec-out screencap -p > "$out/quiz-offline-result.png"
adb shell settings put system font_scale 2.0
adb shell settings put system accelerometer_rotation 0
adb shell settings put system user_rotation 1
adb shell am force-stop "$package"
adb shell monkey -p "$package" -c android.intent.category.LAUNCHER 1
sleep 3
adb exec-out screencap -p > "$out/landscape-font-200.png"
adb shell pidof "$package" > "$out/landscape-pid.txt"
