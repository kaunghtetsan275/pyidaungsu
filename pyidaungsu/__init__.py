from pyidaungsu.tokenize import Tokenize
import emoji
import fasttext
import re, os, sys
import numpy as np

sys.stdout = open(os.devnull, "w")
sys.stderr = open(os.devnull, "w")
f = fasttext.load_model(os.path.join(os.path.abspath(os.path.dirname(__file__)),'model/pdsdetect.ftz'))

def cvt2zg(text):
    rules = [
        { "from": u"\u1004\u103a\u1039", "to": u"\u1064" }, { "from": u"\u1039\u1010\u103d", "to": u"\u1096" }, { "from": u"\u1014(?=[\u1030\u103d\u103e\u102f\u1039])", "to": u"\u108f" }, { "from": u"\u102b\u103a", "to": u"\u105a" }, { "from": u"\u100b\u1039\u100c", "to": u"\u1092" }, { "from": u"\u102d\u1036", "to": u"\u108e" }, { "from": u"\u104e\u1004\u103a\u1038", "to": u"\u104e" }, { "from": u"[\u1025\u1009](?=[\u1039\u102f\u1030])", "to": u"\u106a" }, { "from": u"[\u1025\u1009](?=[\u103a])", "to": u"\u1025" }, { "from": u"\u100a(?=[\u1039\u102f\u1030\u103d])", "to": u"\u106b" }, { "from": u"(\u1039[\u1000-\u1021])\u102f", "to": u"\\1\u1033" }, { "from": u"(\u1039[\u1000-\u1021])\u1030", "to": u"\\1\u1034" }, { "from": u"\u1039\u1000", "to": u"\u1060" }, { "from": u"\u1039\u1001", "to": u"\u1061" }, { "from": u"\u1039\u1002", "to": u"\u1062" }, { "from": u"\u1039\u1003", "to": u"\u1063" }, { "from": u"\u1039\u1005", "to": u"\u1065" }, { "from": u"\u1039\u1007", "to": u"\u1068" }, { "from": u"\u1039\u1008", "to": u"\u1069" }, { "from": u"\u100a(?=[\u1039\u102f\u1030])", "to": u"\u106b" }, { "from": u"\u1039\u100b", "to": u"\u106c" }, { "from": u"\u1039\u100c", "to": u"\u106d" }, { "from": u"\u100d\u1039\u100d", "to": u"\u106e" }, { "from": u"\u100e\u1039\u100d", "to": u"\u106f" }, { "from": u"\u1039\u100f", "to": u"\u1070" }, { "from": u"\u1039\u1010", "to": u"\u1071" }, { "from": u"\u1039\u1011", "to": u"\u1073" }, { "from": u"\u1039\u1012", "to": u"\u1075" }, { "from": u"\u1039\u1013", "to": u"\u1076" }, { "from": u"\u1039\u1013", "to": u"\u1076" }, { "from": u"\u1039\u1014", "to": u"\u1077" }, { "from": u"\u1039\u1015", "to": u"\u1078" }, { "from": u"\u1039\u1016", "to": u"\u1079" }, { "from": u"\u1039\u1017", "to": u"\u107a" }, { "from": u"\u1039\u1018", "to": u"\u107b" }, { "from": u"\u1039\u1019", "to": u"\u107c" }, { "from": u"\u1039\u101c", "to": u"\u1085" }, { "from": u"\u103f", "to": u"\u1086" }, { "from": u"(\u103c)\u103e", "to": u"\\1\u1087" }, { "from": u"\u103d\u103e", "to": u"\u108a" }, { "from": u"(\u1064)([\u1031]?)([\u103c]?)([\u1000-\u1021])\u102d", "to": u"\\2\\3\\4\u108b" }, { "from": u"(\u1064)([\u1031]?)([\u103c]?)([\u1000-\u1021])\u102e", "to": u"\\2\\3\\4\u108c" }, { "from": u"(\u1064)([\u1031]?)([\u103c]?)([\u1000-\u1021])\u1036", "to": u"\\2\\3\\4\u108d" }, { "from": u"(\u1064)([\u1031]?)([\u103c]?)([\u1000-\u1021])", "to": u"\\2\\3\\4\\1" }, { "from": u"\u101b(?=[\u102f\u1030\u103d\u108a])", "to": u"\u1090" }, { "from": u"\u100f\u1039\u100d", "to": u"\u1091" }, { "from": u"\u100b\u1039\u100b", "to": u"\u1097" }, { "from": u"([\u1000-\u1021\u1029\u1090])([\u1060-\u1069\u106c\u106d\u1070-\u107c\u1085\u108a])?([\u103b-\u103e]*)?\u1031", "to": u"\u1031\\1\\2\\3" }, { "from": u"([\u1000-\u1021\u1029])([\u1060-\u1069\u106c\u106d\u1070-\u107c\u1085])?(\u103c)", "to": u"\\3\\1\\2" }, { "from": u"\u103a", "to": u"\u1039" }, { "from": u"\u103b", "to": u"\u103a" }, { "from": u"\u103c", "to": u"\u103b" }, { "from": u"\u103d", "to": u"\u103c" }, { "from": u"\u103e", "to": u"\u103d" }, { "from": u"\u103d\u102f", "to": u"\u1088" }, { "from": u"([\u102f\u1030\u1014\u101b\u103c\u108a\u103d\u1088])([\u1032\u1036]{0,1})\u1037", "to": u"\\1\\2\u1095" }, { "from": u"\u102f\u1095", "to": u"\u102f\u1094" }, { "from": u"([\u1014\u101b])([\u1032\u1036\u102d\u102e\u108b\u108c\u108d\u108e])\u1037", "to": u"\\1\\2\u1095" }, { "from": u"\u1095\u1039", "to": u"\u1094\u1039" }, { "from": u"([\u103a\u103b])([\u1000-\u1021])([\u1036\u102d\u102e\u108b\u108c\u108d\u108e]?)\u102f", "to": u"\\1\\2\\3\u1033" }, { "from": u"([\u103a\u103b])([\u1000-\u1021])([\u1036\u102d\u102e\u108b\u108c\u108d\u108e]?)\u1030", "to": u"\\1\\2\\3\u1034" }, { "from": u"\u103a\u102f", "to": u"\u103a\u1033" }, { "from": u"\u103a([\u1036\u102d\u102e\u108b\u108c\u108d\u108e])\u102f", "to": u"\u103a\\1\u1033" }, { "from": u"([\u103a\u103b])([\u1000-\u1021])\u1030", "to": u"\\1\\2\u1034" }, { "from": u"\u103a\u1030", "to": u"\u103a\u1034" }, { "from": u"\u103a([\u1036\u102d\u102e\u108b\u108c\u108d\u108e])\u1030", "to": u"\u103a\\1\u1034" }, { "from": u"\u103d\u1030", "to": u"\u1089" }, { "from": u"\u103b([\u1000\u1003\u1006\u100f\u1010\u1011\u1018\u101a\u101c\u101a\u101e\u101f])", "to": u"\u107e\\1" }, { "from": u"\u107e([\u1000\u1003\u1006\u100f\u1010\u1011\u1018\u101a\u101c\u101a\u101e\u101f])([\u103c\u108a])([\u1032\u1036\u102d\u102e\u108b\u108c\u108d\u108e])", "to": u"\u1084\\1\\2\\3" }, { "from": u"\u107e([\u1000\u1003\u1006\u100f\u1010\u1011\u1018\u101a\u101c\u101a\u101e\u101f])([\u103c\u108a])", "to": u"\u1082\\1\\2" }, { "from": u"\u107e([\u1000\u1003\u1006\u100f\u1010\u1011\u1018\u101a\u101c\u101a\u101e\u101f])([\u1033\u1034]?)([\u1032\u1036\u102d\u102e\u108b\u108c\u108d\u108e])", "to": u"\u1080\\1\\2\\3" }, { "from": u"\u103b([\u1000-\u1021])([\u103c\u108a])([\u1032\u1036\u102d\u102e\u108b\u108c\u108d\u108e])", "to": u"\u1083\\1\\2\\3" }, { "from": u"\u103b([\u1000-\u1021])([\u103c\u108a])", "to": u"\u1081\\1\\2" }, { "from": u"\u103b([\u1000-\u1021])([\u1033\u1034]?)([\u1032\u1036\u102d\u102e\u108b\u108c\u108d\u108e])", "to": u"\u107f\\1\\2\\3" }, { "from": u"\u103a\u103d", "to": u"\u103d\u103a" }, { "from": u"\u103a([\u103c\u108a])", "to": u"\\1\u107d" }, { "from": u"([\u1033\u1034])\u1094", "to": u"\\1\u1095" }
    ]
    for rule in rules:
        text = re.sub(rule["from"], rule["to"], text)
    return text

