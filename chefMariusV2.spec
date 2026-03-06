# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_all

datas = [('chefMariusV2.py', '.'), ('ReceitasGravadas', 'ReceitasGravadas')]
binaries = []
hiddenimports = ['streamlit', 'streamlit.web.cli', 'streamlit.web.bootstrap', 'streamlit.config', 'streamlit.runtime', 'streamlit.runtime.scriptrunner', 'blinker', 'toml', 'langchain', 'langchain_core', 'langchain_groq', 'langchain_community', 'langchain_community.callbacks.streamlit', 'reportlab', 'reportlab.pdfgen', 'reportlab.platypus', 'reportlab.lib', 'reportlab.lib.styles', 'reportlab.lib.utils', 'reportlab.pdfbase', 'reportlab.pdfbase.ttfonts', 'webview', 'requests', 'groq']
tmp_ret = collect_all('streamlit')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]
tmp_ret = collect_all('reportlab')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]
tmp_ret = collect_all('blinker')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]


a = Analysis(
    ['launcher.py'],
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
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
    [],
    exclude_binaries=True,
    name='chefMariusV2',
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
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='chefMariusV2',
)
