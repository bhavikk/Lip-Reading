from os import listdir
from config import *
import cv2
import numpy as np
from playground import *
import pickle
from pprint import pprint
from keras.models import load_model



path = './data/cleaned/a/'

no_of_frames = 10


def prepare():

    dataset = []
    num_of_videos = 0

    for imgfolder in os.listdir(path):
        imgs = []
        px = os.path.join(path, imgfolder)
        for img in os.listdir(px):
            print(px+"/"+img)
            # print(os.path.join(px, img))
            imx = cv2.imread(px+"/"+img, 0)
            # cv2.imshow("ASDF ", imx)
            # cv2.waitKey(0)

            imx = imx/255
            # imx = round(imx/255)
            # print(imx)
            # pprint(imx)
            imgs.append(imx)
            # print(imx)
        if(len(imgs) == 0):
            print("Empty frame array continuing..")
            continue
        num_of_videos += 1
        frames = normalize(imgs, no_of_frames)
        dataset = dataset + frames



    return dataset, num_of_videos





index_dict = dict()
num_of_words = 0

words = []

for word in listdir("./data/cleaned/"):
    index_dict[word] = num_of_words
    words.append(word)
    num_of_words += 1


def normalize(frames, num_of_frames):
	new_frames = []
	if(len(frames) == 0):
		print("Empty frame array")
		return []
	req = num_of_frames//len(frames)
	for frame in frames:
		for _ in range(req):
			new_frames.append(frame)
	mod = num_of_frames % len(frames)
	for i in range(mod):
		new_frames.append(frames[i])
	return new_frames






X, l = prepare()
# print(X)
X = np.array(X)

X = X.reshape(l, no_of_frames, 64, 64, 1)

print(X.shape)


model = load_model('my_model.h5')


y = model.predict(X, batch_size=None, verbose=1, steps=None)

print(y.shape)

list_y = y.tolist()

for row in list_y:
    ind = row.index(max(row))
    print(row)
    print(words[ind])
# # model =
