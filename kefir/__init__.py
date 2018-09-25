'''
# Kefir

![Logo](https://avatars1.githubusercontent.com/u/42190640?s=200&v=4)

Yogurt is a free software community established at Mustafa Akgül Free Software Camp of 2018.

Kefir is a natural language processing kit for Turkic languages, and maybe Finnish and Hungarian in phonology.

# Credits

  - Berk Buzcu (8-bit artwork)
  - Serdar Açıkyol (Illustration)
  - Fatih Erikli (Phonology, Predicate Logic)
  - Umut Karcı (Packaging)
  - Armağan Amcalar (Javascript Port)
  - Mirkan Kılıç (Predicate Combinations) 

# Contribution guide
- Don't load a fixture, code is our data.
- Don't leave a comment! Docstrings are only for the context and test.
- Be nice 🦄

# Usage
There are two competing notions of the predicate in theories of grammar.
The competition between these two concepts has generated confusion concerning
the use of the term predicate in theories of grammar.

Kefir is designed to construct sentences by using
[predicate-logic](https://www.wikiwand.com/en/Predicate_(grammar)).

## Combining predicates (birleşik yapılı fiiller)

```python
>>> ayni = subject('aynı')
>>> havuc = subject('havuç')
>>> gel = predicate('gel', 'third', 'perfective')
>>> yap = predicate('yap', 'third', 'perfective')
>>> dal = predicate('dal', 'third', 'progressive')
>>> dal = predicate(dal, 'third', 'perfective')

>>> birisi = subject('yakup')
>>> [sentence(birisi, eylem) for eylem in (yap, dal,)]
['yakup yaptı', 'yakup dalmaktaydı']

>>> [sentence(havuc, eylem) for eylem in (gel, yap, dal)]
['havuç geldi', 'havuç yaptı', 'havuç dalmaktaydı']

>>> sebze = predicate(locative('marul'), 'first', 'perfective', True)
>>> dal = predicate(locative('dal'), 'first', 'perfective', True)
>>> [sentence(ayni, eylem) for eylem in (sebze, dal)]
['aynı maruldaydık', 'aynı daldaydık']

```

### Cases

  - nominative
  - genitive
  - dative
  - accusative
  - ablative
  - locative

### Copulas

 - negative
 - zero
 - tobe
 - personal
 - perfective
 - imperfective
 - progressive
 - necessitative
 - future
 - impotential
 - conditional

'''
from .subject import subject, locative, genitive
from .predication import predicate, Copula
from .functional import enum_values

def sentence(subject, predicate, delimiter=' '):
  return delimiter.join((subject, predicate))

if __name__ == "__main__":
    import doctest
    doctest.testmod()
