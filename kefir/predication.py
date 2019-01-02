'''
# Turkish Predication and Copula (Yüklemler)

turkish language copulas, which are called as ek-eylem which
literally means 'suffix-verb' are one of the most distinct
features of turkish grammar.
'''
from enum import Enum

from .functional import (join,
                         is_truthy,
                         skip_falsy_and_join,
                         NOTHING,
                         identity,
                         get_enum_member)
from .suffix import Suffix
from .phonology import (get_last_vowel,
                        get_vowel_symbol,
                        Back,
                        Front,
                        is_front,
                        is_back,
                        is_rounded,
                        voice,
                        devoice,
                        ends_with_consonant,
                        ends_with_voiceless,
                        UNROUNDED_BACK_VOWELS,
                        ROUNDED_BACK_VOWELS,
                        UNROUNDED_FRONT_VOWELS,
                        ROUNDED_FRONT_VOWELS,
                        harmony,
                        swap_front_and_back)

class Person(Enum):
  FIRST = 'first'
  SECOND = 'second'
  THIRD = 'third'

class Copula(Enum):
  NEGATIVE = 'negative'
  ZERO = 'zero'
  TOBE = 'tobe'
  PERSONAL = 'personal'
  PERFECTIVE = 'perfective'
  IMPERFECTIVE = 'imperfective'
  PROGRESSIVE = 'progressive'
  NECESSITATIVE = 'necessitative'
  FUTURE = 'future'
  IMPOTENTIAL = 'impotential'
  CONDITIONAL = 'conditional'

def get_copula_processor(copula):
  return {
    Copula.NEGATIVE: negative,
    Copula.ZERO: zero,
    Copula.TOBE: tobe,
    Copula.PERSONAL: personal,
    Copula.PERFECTIVE: perfective,
    Copula.IMPERFECTIVE: imperfective,
    Copula.PROGRESSIVE: progressive,
    Copula.NECESSITATIVE: necessitative,
    Copula.FUTURE: future,
    Copula.IMPOTENTIAL: impotential,
    Copula.CONDITIONAL: conditional,
  }.get(copula)

def zero(predicate, person=Person.THIRD, is_plural=False):
  '''
  #### zero copula
  is the rule for third person, as in hungarian
  and russian. that means two nouns, or a noun and an
  adjective can be juxtaposed to make a sentence without
  using any copula. third person plural might be indicated
  with the use of plural suffix "-lar/-ler". 

  ✎︎ examples
  ```
  yogurt kültür (yogurt [is-a] culture)
  abbas yolcu (abbas [is-a] traveller)
  evlerinin önü yonca (the front of their home [is-a] plant called yonca)
  ```

  ✎︎ tests
  ```python
  >>> zero('yolcu')
  'yolcu'

  >>> zero('umut')
  'umut'

 ```
  '''
  return predicate

def negative(
  predicate,
  person=Person.THIRD,
  is_plural=False,
  delimiter=Suffix.DELIMITER,
):
  '''
  #### negative
  negation is indicated by the negative copula değil. 
  değil is never used as a suffix, but it takes suffixes
  according to context. 

  ✎︎ examples
  ```
  yogurt kültür değildir (yogurt [is-not-a] culture)
  abbas yolcu değildir (abbas [is-not-a] traveller)
  evlerinin önü yonca değildir (the front of their home [is-not-a] yonca)
  ```

  ✎︎ tests
  ```python
  >>> negative('yolcu')
  'yolcu değil'

  ```
  '''
  return join(predicate, delimiter, Suffix.NEGATIVE)

def tobe(
  predicate,
  person=Person.THIRD,
  is_plural=False,
):
  '''
  ### tobe
  turkish "to be" as regular/auxiliary verb (olmak).

  ✎︎ examples
  ```
  yogurt kültürdür (yogurt [is] culture)
  abbas yolcudur (abbas [is] traveller)
  evlerinin önü yoncadır (the front of their home [is] plant called yonca)
  ```

  ✎︎ tests
  ```python
  >>> tobe('yolcu')
  'yolcudur'
  >>> tobe('üzüm')
  'üzümdür'
  >>> tobe('yonca')
  'yoncadır'

  ```
  '''
  last_vowel = get_last_vowel(predicate)
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
    predicate,
    Suffix.D,
    affix.value,
    Suffix.R,
  )

