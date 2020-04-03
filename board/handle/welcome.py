from ac_api import AcView, ac_template


class WelcomeView(AcView):
    @ac_template('welcome.jinja2')
    async def get(self):
        return {'name': 'RaspManager'}
