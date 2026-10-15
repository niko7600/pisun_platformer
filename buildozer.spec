[app]
title = Pixel Pisun
package.name = pisunplatformer
package.domain = org.pisun

source.dir = .
source.include_exts = py

version = 1.0

# pygame 2.1 из python-for-android (SDL2). Больше ничего не нужно:
# звуки игра синтезирует сама, картинок и шрифтов-файлов нет.
requirements = python3,pygame

orientation = landscape
fullscreen = 1

android.api = 33
android.minapi = 21
android.archs = arm64-v8a, armeabi-v7a
android.accept_sdk_license = True
android.allow_backup = False

[buildozer]
log_level = 2
warn_on_root = 1
