
with open('src/template.html', 'r') as f:
    template=f.read()

with open('src/projects.html', 'r') as f:
    projects_src=f.read()

src = template.format(src=projects_src)

with open('projects.html', 'w') as f:
    f.write(src)
