from ac_api import AcView, ac_template


class LoginView(AcView):
    @ac_template('login.jinja2')
    async def get(self):
        return {'name': 'RaspManager'}
