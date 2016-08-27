import xml.etree.ElementTree as ET

with open('src/template.html', 'r') as f:
    template=f.read()

with open('src/projects.html', 'r') as f:
    project_src=f.read()

project_list = ""

def elem2str(elem):
    elem.text + ''.join(ET.tostring(e) for e in elem)


    # print elem

    # s = ''
    # for c in elem.child:
    #     s += ET.tostring(c)
    # return s


# parse the list of project from an xml file, and
# then format as html.
tree = ET.parse('src/project_list.xml')
root = tree.getroot()
#print ET.tostring(root)
first = True
for child in root:
    title = child[0].text
    href = child[1].text
    img = child[2].text
    text = ET.tostring(child[3])[6:-11]

    project_list += "<hr>"

    project_list += """
  <div class="row project-row">
    <div class="two-thirds column">
      <h2><a href="{href}">{title}</a></h2>
      {text}
    </div>
    <div class="one-third column">
      <a href="{href}"><img src="{img}" alt="img"></a>
    </div>
  </div>
    """.format(href=href, text=text, title=title, img=img)

project_src = project_src.format(project_list = project_list)

src = template.format(src=project_src)

with open('projects.html', 'w') as f:
    f.write(src)
