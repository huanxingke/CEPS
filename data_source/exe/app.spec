# -*- mode: python ; coding: utf-8 -*-
import sys
sys.setrecursionlimit(5000)

block_cipher = None

py_files = [
    'app_png.py',
    'main.py',
    'app.py',
    'get_pip.py'
]

a = Analysis(py_files,
             pathex=['F:\\Study\\Python\\PythonAdventure\\Scraper\\Dissertation-Others\\EXEClient\\main.py'],
             binaries=[],
             datas=[],
             hiddenimports=['psutil', 'PyQt5', 'requests'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='Chemical-EPS',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False,
          icon='F:\\Study\\Python\\PythonAdventure\\Scraper\\Dissertation-Others\\EXEClient\\app.ico')
