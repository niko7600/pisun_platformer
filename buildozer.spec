[app]
title = Pixel Pisun
package.name = pisunplatformer
package.domain = org.pisun

source.dir = .
source.include_exts = py

version = 1.1

# pygame 2.1 из python-for-android (SDL2). Больше ничего не нужно:
# звуки игра синтезирует сама, картинок и шрифтов-файлов нет.
requirements = python3,pygame

orientation = landscape
fullscreen = 1

# Старый, проверенный набор инструментов: свежий python-for-android собирает Python 3.14,
# а pygame 2.1 с ним несовместим (ошибка 'longintrepr.h' file not found).
# Эта ветка собирает Python 3.10.10, с которым pygame 2.1.0 компилируется.
p4a.branch = v2023.09.16
android.ndk = 25b
android.ndk_api = 21

android.api = 33
android.minapi = 21
android.archs = arm64-v8a, armeabi-v7a
android.accept_sdk_license = True
android.allow_backup = False

[buildozer]
log_level = 2
warn_on_root = 1
