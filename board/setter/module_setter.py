import pathlib

from ac_api import AcApi

module_dir = pathlib.Path('module')


def module_set(board):
    for module in board.module_all.values():
        if module.enable:
            board.add_subapp('/' + module.lib.plug_info['id'], module.lib.app)
            module.lib.app['board'] = board
            module.lib.app['board_api'] = AcApi(module.lib.plug_info['id'], module.lib.app)
            module.loaded = True
