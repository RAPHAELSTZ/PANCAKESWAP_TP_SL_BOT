# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(['pancake.py'],
             pathex=['C:\\Users\\Ragnar_lothbroke\\Desktop\\Bureau\\DEV\\BOTS\\uberbot'],
             binaries=[],
             datas=[],
             hiddenimports=[],
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
          [],
          exclude_binaries=True,
          name='pancake',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True , icon='pancakes_icon.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='pancake')
