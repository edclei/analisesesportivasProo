
Mobile wrapper (Capacitor) for Analises Esportivas Pro
----------------------------------------------------

This folder contains helper scripts to produce an Android APK from the frontend web build using Capacitor.
It does NOT include Android SDK or build artifacts. You must run this on a machine with Android Studio / Android SDK installed
or in a CI runner that provides Android build environment (example GitHub Actions workflow provided in .github/workflows/android.yml).

Quick local steps (macOS / Linux):
1. Install Node.js (16+), Java JDK 11, Android SDK, Android Studio.
2. From repo root: npm install (or yarn) then:
   cd mobile
   npm install
   npm run build:web
   npm run cap:init   # only first time
   npm run cap:add:android
   npm run cap:sync
   npm run build:apk

CI (GitHub Actions) will run similar steps automatically.

Note: You may need to adjust package names, signing config, and keystore to produce a signed release APK.
