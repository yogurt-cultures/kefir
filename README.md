<details open>
<summary open>kefir</summary>

# Kefir

![Logo](https://avatars1.githubusercontent.com/u/42190640?s=200&v=4)

Yogurt is a free software community established at Mustafa Akgül Free Software Camp of 2018.

Kefir is a natural language processing kit for Turkic languages, and maybe Finnish and Hungarian in phonology.

# Usage

There are two competing notions of the predicate in theories of grammar.
The competition between these two concepts has generated confusion concerning
the use of the term predicate in theories of grammar.

Kefir is designed to construct sentences by using
[predicate-logic](https://www.wikiwand.com/en/Predicate_(grammar)).

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

</details>
<details>
<summary>kefir.case</summary>

# Grammatical Cases

Implemented 6 grammatical cases:

- Nominative
- Genitive
- Dative
- Accusative
- Ablative
- Locative

Turkish has 9 more:

- Essive
- Instrumental
- Inclusive
- Abessive
- Likeness
- Coverage
- Qualitative
- Conditional
- Possesive

📖 Read more on: [Turkish Cases](https://en.wikibooks.org/wiki/Turkish/Cases).

TODO: Enum'lardaki rakamlar yerine auto() kullanılmalı.

## Nominative Case ('Yalın' in Turkish)

The simplest grammatical case, there's no suffix to affix in that case.

Nominative comes from Latin cāsus nominātīvus means case for naming.

## Ablative Case ('Ayrılma' in Turkish)

A grammatical case for nouns, pronouns and adjectives in
the grammar of various languages; it is sometimes used to
express motion away from something, among other uses.

✎︎ Examples:
```
adalar[dan] geldim
merkez[den] geçtim
teyit[ten] geçtim
açlık[tan] öldüm
```

## Accusative ('İlgi' in Turkish)

The accusative case (abbreviated acc) of a noun is the
grammatical case used to mark the direct object of a
transitive verb. The same case is used in many
languages for the objects of (some or all) prepositions.

✎︎ Examples:
```
aday[ı] yedim
evim[i] yaptım
üzüm[ü] pişirdim
```

## Genitive Case ('Genitifler' in Turkish)

In grammar, the genitive is the grammatical case
that marks a word, usually a noun, as modifying
another word, also usually a noun.

✎︎ Examples:
```
hanımelinin çiçeği (flower of a plant called hanımeli)
kadının ayakkabısı (shoes of the woman)
باب بيت bābu baytin (the door of a house)
mari[i] nie ma w domu (maria is not at home)
```

## Dative Case ('Yönelme' in Turkish)

In some languages, the dative is used to mark the
indirect object of a sentence.

✎︎ Examples:
```
marya yakup'a bir drink verdi (maria gave jacob a drink)
maria jacobī potum dedit (maria gave jacob a drink)
```

## Locative Case ('Bulunma' in Turkish)

Locative is a grammatical case which indicates a location.
It corresponds vaguely to the English prepositions "in",
"on", "at", and "by".

✎︎ Examples:
```
bahçe[de] hanımeli var.
yorum[da] iyi beatler var.
kalem[de] güzel uç var.
```

</details>
<details>
<summary>kefir.phonology</summary>

# Turkish Phonology

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

#### \#swap_front_and_back

Swaps front sounds to back, and vice versa.

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

## Voicing or Sonorization ('Yumuşama' in Turkish)

To make pronouncation easier, nouns ending
with these sounds:

```
⟨p⟩ ⟨ç⟩ ⟨t⟩ ⟨k⟩
```

May be softened by replacing them in order:

```
⟨b⟩ ⟨c⟩ ⟨d⟩ ⟨ğ⟩
```

✎︎ Examples:
```
ço⟨p⟩un → ço⟨b⟩un
ağa⟨ç⟩ın → ağa⟨c⟩n
kağı⟨t⟩ın → kağı⟨d⟩ın
ren⟨k⟩in → ren⟨g⟩in
```

✎︎ Examples in other languages:
```
li⟨f⟩e → li⟨v⟩e
stri⟨f⟩e → stri⟨v⟩e
proo⟨f⟩ → pro⟨v⟩e
```

## Devoicing or Desonorization ('Sertleşme' in Turkish)

To make pronouncation easier, nouns ending with
these sounds:
```
⟨p⟩ ⟨ç⟩ ⟨t⟩ ⟨k⟩
```

May be hardened by replacing them in order:

```
⟨b⟩ ⟨c⟩ ⟨d⟩ ⟨ğ⟩
```

✎︎ Examples:
```
ço⟨p⟩un → ço⟨b⟩un
ağa⟨ç⟩ın → ağa⟨c⟩n
kağı⟨t⟩ın → kağı⟨d⟩ın
ren⟨k⟩in → ren⟨g⟩in
```

✎︎ Examples in Other Languages:
```
dogs → dogs ([ɡz])
missed → missed ([st])
whizzed → whizzed ([zd])
prośba → prɔʑba
просьба → prozʲbə
```

</details>
<details>
<summary>kefir.predication</summary>

# Turkish Predication and Copula

Turkish language copulas, called 'ek-eylem' (literally 'suffix-verb'),
are one of the most distinct features of Turkish grammar.

TODO: Remove unused imports.

#### Zero Copula

Zero copula is the rule for third person, as in Hungarian
and Russian. That means two nouns, or a noun and an
adjective can be juxtaposed to make a sentence without
using any copula. Third person plural might be indicated
with the use of plural suffix "-lar/-ler".

✎︎ Examples:
```
yogurt kültür (yogurt [is-a] culture)
abbas yolcu (abbas [is-a] traveller)
evlerinin önü yonca (the front of their home [is-a] plant called yonca)
```

✎︎ Tests:
```python
>>> zero('yolcu')
'yolcu'

 ```

#### Negative

Negation is indicated by the negative copula 'değil'.
'Değil' is never used as a suffix, but it takes suffixes according to context.

✎︎ Examples:
```
yogurt kültür değildir (yogurt [is-not-a] culture)
abbas yolcu değildir (abbas [is-not-a] traveller)
evlerinin önü yonca değildir (the front of their home [is-not-a] yonca)
```

✎︎ Tests:
```python
>>> negative('yolcu')
'yolcu değil'

```

### To Be

Turkish "to be" as regular/auxiliary verb ('olmak').

✎︎ Examples:
```
yogurt kültürdür (yogurt [is] culture)
abbas yolcudur (abbas [is] traveller)
evlerinin önü yoncadır (the front of their home [is] plant called yonca)
```

✎︎ Tests:
```python
>>> tobe('yolcu')
'yolcudur'
>>> tobe('üzüm')
'üzümdür'
>>> tobe('yonca')
'yoncadır'

```


### Personification Copula

✎︎ Examples:
```
ben buralıyım (i'm from here)
sen oralısın (you're from over there)
aynı gezegenliyiz (we're from same planet)
```

✎︎ Tests:
```python
>>> personal('uçak', Person.FIRST, is_plural=False)
'uçağım'

>>> personal('oralı', Person.SECOND, is_plural=False)
'oralısın'

>>> personal('gezegenli', Person.FIRST, is_plural=True)
'gezegenliyiz'

```

### Inferential Mood ('-miş' in Turkish)

Inferential mood is used to convey information about events
which were not directly observed or were inferred by the speaker.

✎︎ Examples:
```
elmaymışım (i was an apple as i've heard)
üzülmüşsün (you were sad as i've heard)
doktormuş (he/she/it was a doctor as i've heard)
üzümmüşsün (you were a grape as i've heard)
```

✎︎ Tests:
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

### Inferential Mood ('-isem' in Turkish)

Inferential mood is a grammatical mood used to express a proposition whose
validity is dependent on some condition, possibly counterfactual.

✎︎ Examples:
```
elmaysam (if i am an apple)
üzümsen (if you are a grape)
bıçaklarsa (if they are a knife)
```

✎︎ Tests:
```python
>>> conditional('elma', Person.FIRST, is_plural=False)
'elmaysam'
>>> conditional('üzüm', Person.SECOND, is_plural=False)
'üzümsen'
>>> conditional('bıçak', Person.THIRD, is_plural=True)
'bıçaklarsa'

```

### Alethic Modality ('-idi' in Turkish)

Linguistic modality that indicates modalities of truth,
in particular the modalities of logical necessity,
possibility or impossibility.

✎︎ Examples:
```
elmaydım (i was an apple)
üzümdün (you were a grape)
doktordu (he/she/it was a doctor)
```

✎︎ Tests:
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

### The Imperfective ('-iyor' in Turkish)

Grammatical aspect used to describe a situation viewed with interior composition.
It describes ongoing, habitual, repeated, or similar semantic roles,
whether that situation occurs in the past, present, or future.

✎︎ Examples:
```
gidiyorum (i'm going)
kayıyor (he's skating)
üzümlüyor (he's graping)
```

✎︎ Tests:
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

### The Future Tense ('-iyor' in Turkish)

The future tense is a verb form that generally marks the event described by the
verb as not having happened yet, but expected to happen in the future.

✎︎ Examples:
```
gidecek (he'll go)
ölecek (he'll die)
can alacak (he'll kill someone)
```

✎︎ Tests:
```python
>>> future('gel', Person.FIRST, is_plural=False)
'geleceğim'

>>> future('açık', Person.FIRST, is_plural=False)
'açıkacağım'

>>> future('gel', Person.FIRST, is_plural=True)
'geleceğiz'

```

### Progressive Tense

✎︎ Examples:
gülmekteyim (i am in the process of laughing)
ölmekteler (they are in the process of dying 👾)

✎︎ Tests:
```python
>>> progressive('gel', Person.FIRST, is_plural=False)
'gelmekteyim'

>>> progressive('açık', Person.FIRST, is_plural=False)
'açıkmaktayım'

>>> progressive('gel', Person.FIRST, is_plural=True)
'gelmekteyiz'

```

### Necessitative Copula

✎︎ Examples:
```
gitmeliyim (i must go)
kaçmalıyım (i must run away)
```

✎︎ Tests:
```python
>>> necessitative('git', Person.FIRST, is_plural=False)
'gitmeliyim'

>>> necessitative('açık', Person.FIRST, is_plural=False)
'açıkmalıyım'

>>> necessitative('uza', Person.FIRST, is_plural=True)
'uzamalıyız'

```

### Impotential Copula

✎︎ Examples:
```
gidemem (i cannot come)
kaçamayız (we cannot run away)
```

✎︎ Tests:
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

</details>

<details>
<summary>kefir.meta</summary>

# Contribution Guide

- Don't load a fixture, code is our data.
- Don't leave a comment! Docstrings are only for the context and test.
- Be nice 🦄

# Credits

- Berk Buzcu (8-bit artwork)
- Serdar Açıkyol (Illustration)
- Fatih Erikli (Phonological Processes, Predicate Logic)
- Armagan Amcalar ([Javascript Port](https://github.com/yogurt-cultures/kefir-js))
- Umut Karcı (Packaging and Versioning)
- Kerem Bozdaş (Editing)

# License

This project is licensed under the terms of the [MIT license](https://github.com/yogurt-cultures/kefir/blob/master/LICENSE).

</details>
