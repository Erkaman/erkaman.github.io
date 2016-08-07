
import markdown2
import datetime

posts = [
    "src/regl_anim.md",
    "src/cuda_rle.md",
    "src/tess_opt.md"
]

def get_html_file(md_file):
    return "posts/"+md_file[4:-3] + ".html"

def get_begin():

    begin = """
<!DOCTYPE html>
<html>
  <head>
    <title>Magnum Opus</title>
    <meta name="viewport" content="width=device-width,initial-scale=1">
    <style>
"""

# add CSS styling.

    with open('style.css', 'r') as f:
        css=f.read()

    begin += css

# add top title and stuff:
    begin += """
    </style>
  </head>
  <body>
    <div id="container">

     <div class="center-box">
       <div id="top">
         <a id="blog-title" href="/">Magnum Opus</a>
         <p id="blog-title-under">A humble little blog about programming</p>
       </div>
     </div>
     <div class="center-box">
"""
    return begin

def get_end():
    end = """
    </div>

    </div>

    <div id="footer">Blog made by Eric Arneb&#228;ck.
    <a href="mailto:arnebackeric@gmail.com">Email</a>.
    <a href="https://github.com/Erkaman">Github</a>

    </div>

  </body>
</html>
"""
    return end

def create_post(input_file):

    html_source = get_begin()

    with open(input_file, 'r') as f:
        markdown_source=f.read()

    # process markdown.
    html_source += markdown2.markdown(markdown_source, extras=["fenced-code-blocks","tables"])

    # finally, add update date.
    now = datetime.datetime.now()
    html_source +=  "<p class=\"last-update\"> <i>This post was last updated: " + now.strftime("%B %d, %Y") + "</i></p>"

    html_source += get_end()

    output_file = get_html_file(input_file)

    with open(output_file, 'w') as f:
        f.write(html_source)
