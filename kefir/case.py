'''
# Turkish Grammar / Grammatical Cases
==========================================================

Implemented only six grammatical cases.

  - Nominative
  - Genitive
  - Dative
  - Accusative
  - Ablative
  - Locative

Turkish has 9 more cases.

  - Essive
  - Instrumental
  - Inclusive
  - Abessive
  - Likeness
  - Coverage
  - Qualitative
  - Conditional
  - Possesive

  Detailed explaination:
  https://en.wikibooks.org/wiki/Turkish/Cases

TODO: Enum'lardaki rakamlar yerine auto() kullanılmalı.
'''
from enum import Enum

from .functional import join, is_truthy, skip_falsy_and_join
from .suffix import Suffix

from .phonology import (get_last_vowel,
                        get_vowel_symbol,
                        Front,
                        Back,
                        is_back,
                        voice,
                        is_front,
                        ends_with_consonant,
                        SOFTENING_SOUNDS,
                        VOICELESS_CONSONANTS,
                        UNROUNDED_BACK_VOWELS,
                        ROUNDED_BACK_VOWELS,
                        UNROUNDED_FRONT_VOWELS,
                        ROUNDED_FRONT_VOWELS)

class GrammaticalCase(Enum):
  NOMINATIVE = 1
  GENITIVE = 2
  DATIVE = 3
  ACCUSATIVE = 4
  ABLATIVE = 5
  LOCATIVE = 6

def get_case_processor(case):
  return {
    GrammaticalCase.NOMINATIVE: nominative,
    GrammaticalCase.ABLATIVE: ablative,
    GrammaticalCase.ACCUSATIVE: accusative,
    GrammaticalCase.GENITIVE: genitive,
    GrammaticalCase.DATIVE: dative,
    GrammaticalCase.LOCATIVE: locative,
  }.get(case)

def nominative(text):
  '''
  nominative case (yalın in turkish)
  ----------------------------------
  the simplest grammatical case, there's no suffix to
  affix in that case.

  nominative comes from latin cāsus nominātīvus 
  means case for naming.
  '''
  return text

def ablative(text):
  '''
  ablative case (ayrılma in turkish)
  -den, -dan, -ten or -tan
  --------------------------------------------------------
  a grammatical case for nouns, pronouns and adjectives in
  the grammar of various languages; it is sometimes used to
  express motion away from something, among other uses.

  ✎︎ examples
  ```
  adalar[dan] geldim
  merkez[den] geçtim
  teyit[ten] geçtim
  açlık[tan] öldüm
  ```
  '''
  [*head, endswith] = text

  if endswith in VOICELESS_CONSONANTS:
    suffix = Suffix.TAN if is_back(text) else Suffix.TEN
  else:
    suffix = Suffix.DAN if is_back(text) else Suffix.DEN

  return join(*head, endswith, suffix)

def accusative(text, voicer=voice):
  '''
  accusative (ilgi in turkish)
  -ı, -i, -u, or -ü
  --------------------------------------------------------
  The accusative case (abbreviated acc) of a noun is the
  grammatical case used to mark the direct object of a
  transitive verb. The same case is used in many
  languages for the objects of (some or all) prepositions. 

  ✎︎ examples
  ```
  aday[ı] yedim
  evim[i] yaptım
  üzüm[ü] pişirdim
  ```
  '''
  last_vowel = get_last_vowel(text)
  sound = get_vowel_symbol(last_vowel)

  for (vowels, affix) in (
    (UNROUNDED_BACK_VOWELS, Back.I),
    (UNROUNDED_FRONT_VOWELS, Front.I),
    (ROUNDED_BACK_VOWELS, Back.U),
    (ROUNDED_FRONT_VOWELS, Front.U),
  ):
    if sound in vowels:
      break

  return skip_falsy_and_join(
    voicer(text),
    # if ends with a vowel, echo the genitive 
    # sound ⟨n⟩ right before the voiced suffix
    #not ends_with_consonant(text) and Suffix.Y,
    affix.value,
  )

def genitive(text):
  '''
  genitive case (genitifler in turkish)
  -nın, -nin, -nun, or -nün
  -----------------------------------------------------
  In grammar, the genitive is the grammatical case
  that marks a word, usually a noun, as modifying
  another word, also usually a noun.

  ✎︎ examples
  ```
  hanımelinin çiçeği (flower of a plant called hanımeli)
  kadının ayakkabısı (shoes of the woman)
  باب بيت bābu baytin (the door of a house)
  mari[i] nie ma w domu (maria is not at home)
  ```
  '''
  last_vowel = get_last_vowel(text)
  sound = get_vowel_symbol(last_vowel)

  for (vowels, affix) in (
    (UNROUNDED_BACK_VOWELS, Back.I),
    (UNROUNDED_FRONT_VOWELS, Front.I),
    (ROUNDED_BACK_VOWELS, Back.U),
    (ROUNDED_FRONT_VOWELS, Front.U),
  ):
    if sound in vowels:
      break

  return skip_falsy_and_join(
    # nominative form
    voice(text),

    # if ends with a vowel, echo the genitive 
    # sound ⟨n⟩ right before the voiced suffix
    not ends_with_consonant(text)
    and Suffix.N,

    # ⟨a⟩ ⟨i⟩ ⟨u⟩ ⟨ü⟩
    affix.value,

    # genitive sound ⟨n⟩
    Suffix.N,
  )

def dative(text):
  '''
  going-towards case (yönelme in turkish)
  -e, -a
  -----------------------------------------------------
  In some languages, the dative is used to mark the
  indirect object of a sentence.

  ✎︎ examples
  ```
  marya yakup'a bir drink verdi (maria gave jacob a drink)
  maria jacobī potum dedit (maria gave jacob a drink)
  ```
  '''
  last_vowel = get_last_vowel(text)
  sound = get_vowel_symbol(last_vowel)

  if is_front(last_vowel):
    symbol = Front.E
  else:
    symbol = Back.A

  return skip_falsy_and_join(
    # nominative form
    voice(text),

    # if ends with a vowel, echo the genitive 
    # sound ⟨n⟩ right before the voiced suffix
    not ends_with_consonant(text) and Suffix.Y,

    # ⟨e⟩ ⟨a⟩
    symbol.value,
  )

def locative(text):
  '''
  locative case (bulunma in turkish)
  -de, -da
  -----------------------------------------------------
  Locative is a grammatical case which indicates a location.
  It corresponds vaguely to the English prepositions "in",
  "on", "at", and "by". 

  ✎︎ examples
  ```
  bahçe[de] hanımeli var.
  yorum[da] iyi beatler var.
  kalem[de] güzel uç var.
  ```
  '''
  last_vowel = get_last_vowel(text)
  sound = get_vowel_symbol(last_vowel)

  if is_front(last_vowel):
    symbol = Front.E
  else:
    symbol = Back.A

  return skip_falsy_and_join(
    text,

    # ⟨d⟩ or ⟨t⟩
    Suffix.T if text[-1] in SOFTENING_SOUNDS else Suffix.D,

    # ⟨e⟩ or ⟨a⟩
    symbol.value,
  )
