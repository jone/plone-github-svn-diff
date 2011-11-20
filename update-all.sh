#!/usr/bin/env sh

echo "Update plone -> plone.md"
/usr/bin/env python2.6 diff-plone.py > plone.md

echo "Update archetypes -> archetypes.md"
/usr/bin/env python2.6 diff-archetypes.py > archetypes.md

echo "Update collective -> collective.md"
/usr/bin/env python2.6 diff-collective.py > collective.md
