"""
Turkish Grammar / Turkish predication and copula
-----------------------------------------------------------------
turkish language copulas, which are called as ek-eylem which
literally means 'suffix-verb' are one of the most distinct
features of turkish grammar.

TODO: Remove unused imports.
"""
from enum import Enum, auto

from .functional import join, is_truthy, skip_falsy_and_join, NOTHING, identity
from .suffix import Suffix
from .case import accusative
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
  FIRST = auto()
  SECOND = auto()
  THIRD = auto()

class Copula(Enum):
  NEGATIVE = -1
  ZERO = 0
  TOBE = 1
  PERSONAL = 2
  PERFECT = 3
  IMPERFECT = 4
  PROGRESSIVE = 5
  NECESSITATIVE = 6
  FUTURE = 7
  IMPOTENTIAL = 8

def get_copula_processor(copula):
  return {
    Copula.NEGATIVE: negative,
    Copula.ZERO: zero,
    Copula.TOBE: tobe,
    Copula.PERSONAL: personal,
    Copula.PERFECT: past,
  }.get(copula)

def zero(subject, predicate, delimiter):
  """
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
  >>> zero('abbas', 'yolcu', '-')
  'abbas-yolcu'

  ```
  """
  return join(subject, delimiter, predicate)

def negative(subject, predicate, delimiter):
  """
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
  >>> negative('abbas', 'yolcu', '-')
  'abbas-yolcu-değil'

  ```
  """
  return join(subject, delimiter, predicate, delimiter, Suffix.NEGATIVE)

def tobe(subject, predicate, delimiter):
  """
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
  >>> tobe('abbas', 'yolcu', '-')
  'abbas-yolcudur'

  >>> tobe('abbas', 'üzüm', '-')
  'abbas-üzümdür'

  >>> tobe('evlerinin-önü', 'yonca', '-')
  'evlerinin-önü-yoncadır'

  ```
  """
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

  parts = (
    predicate,
    Suffix.D,
    affix.value,
    Suffix.R,
  )

  return join(
    subject,
    delimiter,
    join(*filter(is_truthy, parts))
  )

def personal(subject, predicate, delimiter, whom=Person.THIRD, is_plural=False):
  """
  ### personification copula

  ✎︎ examples
  ```
  ben buralıyım (i'm from here)
  sen oralısın (you're from over there)
  aynı gezegenliyiz (we're from same planet)
  ```

  ✎︎ tests
  ```python
  >>> personal('ben', 'uçak', '-', Person.FIRST, is_plural=False)
  'ben-uçağım'

  >>> personal('sen', 'oralı', '-', Person.SECOND, is_plural=False)
  'sen-oralısın'

  >>> personal('aynı', 'gezegenli', '-', Person.FIRST, is_plural=True)
  'aynı-gezegenliyiz'

  ```
  """
  return join(
    subject,
    delimiter,
    impersonate(predicate, whom, is_plural, in_past=False)
  )

def inferential(subject, predicate, delimiter, whom=Person.THIRD, is_plural=False):
  """
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
  >>> inferential('sen', 'öğretmen', ' ', Person.SECOND, is_plural=False)
  'sen öğretmenmişsin'

  >>> inferential('sen', 'üzül', ' ', Person.SECOND, is_plural=False)
  'sen üzülmüşsün'

  >>> inferential('ben', 'robot', ' ', Person.FIRST, is_plural=False)
  'ben robotmuşum'

  >>> inferential('o', 'robot', ' ', Person.THIRD, is_plural=False)
  'o robotmuş'

  >>> inferential('o', 'ada', ' ', Person.THIRD, is_plural=False)
  'o adaymış'

  ```
  """
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
    subject,
    delimiter,
    predicate,

    # combinative consontant ⟨y⟩
    not ends_with_consonant(predicate) and Suffix.Y,

    impersonate(inference_suffix, whom, is_plural),
  )

def conditional(subject, predicate, delimiter, whom=Person.THIRD, is_plural=False):
  """
  ### inferential mood (-isem in turkish)
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
  >>> conditional('ben', 'elma', '-', Person.FIRST, is_plural=False)
  'ben-elmaysam'
  >>> conditional('sen', 'üzüm', '-', Person.SECOND, is_plural=False)
  'sen-üzümsen'
  >>> conditional('onlar', 'bıçak', '-', Person.THIRD, is_plural=True)
  'onlar-bıçaklarsa'

  ```
  """
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
    subject,
    delimiter,
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

