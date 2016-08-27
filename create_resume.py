
with open('src/template.html', 'r') as f:
    template=f.read()

with open('src/resume.html', 'r') as f:
    resume_src=f.read()

src = template.format(src=resume_src)

with open('resume.html', 'w') as f:
    f.write(src)
