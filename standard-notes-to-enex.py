import json
import html
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

for key, item in enumerate(data['items']):
    if 'title' in item['content'] and 'text' in item['content']:
        title = item['content']['title']
        text = item['content']['text']
        text = text_from_html(title, text)
        final_file += '''<note><title>{title}</title><content><![CDATA[<!DOCTYPE en-note SYSTEM "http://xml.evernote.com/pub/enml2.dtd"><en-note>{text}</en-note>]]></content><created>20171228T194130Z</created><updated>20171228T194141Z</updated><note-attributes><author></author><source></source><reminder-order>0</reminder-order></note-attributes></note>'''.format(title=title, text=text)

# Save
with open("notes.enex", "w") as text_file:
    text_file.write(final_file)
