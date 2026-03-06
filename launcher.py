# launcher to be added to the exe file

import os
import sys
import threading
from multiprocessing import Process, set_start_method
import time
import traceback
import webview
import logging

# Reduce noisy logs
logging.getLogger('streamlit').setLevel(logging.ERROR)

# Resolve base directory for PyInstaller onefile
if getattr(sys, 'frozen', False):
    # _MEIPASS contains extracted resources (read-only temp folder)
    BASE_DIR = sys._MEIPASS
    # EXE_DIR is where the actual executable lives (for persistent files)
    EXE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    EXE_DIR = BASE_DIR

# chefMariusV2.py is extracted to _MEIPASS root (via --add-data=chefMariusV2.py;.)
APP_PATH = os.path.join(BASE_DIR, 'chefMariusV2.py')
PORT = os.environ.get('STREAMLIT_SERVER_PORT', '8501')
URL = f'http://127.0.0.1:{PORT}'


def _run_streamlit_proc():
    """Run Streamlit server in a separate process (Windows-safe)."""
    # Sanity log
    print(f'▶️  Iniciando Streamlit com app: {APP_PATH}')
    print(f'    BASE_DIR: {BASE_DIR}')
    print(f'    EXE_DIR: {EXE_DIR}')
    print(f'    Porta: {PORT}')

    # Ensure app file exists (both dev and PyInstaller runtime)
    if not os.path.exists(APP_PATH):
        print('❌ Arquivo do app não encontrado. Caminho esperado:')
        print(f'   {APP_PATH}')
        return

    # ========== PyInstaller + Streamlit compatibility fixes ==========
    # Streamlit needs writable directories for config/cache. When frozen,
    # _MEIPASS is read-only and temp. We create persistent dirs next to the .exe.
    
    if getattr(sys, 'frozen', False):
        # Create a .streamlit config folder next to the executable
        streamlit_config_dir = os.path.join(EXE_DIR, '.streamlit')
        os.makedirs(streamlit_config_dir, exist_ok=True)
        
        # Create a cache folder for Streamlit
        streamlit_cache_dir = os.path.join(EXE_DIR, '.streamlit_cache')
        os.makedirs(streamlit_cache_dir, exist_ok=True)
        
        # Point Streamlit to use these directories
        os.environ['STREAMLIT_CONFIG_DIR'] = streamlit_config_dir
        os.environ['STREAMLIT_CACHE_DIR'] = streamlit_cache_dir
        
        # Set HOME to EXE_DIR so Streamlit finds .streamlit there
        os.environ['HOME'] = EXE_DIR
        os.environ['USERPROFILE'] = EXE_DIR
        
        # Disable file watcher (causes issues in frozen apps)
        os.environ['STREAMLIT_SERVER_FILE_WATCHER_TYPE'] = 'none'
        
        # CRITICAL: Disable development mode - conflicts with server.port
        os.environ['STREAMLIT_GLOBAL_DEVELOPMENT_MODE'] = 'false'

    # Configure via environment
    os.environ['STREAMLIT_SERVER_PORT'] = PORT
    # Ensure Streamlit does NOT auto-open the system browser
    os.environ['STREAMLIT_SERVER_HEADLESS'] = 'true'
    os.environ['STREAMLIT_BROWSER_GATHER_USAGE_STATS'] = 'false'
    # Block Python's webbrowser auto-open just in case
    os.environ['BROWSER'] = 'none'

    # Invoke CLI main explicitly with headless flag to prevent auto browser
    try:
        from streamlit.web.cli import main as st_main
        sys.argv = [
            'streamlit', 'run', APP_PATH,
            '--server.headless', 'true',
            '--browser.gatherUsageStats', 'false',
            '--server.fileWatcherType', 'none',
            '--global.developmentMode', 'false',
        ]
        st_main()
    except SystemExit:
        pass
    except Exception:
        print('❌ Erro ao executar Streamlit (CLI):')
        traceback.print_exc()

def _wait_for_server(timeout=60):
    """Wait until the local Streamlit server responds or timeout."""
    import requests
    start = time.time()
    while time.time() - start < timeout:
        try:
            r = requests.get(URL, timeout=0.7)
            if r.status_code < 500:
                return True
        except Exception:
            time.sleep(0.5)
    return False


def main():
    # Ensure multiprocessing uses spawn on Windows
    try:
        set_start_method('spawn')
    except RuntimeError:
        # Already set; ignore
        pass

    # If a server is already running (e.g., accidental relaunch), don't start another
    if not _wait_for_server(timeout=1):
        # Start streamlit server in a separate process
        proc = Process(target=_run_streamlit_proc, daemon=True)
        proc.start()
    else:
        proc = None

    # Wait for server to be ready
    ready = _wait_for_server(timeout=60)
    if not ready:
        print('⚠️  Servidor Streamlit não respondeu dentro do tempo esperado.')
        print(f'Tente acessar manualmente: {URL}')

    # Open embedded window pointing to the local app (fallback to system browser if backend missing)
    try:
        webview.create_window('Receitas', URL, width=1100, height=700)
        webview.start()
    except Exception:
        import webbrowser
        print('⚠️  pywebview falhou. Abrindo no navegador padrão...')
        time.sleep(1)
        webbrowser.open(URL)

    # Cleanup: ensure server process exits when UI closes
    if proc is not None and proc.is_alive():
        try:
            proc.terminate()
        except Exception:
            pass



if __name__ == '__main__':
    try:
        from multiprocessing import freeze_support
        freeze_support()
    except Exception:
        pass
    main()
