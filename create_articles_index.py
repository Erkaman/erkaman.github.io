#!/usr/bin/env python

import sys
import site_common as site_common

html_source = ''
html_source += '<div class="container">'
html_source += "<h1>Articles</h1>"
html_source += "<p>Below are some small articles and tutorials I have written.</p>"

def extract_title(md_file):
    # extract the title of a post, from the first line in the file.
    with open(md_file, 'r') as f:
        first_line = f.readline()


    # skip hash and any whitespace in beginning.
    for i, c in enumerate(first_line):
        if not c.isspace() and c != "#":
            # found beginning of title
            return first_line[i:]

    return "Invalid Title!"

html_source += "<ul>"
for md_file in site_common.posts:

    html_source += "<li> <a href=\"{0}\">{1}</a>  </li>".format(
        site_common.get_html_file(md_file), extract_title(md_file))
html_source += "</ul>"

html_source += '</div>'

with open('src/template.html', 'r') as f:
    template=f.read()

output_file = "articles.html"

src = template.format(src=html_source)

with open(output_file, 'w') as f:
     f.write(src)
