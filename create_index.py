
with open('src/template.html', 'r') as f:
    template=f.read()

with open('src/index.html', 'r') as f:
    index_src=f.read()

src = template.format(src=index_src)

with open('index.html', 'w') as f:
    f.write(src)