def perfective(subject, predicate, delimiter, whom=Person.THIRD, is_plural=False):
  """
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
  >>> perfective('men', 'açık', '-', Person.FIRST, is_plural=False)
  'men-açıktım'

  >>> perfective('sen', 'oralı', '-', Person.SECOND, is_plural=False)
  'sen-oralıydın'

  >>> perfective('aynı', 'dalda', '-', Person.FIRST, is_plural=False)
  'aynı-daldaydım'

  >>> perfective('aynı', 'dalda', '-', Person.THIRD, is_plural=False)
  'aynı-daldaydı'

  >>> perfective('aynı', 'dalda', '-', Person.FIRST, is_plural=True)
  'aynı-daldaydık'

  >>> perfective('aynı', 'dalda', '-', Person.SECOND, is_plural=True)
  'aynı-daldaydınız'

  >>> perfective('aynı', 'dalda', '-', Person.THIRD, is_plural=True)
  'aynı-daldaydılar'

  >>> perfective('aynı', 'gezegende', '-', Person.THIRD, is_plural=True)
  'aynı-gezegendeydiler'

  ```
  """
  return join(
    subject,
    delimiter,
    impersonate(predicate, whom, is_plural, in_past=True)
  )

def imperfective(subject, predicate, delimiter, whom=Person.THIRD, is_plural=False):
  """
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
  >>> imperfective('men', 'açı', '-', Person.FIRST, is_plural=False)
  'men-açıyorum'

  >>> imperfective('men', 'açık', '-', Person.FIRST, is_plural=False)
  'men-açıkıyorum'

  >>> imperfective('sen', 'oralı', '-', Person.SECOND, is_plural=False)
  'sen-oralıyorsun'

  >>> imperfective('aynı', 'dal', '-', Person.THIRD, is_plural=False)
  'aynı-dalıyor'

  >>> imperfective('aynı', 'dal', '-', Person.FIRST, is_plural=True)
  'aynı-dalıyoruz'

  >>> imperfective('aynı', 'dal', '-', Person.FIRST, is_plural=True)
  'aynı-dalıyoruz'

  >>> imperfective('aynı', 'dal', '-', Person.SECOND, is_plural=True)
  'aynı-dalıyorsunuz'

  >>> imperfective('aynı', 'dal', '-', Person.THIRD, is_plural=True)
  'aynı-dalıyorlar'

  ```
  """
  imperfect_copula = skip_falsy_and_join(
    ends_with_consonant(predicate) and harmony(
      get_vowel_symbol(
        get_last_vowel(
          predicate))).value,
    Suffix.IMPERFECT,
  )

  return join(
    subject,
    delimiter,
    predicate,
    impersonate(imperfect_copula, whom, is_plural, in_past=False)
  )

def future(subject, predicate, delimiter, whom=Person.THIRD, is_plural=False):
  """
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
  >>> future('men', 'gel', '-', Person.FIRST, is_plural=False)
  'men-geleceğim'

  >>> future('men', 'açık', '-', Person.FIRST, is_plural=False)
  'men-açıkacağım'

  >>> future('biz', 'gel', '-', Person.FIRST, is_plural=True)
  'biz-geleceğiz'

  ```
  """
  future_copula = join(
    predicate,
    Suffix.FUTURE if is_front(predicate) else swap_front_and_back(Suffix.FUTURE),
  )

  return join(
    subject,
    delimiter,
    impersonate(future_copula, whom, is_plural, in_past=False)
  )

def progressive(subject, predicate, delimiter, whom=Person.THIRD, is_plural=False):
  """
  ### progressive tense

  ✎︎ examples
  gülmekteyim (i am in the process of laughing)
  ölmekteler (they are in the process of dying 👾)

  ✎︎ tests
  ```python
  >>> progressive('men', 'gel', '-', Person.FIRST, is_plural=False)
  'men-gelmekteyim'

  >>> progressive('men', 'açık', '-', Person.FIRST, is_plural=False)
  'men-açıkmaktayım'

  >>> progressive('biz', 'gel', '-', Person.FIRST, is_plural=True)
  'biz-gelmekteyiz'

  ```
  """
  progressive_copula = join(
    predicate,
    Suffix.PROGRESSIVE
      if is_front(predicate)
      else swap_front_and_back(Suffix.PROGRESSIVE),
  )

  return join(
    subject,
    delimiter,
    impersonate(progressive_copula, whom, is_plural, in_past=False)
  )

def necessitative(subject, predicate, delimiter, whom=Person.THIRD, is_plural=False):
  """
  ### necessitative copula

  ✎︎ examples
  ```
  gitmeliyim (i must go)
  kaçmalıyım (i must run away)
  ```

  ✎︎ tests
  ```python
  >>> necessitative('men', 'git', '-', Person.FIRST, is_plural=False)
  'men-gitmeliyim'

  >>> necessitative('men', 'açık', '-', Person.FIRST, is_plural=False)
  'men-açıkmalıyım'

  >>> necessitative('biz', 'uza', '-', Person.FIRST, is_plural=True)
  'biz-uzamalıyız'

  ```
  """
  progressive_copula = join(
    predicate,
    Suffix.NECESSITY
      if is_front(predicate)
      else swap_front_and_back(Suffix.NECESSITY),
  )

  return join(
    subject,
    delimiter,
    impersonate(progressive_copula, whom, is_plural, in_past=False)
  )

