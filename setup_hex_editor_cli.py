from distutils.core import setup
import py2exe

setup(
    options = {
        'py2exe': {
            'bundle_files': 1, 
            'compressed': True,
            'includes': ['hex_editor']
            }
        },
    console = [{'script': "hex_editor_cli.py"}],
    zipfile = None,
)