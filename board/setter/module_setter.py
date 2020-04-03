import pathlib

from ac_api import AcApi

module_dir = pathlib.Path('module')


def module_set(board):
    for module in board.module_all.values():
        if module.enable:
            module.app = module.lib.get_app()
            board.add_subapp('/' + module.name, module.app)
            module.app['board'] = board
            module.app['board_api'] = AcApi(module.name, module.app)
            module.loaded = True