def impotential(subject, predicate, delimiter, whom=Person.THIRD, is_plural=False):
  """
  ### impotential copula

  ✎︎ examples
  ```
  gidemem (i cannot come)
  kaçamayız (we cannot run away)
  ```

  ✎︎ tests
  ```python
  >>> impotential('men', 'git', '-', Person.FIRST, is_plural=False)
  'men-gidemem'

  >>> impotential('sen', 'git', '-', Person.SECOND, is_plural=False)
  'sen-gidemezsin'

  >>> impotential('o', 'git', '-', Person.THIRD, is_plural=False)
  'o-gidemez'

  >>> impotential('biz', 'git', '-', Person.FIRST, is_plural=True)
  'biz-gidemeyiz'

  >>> impotential('biz', 'git', '-', Person.FIRST, is_plural=True)
  'biz-gidemeyiz'

  >>> impotential('siz', 'git', '-', Person.SECOND, is_plural=True)
  'siz-gidemezsiniz'

  >>> impotential('onlar', 'git', '-', Person.THIRD, is_plural=True)
  'onlar-gidemezler'

  >>> impotential('onlar', 'al', '-', Person.THIRD, is_plural=True)
  'onlar-alamazlar'

  ```
  """
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
    subject,
    delimiter,
    voice(predicate),

    # combinative consontant ⟨y⟩
    not ends_with_consonant(predicate)
    and Suffix.Y,

    impotential_copula,
    personification,
  )

def first_person_singular(text, in_past=False):
  """
  ```python
  >>> first_person_singular('uçak')
  'uçağım'

  >>> first_person_singular('dalda', in_past=False)
  'daldayım'

  >>> first_person_singular('dalda', in_past=True)
  'daldaydım'

  >>> first_person_singular('uçak', in_past=True)
  'uçaktım'

  >>> first_person_singular('yor', in_past=False)
  'yorum'

  >>> first_person_singular('alur', in_past=True)
  'alurdum'

  ```
  """
  parts = (
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

  return join(*filter(is_truthy, parts))

def second_person_singular(text, in_past=False):
  """
  ```python
  >>> second_person_singular('uçak')
  'uçaksın'

  >>> second_person_singular('üzüm', in_past=True)
  'üzümdün'

  >>> second_person_singular('gel', in_past=True)
  'geldin'

  >>> second_person_singular('kaç', in_past=True)
  'kaçtın'

  >>> second_person_singular('humorsuz')
  'humorsuzsun'

  >>> second_person_singular('üzüm')
  'üzümsün'

  ```
  """
  parts = (
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

  return join(*filter(is_truthy, parts))

def third_person_singular(text, in_past=False):
  """
  ```python
  >>> third_person_singular('men')
  'men'

  >>> third_person_singular('men', in_past=True)
  'mendi'

  >>> third_person_singular('adam', in_past=True)
  'adamdı'

  >>> third_person_singular('üzüm', in_past=True)
  'üzümdü'

  ```
  """
  parts = (
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

  return join(*filter(is_truthy, parts))

def first_person_plural(text, in_past=False):
  """
  ```python
  >>> first_person_plural('uçak')
  'uçağız'

  >>> first_person_plural('kale')
  'kaleyiz'

  >>> first_person_plural('kale', in_past=True)
  'kaleydik'

  ```
  """
  parts = (
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

  return join(*filter(is_truthy, parts))

def second_person_plural(text, in_past=False):
  """
  ```python
  >>> second_person_plural('elma', in_past=False)
  'elmasınız'

  >>> second_person_plural('elma', in_past=True)
  'elmaydınız'

  >>> second_person_plural('gezegen', in_past=True)
  'gezegendiniz'

  >>> second_person_plural('üzüm', in_past=True)
  'üzümdünüz'

  >>> second_person_plural('ağaç', in_past=True)
  'ağaçtınız'

  ```
  """
  parts = (
    second_person_singular(text, in_past),

    # ⟨a⟩ ⟨i⟩ ⟨u⟩ ⟨ü⟩
    harmony(
      get_vowel_symbol(
        get_last_vowel(
          text))).value,

    Suffix.Z,
  )

  return join(*filter(is_truthy, parts))

def third_person_plural(text, in_past=False):
  """
  ```python
  >>> third_person_plural('gezegen')
  'gezegenler'

  >>> third_person_plural('gezegen')
  'gezegenler'

  >>> third_person_plural('gezegen', in_past=True)
  'gezegendiler'

  ```
  """
  parts = (
    third_person_singular(text, in_past),

    # -lar or -ler, plural affix
    Suffix.LER if is_front(text) else Suffix.LAR
  )

  return join(*filter(is_truthy, parts))

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

def predicate(text):
  return text

if __name__ == "__main__":
    import doctest
    doctest.testmod()