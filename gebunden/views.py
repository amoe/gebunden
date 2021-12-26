from pyramid.view import view_config
import pyramid.response
from gebunden.format_livejournal_archive import parse_entries

@view_config(
    route_name='home',
    renderer='gebunden:templates/home.j2'
)
def my_view(request):
    return {'project': 'myproject4'}


@view_config(
    route_name='entry',
    renderer='gebunden:templates/entry.j2'
)
def entry(request):
    month = request.matchdict['month']
    index = int(request.matchdict['index'])

    path = "{}/{}.xml".format(
        "/home/amoe/livejournal_amoe_archive",
        month
    )
    
    with open(path, 'r') as f:
        entries = parse_entries(f)

    if index > len(entries) - 1:
        raise Exception('invalid entry index')

    entry = entries[index]
    
    # ... do some crap here ...
    return {
        'event': entry.event, 'month': month, 'index': index,
        'event_time': entry.event_time, 'subject': entry.subject
    }