def personal(predicate, whom=Person.THIRD, is_plural=False):
  '''
  ### personification copula

  ✎︎ examples
  ```
  ben buralıyım (i'm from here)
  sen oralısın (you're from over there)
  aynı gezegenliyiz (we're from same planet)
  ```

  ✎︎ tests
  ```python
  >>> personal('uçak', Person.FIRST, is_plural=False)
  'uçağım'

  >>> personal('oralı', Person.SECOND, is_plural=False)
  'oralısın'

  >>> personal('gezegenli', Person.FIRST, is_plural=True)
  'gezegenliyiz'

  ```
  '''
  return impersonate(predicate, whom, is_plural, in_past=False)

def inferential(predicate, whom=Person.THIRD, is_plural=False):
  '''
  ### inferential mood (-miş in turkish)
  it is used to convey information about events
  which were not directly observed or were inferred by the speaker. 

  ✎︎ examples
  ```
  elmaymışım (i was an apple as i've heard)
  üzülmüşsün (you were sad as i've heard)
  doktormuş (he/she/it was a doctor as i've heard)
  üzümmüşsün (you were a grape as i've heard)
  ```

  ✎︎ tests
  ```python
  >>> inferential('öğretmen', Person.SECOND, is_plural=False)
  'öğretmenmişsin'

  >>> inferential('üzül', Person.SECOND, is_plural=False)
  'üzülmüşsün'

  >>> inferential('robot', Person.FIRST, is_plural=False)
  'robotmuşum'

  >>> inferential('robot', Person.THIRD, is_plural=False)
  'robotmuş'

  >>> inferential('ada', Person.THIRD, is_plural=False)
  'adaymış'

  ```
  '''
  last_vowel = get_last_vowel(predicate)
  sound = get_vowel_symbol(last_vowel)

  inference_suffix = join(
    'm',
    harmony(
      get_vowel_symbol(
        get_last_vowel(
          predicate))).value,
    'ş'
  )

  return skip_falsy_and_join(
    predicate,

    # combinative consontant ⟨y⟩
    not ends_with_consonant(predicate) and Suffix.Y,

    impersonate(inference_suffix, whom, is_plural),
  )

def conditional(predicate, whom=Person.THIRD, is_plural=False):
  '''
  ### conditional mood (-isem in turkish)
  It is a grammatical mood used to express a proposition whose
  validity is dependent on some condition, possibly counterfactual.

  ✎︎ examples
  ```
  elmaysam (if i am an apple)
  üzümsen (if you are a grape)
  bıçaklarsa (if they are a knife)
  ```

  ✎︎ tests
  ```python
  >>> conditional('elma', Person.FIRST, is_plural=False)
  'elmaysam'
  >>> conditional('üzüm', Person.SECOND, is_plural=False)
  'üzümsen'
  >>> conditional('bıçak', Person.THIRD, is_plural=True)
  'bıçaklarsa'

  ```
  '''
  last_vowel = get_last_vowel(predicate)
  sound = get_vowel_symbol(last_vowel)

  condition_suffix = Suffix.SE if is_front(predicate) else Suffix.SA

  for (to_whom, plurality, personification) in (
    (Person.FIRST, False, Suffix.M),
    (Person.SECOND, False, Suffix.N),
    (Person.THIRD, False, NOTHING),
    (Person.FIRST, True, Suffix.K),
    (Person.SECOND, True, Suffix.NIZ),
    (Person.THIRD, True, NOTHING),
  ):
    if to_whom == whom and plurality == is_plural:
      break

  return skip_falsy_and_join(
    predicate,

    # plural suffix for 3rd person
    whom == Person.THIRD
    and is_plural
    and (Suffix.LER if is_front(predicate) else Suffix.LAR),

    # combinative consontant ⟨y⟩
    not ends_with_consonant(predicate)
    and Suffix.Y,

    condition_suffix,
    personification,
  )

