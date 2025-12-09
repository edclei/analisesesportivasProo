
Analises Esportivas Pro - FINAL BUILD (AGGRESSIVE MODE)
======================================================

This archive is the merged project including the original full project and the Aggressive AI updates.
Location: AnalisesEsportivasPro_FINAL_BUILD

What was merged:
- Original project files (frontend, backend, assets)
- Aggressive-mode AI files (core/config_aggressive.json, core/markets.py, core/strategy.py)
- Procfile and start.sh adjusted to use ${PORT:-8000}
- Mobile wrapper (mobile/) with Capacitor helper scripts
- GitHub Actions workflow at .github/workflows/android_build.yml to produce an APK in CI

HOW TO BUILD APK (locally)
1. Ensure Android SDK, Java 11 and Node.js are installed.
2. From repo root:
   - npm install
   - cd mobile
   - npm install
   - npm run build:web
   - npm run cap:init   # first-time only
   - npm run cap:add:android
   - npm run cap:sync
   - npm run build:apk
3. Configure Android signing (keystore) in mobile/android/app/build.gradle to sign release builds.

HOW TO BUILD APK (GitHub Actions)
- Push to main branch; or run the workflow manually from Actions tab.
- The workflow builds the frontend, prepares Capacitor, builds APK and uploads it as artifact.
- Download artifact from workflow run artifacts.

NOTES:
- The environment where you run the APK build must have Android SDK installed (CI runner or local machine).
- For production release on Play Store, sign the APK and follow Play Store requirements.

