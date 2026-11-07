# Pixel Pisun: Construction of the Century
# Copyright (C) 2026 niko7600 <https://github.com/niko7600/pisun_platformer>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
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
