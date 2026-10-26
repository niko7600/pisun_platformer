[app]
title = Пиксельный Писюн
package.name = pisunplatformer
package.domain = org.pisun

source.dir = .
source.include_exts = py,png
source.exclude_dirs = tools,.github,.buildozer,bin,__pycache__
source.exclude_patterns = tools/*

version = 1.1-netplay

requirements = python3,pygame

# Иконка приложения (512x512) и адаптивная иконка Android 8+ (432x432, слои)
icon.filename = %(source.dir)s/icon.png
icon.adaptive_foreground.filename = %(source.dir)s/icon_fg.png
icon.adaptive_background.filename = %(source.dir)s/icon_bg.png

orientation = landscape
fullscreen = 1

android.permissions = INTERNET,ACCESS_WIFI_STATE,ACCESS_NETWORK_STATE,CHANGE_WIFI_MULTICAST_STATE
android.api = 33
android.ndk = 25b
android.ndk_api = 21
p4a.branch = v2024.01.21
android.minapi = 21
android.archs = arm64-v8a, armeabi-v7a
android.accept_sdk_license = True
android.allow_backup = True

[buildozer]
log_level = 2
warn_on_root = 1
