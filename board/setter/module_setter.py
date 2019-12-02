import importlib
import os
import pathlib
import sys

from ac_api import AcApi

module_dir = pathlib.Path('module')


def find_all(app):
    module_all = {}
    for module_file in os.listdir(pathlib.Path('.') / module_dir):
        if module_file in module_all:
            continue
        module_all[module_file] = {
            'name': module_file,
            'module': f'{module_dir}.{module_file}',
            'lib': None,
            'loaded': False,
            'enable': True,
            'message': '',
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
        if 'id' not in lib.plug_info:
            module['message'] = '插件 plug_info 配置错误，缺少 id'
            load(module)
            continue
        lib.plug_info['index'] = lib.app.router.get(lib.plug_info['index'])
        lib.plug_info['config'] = lib.app.router.get(lib.plug_info['config'])
        lib.app['api'] = AcApi(lib.plug_info['id'], lib.app)

        app.add_subapp('/' + lib.plug_info['id'], lib.app)
        module['message'] = '插件加载成功'
