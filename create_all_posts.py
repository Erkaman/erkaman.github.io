import site_common as site_common


for md_file in site_common.posts:
    site_common.create_post(md_file)
