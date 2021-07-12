from tensorflow import keras
import pickle as pkl
import numpy as np
from pathlib import Path
import os

CONSTANTS_PATH = 'D:\Projects\Gradution Project\AutomaticEarabSystem\helpers'
WITH_EXTRA_TRAIN = False

with open(CONSTANTS_PATH + '/ARABIC_LETTERS_LIST.pickle', 'rb') as file:
    ARABIC_LETTERS_LIST = pkl.load(file)
with open(CONSTANTS_PATH + '/DIACRITICS_LIST.pickle', 'rb') as file:
    DIACRITICS_LIST = pkl.load(file)

if not WITH_EXTRA_TRAIN:
    with open(CONSTANTS_PATH + '/RNN_SMALL_CHARACTERS_MAPPING.pickle', 'rb') as file:
        CHARACTERS_MAPPING = pkl.load(file)
else:
    with open(CONSTANTS_PATH + '/RNN_BIG_CHARACTERS_MAPPING.pickle', 'rb') as file:
        CHARACTERS_MAPPING = pkl.load(file)
with open(CONSTANTS_PATH + '/RNN_CLASSES_MAPPING.pickle', 'rb') as file:
    CLASSES_MAPPING = pkl.load(file)
with open(CONSTANTS_PATH + '/RNN_REV_CLASSES_MAPPING.pickle', 'rb') as file:
    REV_CLASSES_MAPPING = pkl.load(file)


def to_one_hot(data, size):
    one_hot = list()
    for elem in data:
        cur = [0] * size
        cur[elem] = 1
        one_hot.append(cur)
    return one_hot


def remove_diacritics(data_raw):
    return data_raw.translate(str.maketrans('', '', ''.join(DIACRITICS_LIST)))


def map_data(data_raw):
    X = list()
    Y = list()
    
    for line in data_raw:        
        x = [CHARACTERS_MAPPING['<SOS>']]
        y = [CLASSES_MAPPING['<SOS>']]
        for idx, char in enumerate(line):
            if char in DIACRITICS_LIST:
                continue
            x.append(CHARACTERS_MAPPING[char])
            if char not in ARABIC_LETTERS_LIST:
                y.append(CLASSES_MAPPING[''])
            else:
                char_diac = ''
                if idx + 1 < len(line) and line[idx + 1] in DIACRITICS_LIST:
                    char_diac = line[idx + 1]
                    if idx + 2 < len(line) and line[idx + 2] in DIACRITICS_LIST and char_diac + line[idx + 2] in CLASSES_MAPPING:
                        char_diac += line[idx + 2]
                    elif idx + 2 < len(line) and line[idx + 2] in DIACRITICS_LIST and line[idx + 2] + char_diac in CLASSES_MAPPING:
                        char_diac = line[idx + 2] + char_diac
                y.append(CLASSES_MAPPING[char_diac])
        
        assert(len(x) == len(y))
        
        x.append(CHARACTERS_MAPPING['<EOS>'])
        y.append(CLASSES_MAPPING['<EOS>'])
        
        y = to_one_hot(y, len(CLASSES_MAPPING))
        
        X.append(x)
        Y.append(y)
    
    X = np.asarray(X)
    Y = np.asarray(Y)
    
    return X, Y
    

def predict(line, model):
    X, _ = map_data([line])
    predictions = model.predict(X).squeeze()
    predictions = predictions[1:]
    
    output = ''
    for char, prediction in zip(remove_diacritics(line), predictions):
        output += char
        
        if char not in ARABIC_LETTERS_LIST:
            continue
        
        if '<' in REV_CLASSES_MAPPING[np.argmax(prediction)]:
            continue

        output += REV_CLASSES_MAPPING[np.argmax(prediction)]

    return output


model = keras.models.load_model('Encoder.sav')
print(predict('السلام عليكم', model))
