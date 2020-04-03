from ac_api import ac_template, AcView


class ErrorView(AcView):
    @ac_template('error.jinja2')
    async def get(self):
        return {'name': 'RaspManager'}
