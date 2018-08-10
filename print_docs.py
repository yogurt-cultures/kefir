from inspect import getmembers, isfunction

import kefir
from kefir import phonology
from kefir import predication
from kefir import case

modules_to_document = [
  kefir,
  phonology,
  case,
  predication,
]

for module in modules_to_document:
  print(module.__doc__)

  functions = [
    o for o in getmembers(module)
            if isfunction(o[1])
    ]

  for (name, function) in functions:
    doc = function.__doc__

    if not doc:
      continue

    tab = '  '
    for line in doc.splitlines():
      if line.startswith(tab):
        print(line.lstrip(tab))
      else:
        print(line)
