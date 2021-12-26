from pyramid.config import Configurator
import gebunden.views

def main(global_config, **settings):
    with Configurator(settings=settings) as config:
        config.include('pyramid_jinja2')
        config.add_jinja2_renderer('.j2')

        config.add_static_view('static', 'static')
        
        config.add_route('home', '/')
        config.add_route('entry',  '/entry/{month}/{index}')
        config.add_route('entries',  '/entries')

        # Only views defined in this module will be found.
        # @view_config decorator will configure them.
        # It's important for readability that we restrict the scan here,
        # instead of using a bare 'config.scan()'.
        config.scan(package=gebunden.views)
    return config.make_wsgi_app()
