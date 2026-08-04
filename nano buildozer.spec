[app]
title = لعبة النجمة
package.name = gamestealer
package.domain = org.test
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0.0
requirements = python3,kivy,requests,android
orientation = portrait
osx.python_version = 3
osx.kivy_version = 2.1.0
fullscreen = 0
android.permissions = INTERNET,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE
android.api = 30
android.minapi = 21
android.gradle_dependencies =
android.entitlements =
android.add_src =
android.manifest.extra =
android.bootstrap = sdl2

[buildozer]
log_level = 2
warn_on_root = 1
