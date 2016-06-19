#!/usr/bin/env python


import sys
import site_common as site_common

input_file = sys.argv[1]

#input_file = "src/test.md"


site_common.create_post(input_file)