def cvt2uni(text):
    rules = [
        { "from": u"(\u103d|\u1087)", "to": u"\u103e" }, { "from": u"\u103c", "to": u"\u103d" }, { "from": u"(\u103b|\u107e|\u107f|\u1080|\u1081|\u1082|\u1083|\u1084)", "to": u"\u103c" }, { "from": u"(\u103a|\u107d)", "to": u"\u103b" }, { "from": u"\u1039", "to": u"\u103a" }, { "from": u"\u106a", "to": u"\u1009" }, { "from": u"\u106b", "to": u"\u100a" }, { "from": u"\u106c", "to": u"\u1039\u100b" }, { "from": u"\u106d", "to": u"\u1039\u100c" }, { "from": u"\u106e", "to": u"\u100d\u1039\u100d" }, { "from": u"\u106f", "to": u"\u100d\u1039\u100e" }, { "from": u"\u1070", "to": u"\u1039\u100f" }, { "from": u"(\u1071|\u1072)", "to": u"\u1039\u1010" }, { "from": u"\u1060", "to": u"\u1039\u1000" }, { "from": u"\u1061", "to": u"\u1039\u1001" }, { "from": u"\u1062", "to": u"\u1039\u1002" }, { "from": u"\u1063", "to": u"\u1039\u1003" }, { "from": u"\u1065", "to": u"\u1039\u1005" }, { "from": u"\u1068", "to": u"\u1039\u1007" }, { "from": u"\u1069", "to": u"\u1039\u1008" }, { "from": u"/(\u1073|\u1074)/g", "to": u"\u1039\u1011" }, { "from": u"\u1075", "to": u"\u1039\u1012" }, { "from": u"\u1076", "to": u"\u1039\u1013" }, { "from": u"\u1077", "to": u"\u1039\u1014" }, { "from": u"\u1078", "to": u"\u1039\u1015" }, { "from": u"\u1079", "to": u"\u1039\u1016" }, { "from": u"\u107a", "to": u"\u1039\u1017" }, { "from": u"\u107c", "to": u"\u1039\u1019" }, { "from": u"\u1085", "to": u"\u1039\u101c" }, { "from": u"\u1033", "to": u"\u102f" }, { "from": u"\u1034", "to": u"\u1030" }, { "from": u"\u103f", "to": u"\u1030" }, { "from": u"\u1086", "to": u"\u103f" }, { "from": u"\u1036\u1088", "to": u"\u1088\u1036" }, { "from": u"\u1088", "to": u"\u103e\u102f" }, { "from": u"\u1089", "to": u"\u103e\u1030" }, { "from": u"\u108a", "to": u"\u103d\u103e" }, { "from": u"([\u1000-\u1021])\u1064", "to": u"\u1004\u103a\u1039\\1" }, { "from": u"([\u1000-\u1021])\u108b", "to": u"\u1004\u103a\u1039\\1\u102d" }, { "from": u"([\u1000-\u1021])\u108c", "to": u"\u1004\u103a\u1039\\1\u102e" }, { "from": u"([\u1000-\u1021])\u108d", "to": u"\u1004\u103a\u1039\\1\u1036" }, { "from": u"\u108e", "to": u"\u102d\u1036" }, { "from": u"\u108f", "to": u"\u1014" }, { "from": u"\u1090", "to": u"\u101b" }, { "from": u"\u1091", "to": u"\u100f\u1039\u1091" }, { "from": u"\u1019\u102c(\u107b|\u1093)", "to": u"\u1019\u1039\u1018\u102c" }, { "from": u"(\u107b|\u1093)", "to": u"\u103a\u1018" }, { "from": u"(\u1094|\u1095)", "to": u"\u1037" }, { "from": u"\u1096", "to": u"\u1039\u1010\u103d" }, { "from": u"\u1097", "to": u"\u100b\u1039\u100b" }, { "from": u"\u103c([\u1000-\u1021])([\u1000-\u1021])?", "to": u"\\1\u103c\\2" }, { "from": u"([\u1000-\u1021])\u103c\u103a", "to": u"\u103c\\1\u103a" }, { "from": u"\u1031([\u1000-\u1021])(\u103e)?(\u103b)?", "to": u"\\1\\2\\3\u1031" }, { "from": u"([\u1000-\u1021])\u1031([\u103b\u103c\u103d\u103e]+)", "to": u"\\1\\2\u1031" }, { "from": u"\u1032\u103d", "to": u"\u103d\u1032" }, { "from": u"\u103d\u103b", "to": u"\u103b\u103d" }, { "from": u"\u103a\u1037", "to": u"\u1037\u103a" }, { "from": u"\u102f(\u102d|\u102e|\u1036|\u1037)\u102f", "to": u"\u102f\\1" }, { "from": u"\u102f\u102f", "to": u"\u102f" }, { "from": u"(\u102f|\u1030)(\u102d|\u102e)", "to": u"\\2\\1" }, { "from": u"(\u103e)(\u103b|\u1037)", "to": u"\\2\\1" }, { "from": u"\u1025(\u103a|\u102c)", "to": u"\u1009\\1" }, { "from": u"\u1025\u102e", "to": u"\u1026" }, { "from": u"\u1005\u103b", "to": u"\u1008" }, { "from": u"\u1036(\u102f|\u1030)", "to": u"\\1\u1036" }, { "from": u"\u1031\u1037\u103e", "to": u"\u103e\u1031\u1037" }, { "from": u"\u1031\u103e\u102c", "to": u"\u103e\u1031\u102c" }, { "from": u"\u105a", "to": u"\u102b\u103a" }, { "from": u"\u1031\u103b\u103e", "to": u"\u103b\u103e\u1031" }, { "from": u"(\u102d|\u102e)(\u103d|\u103e)", "to": u"\\2\\1" }, { "from": u"\u102c\u1039([\u1000-\u1021])", "to": u"\u1039\\1\u102c" }, { "from": u"\u103c\u1004\u103a\u1039([\u1000-\u1021])", "to": u"\u1004\u103a\u1039\\1\u103c" }, { "from": u"\u1039\u103c\u103a\u1039([\u1000-\u1021])", "to": u"\u103a\u1039\\1\u103c" }, { "from": u"\u103c\u1039([\u1000-\u1021])", "to": u"\u1039\\1\u103c" }, { "from": u"\u1036\u1039([\u1000-\u1021])", "to": u"\u1039\\1\u1036" }, { "from": u"\u1092", "to": u"\u100b\u1039\u100c" }, { "from": u"\u104e", "to": u"\u104e\u1004\u103a\u1038" }, { "from": u"\u1040(\u102b|\u102c|\u1036)", "to": u"\u101d\\1" }, { "from": u"\u1025\u1039", "to": u"\u1009\u1039" }, { "from": u"([\u1000-\u1021])\u103c\u1031\u103d", "to": u"\\1\u103c\u103d\u1031" }, { "from": u"([\u1000-\u1021])\u103d\u1031\u103b", "to": u"\\1\u103b\u103d\u1031" }
    ]
    for rule in rules:
        text = re.sub(rule["from"], rule["to"], text)
    return text

def predict(text, k=1, threshold=0.0, on_unicode_error='strict'):
    global f
    
    def check(entry):
        if entry.find('\n') != -1:
            raise ValueError(
                "predict processes one line at a time (remove newline)"
            )
        entry += "\n"
        return entry

    if type(text) == list:
        #text = [check(entry) for entry in text]
        all_labels, all_probs = f.multilinePredict(text, k, threshold, on_unicode_error)
        return all_labels, all_probs
    else:
        #text = check(text)
        predictions = f.predict(text, k, threshold, on_unicode_error)
        if predictions:
            #probs, labels = zip(*predictions)
            probs, labels = predictions[1],predictions
        else:
            probs, labels = ([], ())

        return labels, np.array(probs, copy=False)

def detect(text):
    return predict(text)[0][0][0][9:]

def tokenize(text,lang='mm',form='syllable'):
    return Tokenize().tokenize(text, lang, form)