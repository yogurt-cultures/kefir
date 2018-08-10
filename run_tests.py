import unittest
import doctest

import kefir
from kefir import predication
from kefir import case
from kefir import phonology

modules_to_test = [
  kefir,
  predication,
  case,
  phonology,
]

testSuite = unittest.TestSuite()

for module in modules_to_test:
  testSuite.addTest(doctest.DocTestSuite(module))

unittest.TextTestRunner(
  verbosity=2
).run(
  testSuite
)
