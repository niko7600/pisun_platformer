"""Локальный рецепт pygame для python-for-android.

pygame 2.1.0 в архиве содержит заранее сгенерированные .c-файлы (Cython 0.29.24),
которые включают "longintrepr.h" — на Python 3.11 такого заголовка в корне больше нет
(он переехал в cpython/), и сборка падает. Здесь мы перед сборкой заново генерируем
эти .c из .pyx свежим Cython 0.29.x (он ставится в workflow: cython<3).
"""
import glob
import os
import subprocess
import sys

from pythonforandroid.recipes.pygame import Pygame2Recipe
from pythonforandroid.logger import info


class PygameFixedRecipe(Pygame2Recipe):

    def prebuild_arch(self, arch):
        super().prebuild_arch(arch)
        build_dir = self.get_build_dir(arch.arch)
        cy = os.path.join(build_dir, "src_c", "cython")
        pyx_files = sorted(set(
            glob.glob(os.path.join(cy, "pygame", "*.pyx")) +
            glob.glob(os.path.join(cy, "pygame", "**", "*.pyx"), recursive=True)))
        for pyx in pyx_files:
            rel = os.path.relpath(pyx, cy)
            # pygame/_sdl2/sdl2.pyx -> src_c/_sdl2/sdl2.c ; pygame/_sprite.pyx -> src_c/_sprite.c
            out = os.path.join(build_dir, "src_c", os.path.splitext(rel)[0].split(os.sep, 1)[1] + ".c")
            if os.path.exists(out):
                os.remove(out)
            info("pygame: Cython {} -> {}".format(rel, os.path.relpath(out, build_dir)))
            subprocess.check_call([sys.executable, "-m", "cython", "-o", out, rel], cwd=cy)


recipe = PygameFixedRecipe()