def perfective(predicate, whom=Person.THIRD, is_plural=False):
  '''
  ### alethic modality (-idi in turkish)
  linguistic modality that indicates modalities of truth,
  in particular the modalities of logical necessity,
  possibility or impossibility.

  ✎︎ examples
  ```
  elmaydım (i was an apple)
  üzümdün (you were a grape)
  doktordu (he/she/it was a doctor)
  ```

  ✎︎ tests
  ```python
  >>> perfective('açık', Person.FIRST, is_plural=False)
  'açıktım'

  >>> perfective('oralı', Person.SECOND, is_plural=False)
  'oralıydın'

  >>> perfective('dalda', Person.FIRST, is_plural=False)
  'daldaydım'

  >>> perfective('dalda', Person.THIRD, is_plural=False)
  'daldaydı'

  >>> perfective('dalda', Person.FIRST, is_plural=True)
  'daldaydık'

  >>> perfective('dalda', Person.SECOND, is_plural=True)
  'daldaydınız'

  >>> perfective('dalda', Person.THIRD, is_plural=True)
  'daldaydılar'

  >>> perfective('gezegende', Person.THIRD, is_plural=True)
  'gezegendeydiler'

  ```
  '''
  return impersonate(predicate, whom, is_plural, in_past=True)

def imperfective(predicate, whom=Person.THIRD, is_plural=False):
  '''
  ### the imperfective (-iyor in turkish)
  grammatical aspect used to describe a situation viewed with interior composition. 
  describes ongoing, habitual, repeated, or similar semantic roles, 
  whether that situation occurs in the past, present, or future.

  ✎︎ examples
  ```
  gidiyorum (i'm going)
  kayıyor (he's skating)
  üzümlüyor (he's graping)
  ```

  ✎︎ tests
  ```python
  >>> imperfective('açı', Person.FIRST, is_plural=False)
  'açıyorum'

  >>> imperfective('açık', Person.FIRST, is_plural=False)
  'açıkıyorum'

  >>> imperfective('oralı', Person.SECOND, is_plural=False)
  'oralıyorsun'

  >>> imperfective('dal', Person.THIRD, is_plural=False)
  'dalıyor'

  >>> imperfective('dal', Person.FIRST, is_plural=True)
  'dalıyoruz'

  >>> imperfective('dal', Person.FIRST, is_plural=True)
  'dalıyoruz'

  >>> imperfective('dal', Person.SECOND, is_plural=True)
  'dalıyorsunuz'

  >>> imperfective('dal', Person.THIRD, is_plural=True)
  'dalıyorlar'

  ```
  '''
  imperfect_copula = skip_falsy_and_join(
    ends_with_consonant(predicate) and harmony(
      get_vowel_symbol(
        get_last_vowel(
          predicate))).value,
    Suffix.IMPERFECT,
  )

  return join(
    predicate,
    impersonate(imperfect_copula, whom, is_plural, in_past=False)
  )

def future(predicate, whom=Person.THIRD, is_plural=False):
  '''
  ### the future tense (-iyor in turkish)
  is a verb form that generally marks the event described by the verb as not
  having happened yet, but expected to happen in the future.

  ✎︎ examples
  ```
  gidecek (he'll go)
  ölecek (he'll die)
  can alacak (he'll kill someone)
  ```

  ✎︎ tests
  ```python
  >>> future('gel', Person.FIRST, is_plural=False)
  'geleceğim'

  >>> future('açık', Person.FIRST, is_plural=False)
  'açıkacağım'

  >>> future('gel', Person.FIRST, is_plural=True)
  'geleceğiz'

  ```
  '''
  future_copula = join(
    predicate,
    Suffix.FUTURE if is_front(predicate) else swap_front_and_back(Suffix.FUTURE),
  )

  return impersonate(future_copula, whom, is_plural, in_past=False)

