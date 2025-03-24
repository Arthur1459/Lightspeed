# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[('rsc/maps/*.pkl', 'rsc/maps/'), ('rsc/*.*', 'rsc/'), ('rsc/visuals/*.*', 'rsc/visuals/'), ('rsc/visuals/player/stand/*.png', 'rsc/visuals/player/stand/'), ('rsc/visuals/player/run/*.png', 'rsc/visuals/player/run/'), ('rsc/visuals/player/jumpside/*.png', 'rsc/visuals/player/jumpside/'), ('rsc/visuals/player/fall/*.png', 'rsc/visuals/player/fall/'), ('rsc/visuals/player/slide/*.png', 'rsc/visuals/player/slide/'), ('rsc/visuals/player/dead/*.png', 'rsc/visuals/player/dead/'), ('rsc/visuals/blocks/metal_blocks/*.png', 'rsc/visuals/blocks/metal_blocks/'), ('rsc/visuals/blocks/fire_blocks/*.png', 'rsc/visuals/blocks/fire_blocks/'), ('rsc/visuals/blocks/fire_blocks/*.png', 'rsc/visuals/blocks/fire_blocks/'), ('rsc/visuals/particles/default/*.png', 'rsc/visuals/particles/default/'), ('rsc/visuals/particles/fire/*.png', 'rsc/visuals/particles/fire/'), ('rsc/visuals/particles/star/*.png', 'rsc/visuals/particles/star/'), ('rsc/visuals/particles/void/*.png', 'rsc/visuals/particles/void/')],
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
