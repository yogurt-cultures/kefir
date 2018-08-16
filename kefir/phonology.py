'''
# Turkish phonology

In Hungarian, Finnish, and Turkic languages
vowel sounds are organized in a concept called
vowel harmony. Vowels may be classified as Back
or Front vowels, based on the placement of the
sound in the mouth.

```
 Front Vowels
+----------------+
 Unrounded  ⟨e⟩ ⟨i⟩
 Rounded    ⟨ü⟩ ⟨ö⟩

 Back Vowels
+----------------+
 Unrounded  ⟨a⟩ ⟨ı⟩
 Rounded    ⟨u⟩ ⟨o⟩
```

TODO: Document consonant harmony.
'''
from enum import Enum

from .functional import enum_values, join, reduce

class MissingVowelSound(Exception):
  pass

class Front(Enum):
  E = 'e'
  I = 'i'
  U = 'ü'
  O = 'ö'

class Back(Enum):
  A = 'a'
  I = 'ı'
  U = 'u'
  O = 'o'

ROUNDED_FRONT_VOWELS =   {
  Front.U, Front.O,
}

UNROUNDED_FRONT_VOWELS = {
  Front.E, Front.I,
}

ROUNDED_BACK_VOWELS = {
  Back.U, Back.O,
}

UNROUNDED_BACK_VOWELS = {
  Back.A, Back.I,
}

ROUNDED_VOWELS = (
  ROUNDED_BACK_VOWELS.union(
    ROUNDED_FRONT_VOWELS
  )
)

CONTINUANT_VOICED = {
  'ğ', 'j', 'l', 'm',
  'n', 'r', 'v', 'y',
  'z',
}

NON_CONTINUANT_VOICED = {
  'b', 'c', 'd', 'g',
}

VOICELESS_CONTINUANT = {
  'p', 'ç', 't', 'k',
}

VOICELESS_NON_CONTINUANT = {
  'f', 'h', 's', 'ş',
}

VOICELESS_CONSONANTS = (
  # FISTIKÇI ŞAHAP 👳
  VOICELESS_CONTINUANT.union(
    VOICELESS_NON_CONTINUANT
  )
)

VOICED_CONSONANTS = (
  CONTINUANT_VOICED.union(
    NON_CONTINUANT_VOICED
  )
)

CONSONANTS = (
  VOICED_CONSONANTS.union(
    VOICELESS_CONSONANTS
  )
)

ends_with_consonant = (
  lambda text:
    text[-1] in CONSONANTS
)

ends_with_voiceless = (
  lambda text:
    text[-1] in VOICELESS_CONSONANTS
)

SOFTENING_SOUNDS = {
  'p': 'b',
  'ç': 'c',
  't': 'd',
  'k': 'ğ',
}

HARDENING_SOUNDS = {
  'p': 'b',
  'ç': 'c',
  't': 'd',
  'k': 'ğ',
}

def get_vowel_symbol(vowel):
  for member in Front:
    if member.value == vowel:
      return member

  for member in Back:
    if member.value == vowel:
      return member

def get_last_vowel(text):
  for symbol in reversed(text):
    if symbol in enum_values(Front):
      return symbol

    if symbol in enum_values(Back):
      return symbol

  raise MissingVowelSound

def determine_vowel_harmony(text):
  for sound in reversed(text):
    if sound in enum_values(Front):
      return Front

    if sound in enum_values(Back):
      return Back

  raise MissingVowelSound

def is_front(text):
  return determine_vowel_harmony(text) is Front

def is_back(text):
  return determine_vowel_harmony(text) is Back

def is_rounded(text):
  return get_vowel_symbol(get_last_vowel(text)) in ROUNDED_VOWELS

def harmony(sound):
  for (vowels, affix) in (
    (UNROUNDED_BACK_VOWELS, Back.I),
    (UNROUNDED_FRONT_VOWELS, Front.I),
    (ROUNDED_BACK_VOWELS, Back.U),
    (ROUNDED_FRONT_VOWELS, Front.U),
  ):
    if sound in vowels:
      break
  return affix

def swap_front_and_back(text):
  '''
  #### swap_front_and_back
  Swaps front sounds to back, and vice versa

  ```python
  >>> swap_front_and_back('acak')
  'ecek'

  >>> swap_front_and_back('ocok')
  'öcök'

  >>> swap_front_and_back('öcök')
  'ocok'

  >>> swap_front_and_back('acak')
  'ecek'

  ```
  '''
  symbols = []

  if is_front(text):
    vowel_set = [Front, Back]
  else:
    vowel_set = [Back, Front]

  for symbol in text:
    try:
      determine_vowel_harmony(symbol)

    except MissingVowelSound:
      new = symbol

    else:
      for (vowel, to_replace) in zip(*vowel_set):
        if vowel.value == symbol:
          new = to_replace.value
          break

    finally:
      symbols.append(new)

  return join(*symbols)

def voice(text):
  '''
  ## Voicing or sonorization (yumuşama in turkish)
  to make pronouncation easier, nouns ending
  with these sounds.

  ```
  ⟨p⟩ ⟨ç⟩ ⟨t⟩ ⟨k⟩ 
  ```

  may be softened by replacing them in order:

  ```
  ⟨b⟩ ⟨c⟩ ⟨d⟩ ⟨ğ⟩
  ```

  ✎︎ examples
  ```
  ço⟨p⟩un → ço⟨b⟩un
  ağa⟨ç⟩ın → ağa⟨c⟩ın
  kağı⟨t⟩ın → kağı⟨d⟩ın 
  ren⟨k⟩in → ren⟨g⟩in
  ```

  ✎︎ examples in other languages
  ```
  li⟨f⟩e → li⟨v⟩e
  stri⟨f⟩e → stri⟨v⟩e
  proo⟨f⟩ → pro⟨v⟩e
  ```
  '''
  for sound, softened in SOFTENING_SOUNDS.items():
    if text.endswith(sound):
      return join(text[:-1], softened)

  return text

def devoice(text):
  '''
  ## Devoicing or desonorization (sertleşme in turkish)
  to make pronouncation easier, nouns ending with
  these sounds:
  ```
  ⟨p⟩ ⟨ç⟩ ⟨t⟩ ⟨k⟩
  ```
  
  may be hardened by replacing them in order:
  ```
  ⟨b⟩ ⟨c⟩ ⟨d⟩ ⟨ğ⟩
  ```

  ✎︎ examples
  ```
  ço⟨p⟩un → ço⟨b⟩un
  ağa⟨ç⟩ın → ağa⟨c⟩ın
  kağı⟨t⟩ın → kağı⟨d⟩ın 
  ren⟨k⟩in → ren⟨g⟩in
  ```

  ✎︎ examples in other languages
  ```
  dogs → dogs ([ɡz])
  missed → missed ([st])
  whizzed → whizzed ([zd])
  prośba → prɔʑba
  просьба → prozʲbə
  ```
  '''
  for sound, softened in SOFTENING_SOUNDS.items():
    if text.endswith(sound):
      return join(text[:-1], softened)

  return text
