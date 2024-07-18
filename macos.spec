# -*- mode: python ; coding: utf-8 -*-


block_cipher = None

data_list = [
    ('./ab_launcher/assets/activity-browser.ico', './ab_launcher/assets/'),
    ('./ab_launcher/assets/activity-browser.icns', './ab_launcher/assets/'),
    ('./ab_launcher/assets/splash.png', './ab_launcher/assets/'),
]

a = Analysis(
    ['ab_launcher/main.py'],
    pathex=[],
    binaries=[],
    datas=data_list,
    hiddenimports=["logging.handlers"],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='Activity Browser',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='Activity Browser',
)
app = BUNDLE(
    coll,
    name='Activity Browser',
    icon='ab_launcher/assets/activity-browser.icns',
    bundle_identifier=None,
)
