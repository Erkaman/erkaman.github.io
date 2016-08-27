
with open('src/template.html', 'r') as f:
    template=f.read()

with open('src/index.html', 'r') as f:
    index_src=f.read()


s = """
  <div class="row gallery-row">
    <div class="one-third column">
      <img src="/img/gallery/deferred_shading.png" alt="img" >
    </div>
    <div class="one-third column">
      <img src="/img/gallery/deferred_shading.png" alt="img" >
    </div>
    <div class="one-third column">
      <img src="/img/gallery/deferred_shading.png" alt="img" >
    </div>
  </div>
"""

# extract all the rows from the file.
with open('src/img_list.txt', 'r') as f:
    rows = []
    row = []
    for line in f.readlines():
        l = line.split()
        img = l[0]
        href = l[1]

        if len(row) == 3:
            rows.append(row)
            row = []

        row.append([img, href])
    if len(row) > 0: # add last row
        rows.append(row)

img_list_src = ""

# now format the rows as html
for row in rows:
    row_src = ""
    row_src += '<div class="row gallery-row">'
    for e in row:
        row_src += """
        <div class="one-third column">
        <a href="{link}"><img src="{img}" alt="img" ></a>
        </div>
        """.format(img=e[0], link=e[1])

    row_src += '</div>'
    img_list_src = row_src + img_list_src

index_src = index_src.format(img_list=img_list_src)

src = template.format(src=index_src)

with open('index.html', 'w') as f:
    f.write(src)
