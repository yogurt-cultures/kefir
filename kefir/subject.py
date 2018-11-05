'''
# Turkish Predication and Copula (Yüklemler)

Turkish language copulas, which are called as ek-eylem which
literally means 'suffix-verb' are one of the most distinct
features of turkish grammar.

## Grammatical Cases

Implemented only six grammatical cases.

  - Nominative (Yalın hal)
  - Genitive (ilgi eki, -ın -in, un, ün)
  - Dative (yer tamlayıcıları -da, de, ta, te)
  - Accusative (-i, dolaylı)
  - Ablative
  - Locative
  - Possesive

Turkish has 9 more cases (will be somehow implemented in future).

  - Essive
  - Instrumental
  - Inclusive
  - Abessive
  - Likeness
  - Coverage
  - Qualitative
  - Conditional

  Detailed explaination:
  https://en.wikibooks.org/wiki/Turkish/Cases

'''
from enum import Enum
from .phonology import is_front, is_back
from .suffix import Suffix
from .functional import join, NOTHING, is_truthy, skip_falsy_and_join
from .phonology import (get_last_vowel,
                        get_vowel_symbol,
                        Front,
                        Back,
                        is_back,
                        voice,
                        is_front,
                        ends_with_consonant,
                        harmony,
                        SOFTENING_SOUNDS,
                        VOICELESS_CONSONANTS,
                        UNROUNDED_BACK_VOWELS,
                        ROUNDED_BACK_VOWELS,
                        UNROUNDED_FRONT_VOWELS,
                        ROUNDED_FRONT_VOWELS)
from .predication import Person

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
  ## nominative case (yalın in turkish)
  the simplest grammatical case, there's no suffix to
  affix in that case.

  nominative comes from latin cāsus nominātīvus
  means case for naming.
  '''
  return text

def ablative(text):
  '''
  ## ablative case (ayrılma in turkish)
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
  ## accusative
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
  ## genitive case (genitifler in turkish)
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


def possesive(text,whom,is_plural = False):
  '''
  ## possesive case (iyelik in turkish)
  Creates a relationship of belonging
  between one thing and another.
  It refers nouns to people, countries, animals, objects.

  ✎︎ examples
  ```
  Kahvesi (Her coffee)
  Kitabım (My book)
  Evin (Your home)
  Dolabımız (Our wardrobe)
  Yuvanız (Your nest)
  Okulları (Their school)

  ```
  '''

  states = {
      Person.FIRST: "m",
      Person.SECOND: "n",
      Person.THIRD: NOTHING
  }


  last_vowel = get_last_vowel(text)
  symbol = get_vowel_symbol(last_vowel)

  if is_plural and whom == Person.THIRD:
      if is_front(last_vowel):
        symbol = Front.E
        suffix = join("ler", harmony(symbol).value)
      else:
        symbol = Back.A
        suffix = join("lar", harmony(symbol).value)

  elif is_plural:
      suffix = join(states[whom],harmony(symbol).value, Suffix.Z)
  else:
      suffix = states[whom]

  if ends_with_consonant(text):
    if whom == Person.THIRD and is_plural:
      return join(text, suffix)
    else:
      return join(voice(text), harmony(symbol).value, suffix)

  else:
    if whom == Person.THIRD and is_plural:
        return join(voice(text), suffix)
    elif whom == Person.THIRD and is_plural == False:
        return join(voice(text), Suffix.S, harmony(symbol).value)
    else:
        return join(voice(text), suffix)

def dative(text):
  '''
  ## dative case (yönelme in turkish)
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
  ## locative case (bulunma in turkish)
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

def subject(
  stem,
  is_plural=False,
  case=GrammaticalCase.NOMINATIVE,
):
  if is_plural:
    suffix = \
      Suffix.LER if is_front(stem) else Suffix.LAR
  else:
    suffix = NOTHING

  processor = get_case_processor(case)
  return processor(join(stem, suffix))
