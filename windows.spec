# -*- mode: python ; coding: utf-8 -*-

data_list = [
    ('./ab_launcher/runners/install-runner.py', './ab_launcher/runners/'),
    ('./ab_launcher/runners/launch-runner.py', './ab_launcher/runners/'),
    ('./ab_launcher/assets/activity-browser.ico', './ab_launcher/assets/'),
    ('./ab_launcher/assets/splash.png', './ab_launcher/assets/'),
]


a = Analysis(
    ['ab_launcher/main.py'],
    pathex=[],
    binaries=[],
    datas=data_list,
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
    name='Activity Browser',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['ab_launcher\\assets\\activity-browser.ico'],
)


