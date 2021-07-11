# Pyidaungsu

Python library for Myanmar language. Useful in Natural Language Processing and text preprocessing for Myanmar language.

## Installation

```sh
pip install pyidaungsu
```

## Usage

### ~~Zawgyi-Unicode detection~~ Language detection (Myanmar <Zawgyi, Unicode>, Karen, Mon, Shan)
Starting from the pyidaungsu 0.0.9, it does not only detect Zawgyi and Unicode for Myanmar language but also other languages such as Mon, Karen, Shan as well.

```sh
import pyidaungsu as pds

# language detection
pds.detect("ထမင်းစားပြီးပြီလား")
>> "mm_uni"
pds.detect("ထမင္းစားၿပီးၿပီလား")
>> "mm_zg"
pds.detect("တၢ်သိၣ်လိတၢ်ဖးလံာ် ကွဲးလံာ်အိၣ်လၢ မ့ရ့ၣ်အစုပူၤလီၤ.")
>> "karen"
pds.detect("ဇၟာပ်မၞိဟ်ဂှ် ကတဵုဒှ်ကၠုင် ပ္ဍဲကဵုဂကောံမွဲ ဖအိုတ်ရ၊၊")
>> "mon"
pds.detect("ၼႂ်းဢိူင်ႇမိူင်းၽူင်း ၸႄႈဝဵင်းတႃႈၶီႈလဵၵ်း ၾႆးမႆႈႁိူၼ်း ၵူၼ်းဝၢၼ်ႈ လင်ၼိုင်ႈ")
>> "shan"
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

### Tokenization

```sh
# syllable level tokenization for Burmese
pds.tokenize("Alan TuringကိုArtificial Intelligenceနဲ့Computerတွေရဲ့ဖခင်ဆိုပြီးလူသိများပါတယ်") # lang parameter for default function is 'mm'
>> ['Alan', 'Turing', 'ကို', 'Artificial', 'Intelligence', 'နဲ့', 'Computer', 'တွေ', 'ရဲ့', 'ဖ', 'ခင်', 'ဆို', 'ပြီး', 'လူ', 'သိ', 'များ', 'ပါ', 'တယ်']

# syllable level tokenization for Karen
pds.tokenize("သရၣ်,သရၣ်မုၣ် ခဲလၢာ်ဟးထီၣ် (၃၅) ဂၤန့ၣ်လီၤ.", lang="karen")
>> ['ကၠိ', 'သ', 'ရၣ်', ',', 'သ', 'ရၣ်', 'မုၣ်', 'ခဲ', 'လၢာ်', 'ဟး', 'ထီၣ်', '(', '၃၅', ')', 'ဂၤ', 'န့ၣ်', 'လီၤ', '.']

# word level tokenization
pds.tokenize("ဖေဖေနဲ့မေမေ၏ကျေးဇူးတရားမှာကြီးမားလှပေသည်", form="word")
>> ['ဖေဖေ', 'နဲ့', 'မေမေ', '၏', 'ကျေးဇူးတရား', 'မှာ', 'ကြီးမား', 'လှ', 'ပေ', 'သည်']

```

Syllable-level tokenization supports for 4 languages (Burmese, Karen, Shan, Mon). Word-level tokenization supports only Burmese currently.</br>
Available values for `lang` parameter in `tokenize` function: "mm", "karen", "mon", "shan"

## Future work

- [x] Add tokenizer for Burmese (Syllabel and word-level tokenization)
- [ ] Add more tokenizer (BPE, WordPiece etc.)
- [ ] Add Part-of-Speech (POS) tagger for Burmese
- [ ] Add Named-entities Recognition (NER) classifier for Burmese
- [ ] Add thorough documentation
