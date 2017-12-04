#!/usr/bin/env python

import sys
import site_common as site_common

html_source = ''
html_source += '<div class="container">'
html_source += """<h1>Articles <a href="/rss.xml" title="RSS feed"><img src="/img/rss.png" alt="RSS" class="feed-button"></a></h1>"""
html_source += "<p>Below are some small articles and tutorials I have written. They are mostly about computer graphics, and mathematics that is useful in computer graphics. </p>"

html_source += """"""

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

    post_title = ""
    if len(md_file) == 2:
        post_title = md_file[1]
    else:
        post_title = extract_title(md_file)

    html_file = ""
    if len(md_file) == 2:
        html_file = "posts/"+md_file[0][4:-5] + '.html'
    else:
        html_file = site_common.get_html_file(md_file)


    html_source += "<li> <a href=\"{0}\">{1}</a>  </li>".format(
        html_file,post_title )
html_source += "</ul>"

html_source += '</div>'

with open('src/template.html', 'r') as f:
    template=f.read()

output_file = "articles.html"

src = template.format(src=html_source)

with open(output_file, 'w') as f:
     f.write(src)
