import importlib
import os
import pathlib
import sys

module_dir = pathlib.Path('module')


def find_all(app):
    module_all = {}
    for module_file in os.listdir(pathlib.Path('.') / module_dir):
        if module_file in module_all:
            continue
        module_all[module_file] = {
            'name': module_file,
            'module': f'{module_dir}.{module_file}',
            'loaded': False,
            'lib': None,
        }
    app['module_all'] = module_all


def load(module):
    lib = importlib.import_module(module['module'])
    module['loaded'] = True
    module['lib'] = lib
    return lib


def reload(module):
    if not module['loaded']:
        return
    lib = importlib.reload(module['module'])
    module['lib'] = lib
    return lib


def unload(module):
    del sys.modules[module['module']]
    module['loaded'] = False
    module['lib'] = None


def module_set(app):
    find_all(app)
    for module in app['module_all'].values():
        lib = load(module)
        plug_info = lib.plug_info
        app.add_subapp('/' + plug_info['url'], lib.app)
