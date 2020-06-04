import json
import html
import datetime
import re
from sys import argv

source = argv[1] if len(argv) > 1 else 'notes.txt'

data = json.load(open(source))


def text_from_html(title, text):
    # Clear title
    temp_text = text.replace(title + '\n\n  \n\n', '')
    # Parse to html
    temp_text = html.escape(temp_text)
    temp_text = temp_text.replace('\n', '<br>')
    return temp_text

final_file = '''
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE en-export SYSTEM "http://xml.evernote.com/pub/evernote-export3.dtd">
<en-export export-date="20171228T194211Z" application="Evernote" version="Evernote Mac 6.13.3 (455969)">
'''

tag_notes_links = {}
for key, item in enumerate(data['items']):
    if item['content_type'] == 'Tag':
        for inner_key, reference in enumerate(item['content']['references']):
            if 'uuid' not in reference:
                print(f"Missing UUID for one entry in {reference} ... this can happen sometimes ... reason so far unclear")
                continue
            if reference['uuid'] in tag_notes_links:
                tag_notes_links[reference['uuid']].append(html.escape(item['content']['title']))
            else:
                tag_notes_links[reference['uuid']] = [html.escape(item['content']['title'])]

for key, item in enumerate(data['items']):
 if item['content_type'] == 'Note':

    if 'title' in item['content']:
        title = item['content']['title']
        title = html.escape(title)
    else:
        title = "empty title"

    text = item['content']['text']
    text = text_from_html(title, text)

    if item['uuid'] not in tag_notes_links:
        print(f"Whoops .... {title} had no tag ... if this is expected, then safely ignore ... Setting tag: 'Missing-Standard-Notes-Tag'.")
        tag = 'Missing-Standard-Notes-Tag'
    else:
        tag = '</tag><tag>'.join(tag_notes_links[item['uuid']])

    # remove miliseconds and timezone ... example: 2020-04-14T14:30:09.256Z => 2020-04-14T14:30:09
    # we assume zulu time for all dates (UTC)
    created_at = datetime.datetime.strptime(item['created_at'][0:19], '%Y-%m-%dT%H:%M:%S').strftime('%Y%m%dT%H%M%SZ')
    updated_at = datetime.datetime.strptime(item['updated_at'][0:19], '%Y-%m-%dT%H:%M:%S').strftime('%Y%m%dT%H%M%SZ')


    final_file += '''<note><title>{title}</title><content><![CDATA[<!DOCTYPE en-note SYSTEM "http://xml.evernote.com/pub/enml2.dtd"><en-note>{text}</en-note>]]></content><created>{created_at}</created><updated>{updated_at}</updated><tag>{tag}</tag><note-attributes><author></author><source></source><reminder-order>0</reminder-order></note-attributes></note>'''.format(title=title, text=text, tag=tag, created_at=created_at, updated_at=updated_at)

final_file += '''</en-export>''' # close root tag


# Save
with open("notes.enex", "w") as text_file:
    text_file.write(final_file)

