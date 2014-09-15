# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>


from docutils import nodes
from docutils.parsers.rst import roles

# <codecell>

nodes.__doc()__

# <codecell>

help(nodes)

# <codecell>

 node = nodes.image(
        uri='http://www.tortue.me/emoji/{0}.png'.format(text),
        alt=text,
        classes=['emoji'],
    )

