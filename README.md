# erkaman.github.io

This is the source code of my personal website and portfolio. It uses
[skeleton](https://github.com/dhg/Skeleton) to create a responsive
layout that works on mobile. All the pages of the site are created by a
bunch of python scripts. You can create all pages of the site by running:

```bash
python create_index.py && python create_resume.py && python create_projects.py && python create_all_posts.py && python create_articles_index.py
```

The above scripts will use the source files in `src/` as input, and
use them to create the actual HTML files.
