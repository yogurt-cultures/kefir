from inspect import getmembers, isfunction

import kefir
from kefir import phonology
from kefir import predication
from kefir import case

modules_to_document = [
  kefir,
  case,
  phonology,
  predication,
]

DOCSTRING_TOKEN = "'''"

def include_line(part):
  return part.strip().startswith('#')

for module in modules_to_document:
  module_name = module.__name__
  content = open(module.__file__).read()
  docs = [
    part
    for part in content.split(DOCSTRING_TOKEN)
    if include_line(part)
  ]

  if module_name == 'kefir':
    print('<details open>')
    print('<summary open>%s</summary>' % module_name)
  else:
    print('<details>')
    print('<summary>%s</summary>' % module_name)

  for doc in docs:
    tab = '  '
    for line in doc.splitlines():
      if line.startswith(tab):
        print(line.lstrip(tab))
      else:
        print(line)
  print('</details>')

