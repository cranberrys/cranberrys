import pathlib

module_dir = pathlib.Path('module')


def _set_template_path(app):
    """

    :type app: AcApplication
    """
    static_path = pathlib.Path(app.module.path) / "template"
    if static_path.exists():
        app.ac_set_static_path(static_path)


def _set_static_path(app):
    """

    :type app: AcApplication
    """
    static_path = pathlib.Path(app.module.path) / "static"
    if static_path.exists():
        app.ac_set_static_path(static_path)


def module_set(board):
    for module in board.module_all.values():
        if module.enable:
            module.app = module.lib.get_app()
            module.app.board = board
            module.app.module = module

            _set_template_path(module.app)
            _set_static_path(module.app)

            board.add_subapp('/' + module.name, module.app)
            module.loaded = True
