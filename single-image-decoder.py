import jsonrpclib
from cv2 import imread
import numpy as np
from itertools import groupby
from operator import itemgetter

def normalize_image(imgfile, pad_x=15, pad_y=15):
    img = imread(imgfile, 0)
    img = 255 - img;
    img = np.pad(img, ((pad_y, pad_y), (pad_x, pad_x)), 'constant')
    padded_shape = img.shape
    img = img.reshape(img.size, 1)
    img = img.astype("float32") / 255.0
    return img, padded_shape

def main():
    batch_size = 1 # ATUALMENTE SO FUNCIONA COM UMA IMAGEM POR VEZ
    nb_classes = 79
    chars = [
    "!", "#", "\"", "'", "&", ")", "(", "+", "*", "-", ",", "/", ".", 
    "1", "0", "3", "2", "5", "4", "7", "6", "9", "8", ";", ":", "?",
    "A", "C", "B", "E", "D", "G", "F", "I", "H", "K", "J", "M", "L",
    "O", "N", "Q", "P", "S", "R", "U", "T", "W", "V", "Y", "X", "Z",
    "a", "c", "b", "e", "d", "g", "f", "i", "h", "k", "j", "m", "l",
    "o", "n", "q", "p", "s", "r", "u", "t", "w", "v", "y", "x", "z",
    " ", ""]

    pad_whitespaces = "|"
    
    img, padded_shape = normalize_image("/home/dayvidwelles/MasterResearch/main/returnn-modified/demos/mdlstm/IAM/IAM_lines/a01-000u-00.png")

    rpc = jsonrpclib.Server('http://localhost:3334')
    imgs = [img]
    padded_shapes = [padded_shape]

    data_structure = {}
    data_structure['classes'] = [nb_classes,1]
    data_structure['data'] = []
    data_structure['sizes'] = []

    imgs = np.concatenate(imgs, axis=0)
    padded_shapes = np.concatenate(padded_shapes, axis=0)

    data_structure['sizes'] += padded_shapes.tolist()

    for img in imgs:
        data_structure['data'].append(img.tolist())

    json = data_structure

    while True:
        try:
            ret = rpc.classify(json)
            r = rpc.result(ret['result']['hash'])[u'result'][u'seq-0']
        except KeyError:
            continue
        break

    output = r[0]
    output = np.transpose(output, (1,0,2))
    output = np.squeeze(output, 0)

    transcription = ''.join(map(itemgetter(0), groupby([chars[emissions.argmax()] for emissions in output])))

    print transcription

if __name__ == '__main__':
    main()