from pyramid.view import view_config
import pyramid.response
import gebunden.format_livejournal_archive

@view_config(
    route_name='home',
    renderer='gebunden:templates/home.j2'
)
def my_view(request):
    return {'project': 'myproject4'}


@view_config(
    route_name='entry',
)
def entry(request):
    month = request.matchdict['month']
    index = request.matchdict['index']
    # ... do some crap here ...
    return pyramid.response.Response("Hello, world!")
