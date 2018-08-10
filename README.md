
# Kefir

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

# Grammatical Cases

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

# nominative case (yalın in turkish)
the simplest grammatical case, there's no suffix to
affix in that case.

nominative comes from latin cāsus nominātīvus 
means case for naming.


# ablative case (ayrılma in turkish)
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


# accusative (ilgi in turkish)
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


# genitive case (genitifler in turkish)
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


# going-towards case (yönelme in turkish)
In some languages, the dative is used to mark the
indirect object of a sentence.

✎︎ examples
```
marya yakup'a bir drink verdi (maria gave jacob a drink)
maria jacobī potum dedit (maria gave jacob a drink)
```


# locative case (bulunma in turkish)
Locative is a grammatical case which indicates a location.
It corresponds vaguely to the English prepositions "in",
"on", "at", and "by". 

✎︎ examples
```
bahçe[de] hanımeli var.
yorum[da] iyi beatler var.
kalem[de] güzel uç var.
```


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


# Turkish Predication and Copula

turkish language copulas, which are called as ek-eylem which
literally means 'suffix-verb' are one of the most distinct
features of turkish grammar.

TODO: Remove unused imports.

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

