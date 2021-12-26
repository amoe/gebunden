from pyramid.config import Configurator
import gebunden.views

def main(global_config, **settings):
    with Configurator(settings=settings) as config:
        config.include('pyramid_jinja2')
        config.add_jinja2_renderer('.j2')

        config.add_static_view('static', 'static')
        
        config.add_view(gebunden.views.my_view)
        
        config.add_route('home', '/')
        config.scan()
    return config.make_wsgi_app()
