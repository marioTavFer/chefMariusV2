"""
Build script: creates a single executable that runs the Streamlit app
embedded in a desktop window (via pywebview). Works on laptops without
Python or Streamlit installed.

NOTE: Using --onedir creates a folder with all files already extracted.
This provides INSTANT startup (no extraction needed). To distribute:
  - Copy the entire 'dist/chefMariusV2/' folder to the target machine
  - Run 'chefMariusV2.exe' inside that folder
  - Optionally create a shortcut to the .exe
"""

import PyInstaller.__main__

pyinstaller_args = [
    'launcher.py',
    '--name=chefMariusV2',
    '--onedir',  # Creates a folder instead of single file - MUCH faster startup!
    '--clean',
    # Include runtime data folders (use ';' on Windows)
    #'--add-data=fonts;fonts',
    # Include the Streamlit app source so Streamlit can run it from _MEIPASS
    '--add-data=chefMariusV2.py;.',
    # Include ReceitasGravadas folder for initial state
    '--add-data=ReceitasGravadas;ReceitasGravadas',
    # Hidden imports required at runtime
    '--hidden-import=streamlit',
    '--hidden-import=streamlit.web.cli',
    '--hidden-import=streamlit.web.bootstrap',
    '--hidden-import=streamlit.config',
    '--hidden-import=streamlit.runtime',
    '--hidden-import=streamlit.runtime.scriptrunner',
    '--hidden-import=blinker',
    '--hidden-import=toml',
    '--hidden-import=langchain',
    '--hidden-import=langchain_core',
    '--hidden-import=langchain_groq',
    '--hidden-import=langchain_community',
    '--hidden-import=langchain_community.callbacks.streamlit',
    '--hidden-import=reportlab',
    '--hidden-import=reportlab.pdfgen',
    '--hidden-import=reportlab.platypus',
    '--hidden-import=reportlab.lib',
    '--hidden-import=reportlab.lib.styles',
    '--hidden-import=reportlab.lib.utils',
    '--hidden-import=reportlab.pdfbase',
    '--hidden-import=reportlab.pdfbase.ttfonts',
    '--hidden-import=webview',
    '--hidden-import=requests',
    '--hidden-import=groq',
    # Collect package resources (Streamlit static assets, ReportLab fonts)
    '--collect-all=streamlit',
    '--collect-all=reportlab',
    '--collect-all=blinker',
    # Output paths
    '--distpath=dist',
    '--workpath=build',
    #'--specpath=spec',
]

print('🔨 Building single executable (chefMariusV2.exe)...')
PyInstaller.__main__.run(pyinstaller_args)
print('✅ Done. dist/chefMariusV2.exe created.')