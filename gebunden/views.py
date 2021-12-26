from pyramid.view import view_config

@view_config(
    route_name='home',
    renderer='gebunden:templates/home.j2'
)
def my_view(request):
    return {'project': 'myproject4'}
