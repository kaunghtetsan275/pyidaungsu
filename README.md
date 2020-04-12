# Pyidaungsu

Python library for Myanmar language. Useful in Natural Language Processing and text preprocessing for Myanmar language.

## Installation

```sh
pip install pyidaungsu
```

## Usage

### Zawgyi-Unicode detection

```sh
import pyidaungsu as pds

# font encoding detection
pds.detect("ထမင်းစားပြီးပြီလား")
>> "Unicode"
```

### Zawgyi-Unicode conversion

```sh
# convert to zawgyi
pds.cvt2zgi("ထမင်းစားပြီးပြီလား")
>> "ထမင္းစားၿပီးၿပီလား"

# convert to unicode
pds.cvt2uni("ထမင္းစားၿပီးၿပီလား")
>> "ထမင်းစားပြီးပြီလား"
```

### Syllabification

```sh
# syllabification
pds.syllabify("Alan TuringကိုArtificial Intelligenceနဲ့Computerတွေရဲ့ဖခင်ဆိုပြီးလူသိများပါတယ်")
>> ['Alan', 'Turing', 'ကို', 'Artificial', 'Intelligence', 'နဲ့', 'Computer', 'တွေ', 'ရဲ့', 'ဖ', 'ခင်', 'ဆို', 'ပြီး', 'လူ', 'သိ', 'များ', 'ပါ', 'တယ်']
```

## Future work

- [ ] Add tokenizer for Burmese
- [ ] Add Part-of-Speech (POS) tagger for Burmese
- [ ] Add Named-entities Recognition (NER) classifier for Burmese
- [ ] Add thorough documentation
