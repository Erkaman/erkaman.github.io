
import markdown2
import datetime

posts = [
    ("src/harmonic_map.html", "Automatic UV mapping using Harmonic Mapping: A tutorial and Introduction"),
    "src/regl_anim.md",
    "src/cuda_rle.md",
    "src/tess_opt.md",
]

def get_html_file(md_file):
    return "posts/"+md_file[4:-3] + ".html"

def create_post(input_file):

    with open('src/template.html', 'r') as f:
        template=f.read()

    if input_file[-5:] == '.html':

        with open(input_file, 'r') as f:
            html_source=f.read()

        # process markdown.
        article_src = '<div class="container">' + html_source + '</div>'
        src = template.format(src=article_src)

        output_file = "posts/"+input_file[4:-5] + '.html'

        print output_file

        with open(output_file, 'w') as f:
            f.write(src)

    else:

        with open(input_file, 'r') as f:
            markdown_source=f.read()

        # process markdown.
        article_src = '<div class="container">' + markdown2.markdown(markdown_source, extras=["fenced-code-blocks","tables"]) + '</div>'

        src = template.format(src=article_src)

        output_file = get_html_file(input_file)

        with open(output_file, 'w') as f:
            f.write(src)
