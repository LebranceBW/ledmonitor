# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ['ledmonitor.py'],
    pathex=[],
    binaries=[('.venv/Lib/site-packages/HardwareMonitor/lib/LibreHardwareMonitorLib.dll', 'HardwareMonitor/lib'),
           ('.venv/Lib/site-packages/HardwareMonitor/lib/HidSharp.dll', 'HardwareMonitor/lib')],
    datas=[('config/config.toml', '.')],
    hiddenimports=[
        'toml',
        'toml.decoder',
        'toml.encoder',
        'bleak',
        'argparse',
        'asyncio',
        'logging',
        'logging.handlers',
        'dynaconf',
        'HardwareMonitor',
        'HardwareMonitor.Util'
    ],
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
    name='ledmonitor',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    uac_admin=True,
)