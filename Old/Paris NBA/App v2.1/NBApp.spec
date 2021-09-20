# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['Test.py'],
             pathex=['C:\\Users\\basti\\OneDrive\\Bureau\\NBA\\Paris NBA\\App v2.1'],
             binaries=[],
             datas=[],
             hiddenimports=['matplotlib.pyplot', 'sklearn.pipeline', 'sklearn.compose', 'sklearn.feature_selection', 'sklearn.neighbors._typedefs', 'sklearn.utils._weight_vector', 'sklearn.neural_network'],
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
          name='NBApp',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True )
