import re, os
import pycrfsuite

class Tokenize:
    def __init__(self):
        self.karen_consonant = 'ကခဂဃငစဆၡညတထဒနပဖဘမယရလဝသဟအဧၦ'
        self.shan_consonant = 'ၵၶငၸသၹၺတထၼပၽၾမယလဝရႁဢၷႀၻၿ'
        self.mon_consonant = 'ကခဂဃၚစဆဇၛညဋဌဍဎဏတထဒဓနပဖဗဘမယရလဝသဟဠၜအၝ'
        self.burmese_consonant = 'က-အ'
        self.others = '၀-၉၊။!-/:-@[-`{-~\s.'

    def create_char_features(self, sentence, i):
        features = [
        'bias',
        'char=' + sentence[i][0] 
        ]
        
        if i >= 1:
            features.extend([
                'char-1=' + sentence[i-1][0],
                'char-1:0=' + sentence[i-1][0] + sentence[i][0],
            ])
        else:
            features.append("BOS")
            
        if i >= 2:
            features.extend([
                'char-2=' + sentence[i-2][0],
                'char-2:0=' + sentence[i-2][0] + sentence[i-1][0] + sentence[i][0],
                'char-2:-1=' + sentence[i-2][0] + sentence[i-1][0],
            ])
            
        if i >= 3:
            features.extend([
                'char-3:0=' + sentence[i-3][0] + sentence[i-2][0] + sentence[i-1][0] + sentence[i][0],
                'char-3:-1=' + sentence[i-3][0] + sentence[i-2][0] + sentence[i-1][0],
            ])
            
            
        if i + 1 < len(sentence):
            features.extend([
                'char+1=' + sentence[i+1][0],
                'char:+1=' + sentence[i][0] + sentence[i+1][0],
            ])
        else:
            features.append("EOS")
            
        if i + 2 < len(sentence):
            features.extend([
                'char+2=' + sentence[i+2][0],
                'char:+2=' + sentence[i][0] + sentence[i+1][0] + sentence[i+2][0],
                'char+1:+2=' + sentence[i+1][0] + sentence[i+2][0],
            ])
            
        if i + 3 < len(sentence):
            features.extend([
                'char:+3=' + sentence[i][0] + sentence[i+1][0] + sentence[i+2][0]+ sentence[i+3][0],
                'char+1:+3=' + sentence[i+1][0] + sentence[i+2][0] + sentence[i+3][0],
            ])
        
        return features

    def create_sentence_features(self, prepared_sentence):
        return [self.create_char_features(prepared_sentence, i) for i in range(len(prepared_sentence))]

    def segment_sentence(self, tagger, sentence):
        sent = sentence.replace(" ", "")
        prediction = tagger.tag(self.create_sentence_features(sent))
        complete = ""
        for i, p in enumerate(prediction):
            if p == "1":
                complete += " " + sent[i]
            else:
                complete += sent[i]
        return complete
    
    def tokenize(self, line, lang='mm', form='syllable'):

        if form=='word':
            return self.tokenize_word(line,lang,form)
        if lang=='mm':
            others = 'ဣဤဥဦဧဩဪဿ၌၍၏၀-၉၊။!-/:-@[-`{-~\s.,'
            line = re.sub("(?<![္])(["+self.burmese_consonant+"])(?![်္])|(["+others+"])",r" \1\2", line).strip()
        if lang=='karen':
            line = re.sub("(["+self.karen_consonant+"])|(["+self.others+"])",r" \1\2", line).strip()
        if lang=='shan':
            line = re.sub("(["+self.shan_consonant+"])(?![်္])|(["+self.others+"])",r" \1\2", line).strip()
        if lang=='mon':
            line = re.sub("(?<![္])(["+self.mon_consonant+"])(?![်္])|(["+self.others+"])",r" \1\2", line).strip()

        line = re.sub('(?<=[က-ၴ])([a-zA-Z0-9])',r' \1',line)
        line = re.sub('([0-9၀-၉])\s+([0-9၀-၉])\s*',r'\1\2 ',line)
        line = re.sub('([0-9၀-၉])\s+(\+)',r'\1 \2 ',line)

        return line.split()
    
    def tokenize_word(self, line, lang, form):
        tagger = pycrfsuite.Tagger()
        model_path = os.path.join(os.path.abspath(os.path.dirname(__file__)),'model/tokenizer.crfsuite')
        tagger.open(model_path)
        return self.segment_sentence(tagger,line).strip().split()