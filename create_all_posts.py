#!/usr/bin/env python

import site_common as site_common


for md_file in site_common.posts:
    if len(md_file) == 2:
        md_file = md_file[0]
    site_common.create_post(md_file)
