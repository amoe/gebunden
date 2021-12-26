from pyramid.view import view_config
import pyramid.response
from gebunden.format_livejournal_archive import parse_entries
import os
import os.path
import re

@view_config(
    route_name='home',
    renderer='gebunden:templates/home.j2'
)
def my_view(request):
    return {'project': 'myproject4'}


def preformat(event: str):
    return event.replace('\n', '<br>')
    

BASE_DIR = "/home/amoe/livejournal_amoe_archive"

@view_config(
    route_name='entry',
    renderer='gebunden:templates/entry.j2'
)
def entry(request):
    month = request.matchdict['month']
    index = int(request.matchdict['index'])

    path = "{}/{}.xml".format(BASE_DIR, month)
    
    with open(path, 'r') as f:
        entries = parse_entries(f)

    if index > len(entries) - 1:
        raise Exception('invalid entry index')

    entry = entries[index]
    
    # ... do some crap here ...
    return {
        'event': preformat(entry.event),
        'month': month,
        'index': index,
        'event_time': entry.event_time,
        'subject': entry.subject
    }

def parse_file_name(name: str):
    m = re.fullmatch(r'(\d{4})-(\d?\d).xml', name)
    return (int(m.group(1)), int(m.group(2)))

@view_config(
    route_name='entries',
    renderer='gebunden:templates/entries.j2'
)
def entries(request):
    pairs = []
    
    for p in sorted(os.listdir(BASE_DIR), key=parse_file_name):
        fullpath = os.path.join(BASE_DIR, p)
        with open(fullpath, 'r') as f:
            count = len(parse_entries(f))
        pairs.append((p.removesuffix('.xml'), count))

    return {'pairs': pairs}