def progressive(predicate, whom=Person.THIRD, is_plural=False):
  '''
  ### progressive tense

  ✎︎ examples
  gülmekteyim (i am in the process of laughing)
  ölmekteler (they are in the process of dying 👾)

  ✎︎ tests
  ```python
  >>> progressive('gel', Person.FIRST, is_plural=False)
  'gelmekteyim'

  >>> progressive('açık', Person.FIRST, is_plural=False)
  'açıkmaktayım'

  >>> progressive('gel', Person.FIRST, is_plural=True)
  'gelmekteyiz'

  ```
  '''
  progressive_copula = join(
    predicate,
    Suffix.PROGRESSIVE
      if is_front(predicate)
      else swap_front_and_back(Suffix.PROGRESSIVE),
  )

  return impersonate(progressive_copula, whom, is_plural, in_past=False)

def necessitative(predicate, whom=Person.THIRD, is_plural=False):
  '''
  ### necessitative copula

  ✎︎ examples
  ```
  gitmeliyim (i must go)
  kaçmalıyım (i must run away)
  ```

  ✎︎ tests
  ```python
  >>> necessitative('git', Person.FIRST, is_plural=False)
  'gitmeliyim'

  >>> necessitative('açık', Person.FIRST, is_plural=False)
  'açıkmalıyım'

  >>> necessitative('uza', Person.FIRST, is_plural=True)
  'uzamalıyız'

  ```
  '''
  progressive_copula = join(
    predicate,
    Suffix.NECESSITY
      if is_front(predicate)
      else swap_front_and_back(Suffix.NECESSITY),
  )

  return impersonate(progressive_copula, whom, is_plural, in_past=False)

def impotential(predicate, whom=Person.THIRD, is_plural=False):
  '''
  ### impotential copula

  ✎︎ examples
  ```
  gidemem (i cannot go)
  kaçamayız (we cannot run away)
  ```

  ✎︎ tests
  ```python
  >>> impotential('git', Person.FIRST, is_plural=False)
  'gidemem'

  >>> impotential('git', Person.SECOND, is_plural=False)
  'gidemezsin'

  >>> impotential('git', Person.THIRD, is_plural=False)
  'gidemez'

  >>> impotential('git', Person.FIRST, is_plural=True)
  'gidemeyiz'

  >>> impotential('git', Person.FIRST, is_plural=True)
  'gidemeyiz'

  >>> impotential('git', Person.SECOND, is_plural=True)
  'gidemezsiniz'

  >>> impotential('git', Person.THIRD, is_plural=True)
  'gidemezler'

  >>> impotential('al', Person.THIRD, is_plural=True)
  'alamazlar'

  ```
  '''
  last_vowel = get_last_vowel(predicate)
  sound = get_vowel_symbol(last_vowel)

  if is_back(predicate):
    impotential_copula = swap_front_and_back(Suffix.IMPOTENTIAL)
    plurality = Suffix.LAR
  else:
    impotential_copula = Suffix.IMPOTENTIAL
    plurality = Suffix.LER

  for (to_whom, plurality, personification) in (
    (Person.FIRST, False, Suffix.M),
    (Person.SECOND, False, Suffix.Z + Suffix.SIN),
    (Person.THIRD, False, Suffix.Z),
    (Person.FIRST, True, Suffix.Y + Suffix.IZ),
    (Person.SECOND, True, Suffix.Z + Suffix.SIN + Suffix.IZ),
    (Person.THIRD, True, Suffix.Z + plurality),
  ):
    if to_whom == whom and plurality == is_plural:
      break

  return skip_falsy_and_join(
    voice(predicate),

    # combinative consontant ⟨y⟩
    not ends_with_consonant(predicate)
    and Suffix.Y,

    impotential_copula,
    personification,
  )

