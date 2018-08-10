"""
![Logo](https://avatars1.githubusercontent.com/u/42190640?s=200&v=4)

Yogurt is a free software community that establised in `Mustafa Akgul Ozgul Yazılım Kampı` in 2018.

Kefir is a natural language processing kit for Turkic languages, and maybe Finnish and Hungarian in phonology.

# Credits

  - Berk Buzcu (8-bit artwork)
  - Serdar Açıkyol (Illustration)
  - Fatih Erikli (Phonological processes, Predicate Logic)

# Contribution guide
- Don't load a fixture, code is our data.
- Don't leave a comment! Docstrings are only for the context and test.
- Be nice 🦄

# How to use

There are two competing notions of the predicate in theories of grammar.
The competition between these two concepts has generated confusion concerning
the use of the term predicate in theories of grammar.

Kefir is designed to construct sentences by predicate-logic.  
https://www.wikiwand.com/en/Predicate_(grammar)

```python
>>> sentence(subject('ali'), predicate('öl'))
'ali öl'

```
"""
from .subject import subject
from .predication import predicate

def sentence(subject, predicate, delimiter=' '):
  return delimiter.join((subject, predicate))

if __name__ == "__main__":
    import doctest
    doctest.testmod()
