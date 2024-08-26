# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[
        ('bin/xgboost/lib/xgboost.dll', 'xgboost/lib')
    ],
    datas=[
        ('models', 'models'),
        ('resources', 'resources'),
        ('styles.qss', '.'),
        ('bin/xgboost/VERSION', 'xgboost'),
    ],
    hiddenimports=[
        'pickle', 'sklearn', 'sklearn.base', 'sklearn.compose', 'sklearn.datasets', 
        'sklearn.ensemble', 'sklearn.exceptions', 'sklearn.feature_extraction', 
        'sklearn.feature_selection', 'sklearn.impute', 'sklearn.kernel_approximation', 
        'sklearn.kernel_ridge', 'sklearn.linear_model', 'sklearn.metrics', 
        'sklearn.model_selection', 'sklearn.multioutput', 'sklearn.neighbors', 
        'sklearn.neural_network', 'sklearn.pipeline', 'sklearn.preprocessing', 
        'sklearn.random_projection', 'sklearn.svm', 'sklearn.tree', 
        'sklearn.utils', 'xgboost', 'xgboost.core', 'xgboost.compat', 
        'xgboost.training', 'xgboost.plotting', 'xgboost.callback', 
        'xgboost.sklearn', 'pandas'
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
    name='Carbon Predictor',
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
