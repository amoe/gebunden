import pdb
import bs4
import attr
from datetime import datetime
import os
import sys
import jinja2

doc = """
<?xml version="1.0" encoding='utf-8'?>
<livejournal>
<entry>
<eventtime>2001-04-01 15:04:00</eventtime>
<subject>foo</subject>
<event>bar</event>
</entry>
</livejournal>
"""

css = """
body{margin:40px
auto;max-width:650px;line-height:1.6;font-size:18px;color:#444;padding:0
10px}h1,h2,h3{line-height:1.2}

div.subject { font-weight: bold; }

div.entry { margin-bottom: 1em; }
"""

template = """
<style type="text/css">{{ css }}</style>
<div class="all_entries">
{% for entry in entries %}
  <div class="entry">
    <div class="event_time">{{ entry.event_time }}</div>

    <div class="subject">
      {% if entry.subject %}
      {{ entry.subject }}
      {% else %}
      (no subject)
      {% endif %}
    </div>

    <div class="event">
      {{ entry.event }}
    </div>
  </div>
{% endfor %}
</div>
"""

@attr.attrs
class Entry(object):
    event_time = attr.attrib()
    subject = attr.attrib()
    event = attr.attrib()

    @classmethod
    def from_text(cls, eventtime: str, subject: str, event: str):
        return Entry(
            datetime.strptime(eventtime, '%Y-%m-%d %H:%M:%S'),
            subject,
            event
        )
    
def parse_entries(f):
    entries = []
    soup = bs4.BeautifulSoup(f, features='lxml')
    for entry in soup.find_all('entry'):
        eventtime = entry.eventtime.get_text()
        subject = entry.subject.get_text()
        event = entry.event.get_text()

        entries.append(Entry.from_text(eventtime, subject, event))
        
    return entries


class Foo:
    def run(self, directory):
        all_entries = []

        for path in os.listdir(directory):
            fullpath = os.path.join(directory, path)
            with open(fullpath, 'r') as f:
                result = parse_entries(f)
            all_entries.extend(result)

        print("Collected", len(all_entries), "entries")
        rtemplate = jinja2.Environment(
            loader=jinja2.BaseLoader(), undefined=jinja2.StrictUndefined
        ).from_string(template)
        sorted_entries = sorted(all_entries, key=lambda e: e.event_time)
        print(rtemplate.render(entries=sorted_entries, css=css))

    