def first_person_singular(text, in_past=False):
  return skip_falsy_and_join(
    # last vowel should not be voiced in alethic modality
    text if in_past else voice(text),

    # combinative consontant ⟨y⟩
    not ends_with_consonant(text) and Suffix.Y,

    # ⟨d⟩ or ⟨t⟩
    in_past and (Suffix.T if ends_with_voiceless(text) else Suffix.D),

    # ⟨a⟩ ⟨i⟩ ⟨u⟩ ⟨ü⟩
    harmony(
      get_vowel_symbol(
        get_last_vowel(
          text))).value,
    Suffix.M,
  )

def second_person_singular(text, in_past=False):
  return skip_falsy_and_join(
    text,

    # combinative consontant ⟨y⟩
    in_past and not ends_with_consonant(text) and Suffix.Y,

    # ⟨d⟩ or ⟨t⟩
    in_past and (Suffix.T if ends_with_voiceless(text) else Suffix.D),

    # sound ⟨s⟩ in present time
    not in_past and Suffix.S,

    harmony( # ⟨a⟩ ⟨i⟩ ⟨u⟩ ⟨ü⟩
      get_vowel_symbol(
        get_last_vowel(
          text))).value,

    Suffix.N,
  )


def third_person_singular(text, in_past=False):
  return skip_falsy_and_join(
    text,

    # combinative consontant ⟨y⟩
    not ends_with_consonant(text) and Suffix.Y,

    # add ⟨t⟩ or ⟨d⟩ for alethic modality
    in_past and (Suffix.T if ends_with_voiceless(text) else Suffix.D),

    in_past and harmony( # ⟨a⟩ ⟨i⟩ ⟨u⟩ ⟨ü⟩
      get_vowel_symbol(
        get_last_vowel(
          text)
        )
      ).value,
  )

def first_person_plural(text, in_past=False):
  return skip_falsy_and_join(
    # last vowel should not be voiced in alethic modality
    text if in_past else voice(text),

    # combinative consontant ⟨y⟩
    not ends_with_consonant(text) and Suffix.Y,

    # ⟨d⟩ or ⟨t⟩
    in_past and (Suffix.T if ends_with_voiceless(text) else Suffix.D),

    # ⟨a⟩ ⟨i⟩ ⟨u⟩ ⟨ü⟩
    harmony(
      get_vowel_symbol(
        get_last_vowel(
          text))).value,

    Suffix.K if in_past else Suffix.Z
  )

def second_person_plural(text, in_past=False):
  return skip_falsy_and_join (
    second_person_singular(text, in_past),

    # ⟨a⟩ ⟨i⟩ ⟨u⟩ ⟨ü⟩
    harmony(
      get_vowel_symbol(
        get_last_vowel(
          text))).value,

    Suffix.Z,
  )

def third_person_plural(text, in_past=False):
  return skip_falsy_and_join(
    third_person_singular(text, in_past),

    # -lar or -ler, plural affix
    Suffix.LER if is_front(text) else Suffix.LAR
  )

def impersonate(text, to_whom, is_plural, in_past=False):
  for (person, plurality, processor) in (
    (Person.FIRST, False, first_person_singular),
    (Person.SECOND, False, second_person_singular),
    (Person.THIRD, False, third_person_singular),
    (Person.FIRST, True, first_person_plural),
    (Person.SECOND, True, second_person_plural),
    (Person.THIRD, True, third_person_plural),
  ):
    if person == to_whom \
      and is_plural == plurality:
      return processor(text, in_past)

def combinator(copula, text, whom=Person.THIRD, is_plural=False):
  try:
    for i in copula:
      text = predicate(text, whom, i, is_plural)
  except TypeError:
    raise Exception(
      'invalid copula. options: %s' % copula
    )

  return text

def predicate(
  text,
  person=Person.THIRD,
  copula=Copula.ZERO,
  is_plural=False,
):
  if isinstance(person, str):
    person = get_enum_member(Person, person)
  if isinstance(copula, str):
    copula = get_enum_member(Copula, copula)
  elif isinstance(copula, tuple):
    return combinator(copula, text, person, is_plural)
  
  try:
    processor = get_copula_processor(copula)
  except TypeError:
    raise Exception(
      'invalid copula. options: %s' % Copula
    )

  return processor(text, person, is_plural)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
