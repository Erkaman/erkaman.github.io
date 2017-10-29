
import markdown2
import datetime

with open('test2.md', 'r') as f:
    markdown_source=f.read()

# process markdown.
article_src = markdown2.markdown(markdown_source, extras=["fenced-code-blocks","tables"])

with open('formatted', 'w') as f:
    f.write(article_src)
