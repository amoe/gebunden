from pyramid.config import Configurator


def main(global_config, **settings):
    with Configurator(settings=settings) as config:
        config.include('pyramid_jinja2')

        config.add_static_view('static', 'static')
        config.add_route('home', '/')
        config.scan()
    return config.make_wsgi_app()
