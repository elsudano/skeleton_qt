# -*- mode: python ; coding: utf-8 -*-

import sys


APP_NAME = 'QtSkeleton'

TRANSLATION_FILES = [
    ('resources/translations/skeleton_es_ES.qm', 'resources/translations'),
    ('resources/translations/skeleton_en_US.qm', 'resources/translations'),
]

ASSET_FILES = [
    ('resources/assets/icon.ico', 'resources/assets'),
]

datas = TRANSLATION_FILES + ASSET_FILES

# ICO is appropriate for Windows. Linux does not require an executable icon
# for the PyInstaller build.
icon = 'resources/assets/icon.ico' if sys.platform == 'win32' else None

a = Analysis(
    ['main.py'],
    pathex=['.'],
    binaries=[],
    datas=datas,
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name=APP_NAME,
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    # UPX compression is disabled: compressed binaries trigger antivirus
    # false positives on Windows.
    upx=False,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=icon,
)
