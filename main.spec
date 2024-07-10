# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


datafiles = [
    ('./install.py', '.'),
    ('./launch.py', '.'),
    ('./download/win-environment.tar.gz', './download/'),
    ('./download/win-environment_spec.txt', './download/'),
    ('./download/mac-environment.tar.gz', './download/'),
    ('./download/mac-environment_spec.txt', './download/'),
]


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=datafiles,
    hiddenimports=[],
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
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='main',
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
)
app = BUNDLE(
    exe,
    name='main.app',
    icon=None,
    bundle_identifier=None,
)
