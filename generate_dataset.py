from os import listdir
from config import *
import cv2
import numpy as np
import pickle

#
# def shuffle_in_unison_scary(a, b):
# 	rng_state = np.random.get_state()
# 	np.random.shuffle(a)
# 	np.random.set_state(rng_state)
# 	np.random.shuffle(b)
#
# 	return a, b

no_of_frames = 3


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

# if __name__ == "__main__":
train_x = []
train_y = []
num_of_videos = 0
num_of_words = 0
num_of_word_lim = 5
index_dict = {}

f = open('logging.txt', 'w')

for word in listdir(working_dir + "data/cleaned/"):
	f.write(word)
	index_dict[word] = num_of_words

	num_of_words += 1
	if num_of_word_lim <= num_of_words:
		break


f.write("------------------------ hohayaa ----------------------\n")


cnt = 0

for word in listdir(working_dir + "data/cleaned/"):

	if cnt == num_of_word_lim:
		break

	cnt+=1

	# f.write(word)
	for video in listdir(working_dir + "data/cleaned/" + word + "/"):
		frames = []
		prediction = [0]*num_of_words
		for image in listdir(working_dir + "data/cleaned/" + word + "/" + video + "/"):
			print(working_dir + "data/cleaned/" + word + "/" + video + "/" + image)
			imgx = cv2.imread(working_dir + "data/cleaned/" + word + "/" + video + "/" + image,0)
			imgx = imgx/255
			frames.append(imgx)
		if(len(frames) == 0):
			print("Empty frame array continuing..")
			continue
		num_of_videos += 1
		frames = normalize(frames, no_of_frames)
		train_x = train_x + frames
		prediction[index_dict[word]] = 1
		train_y.append(prediction)

	# 	print(word)
	# 	print(len(train_x))
	# 	print(len(train_y[0]))
	# 	print(train_y)
	# # 	break
	# break


#
train_x = np.array(train_x)
train_y = np.array(train_y)
train_x = train_x.reshape(num_of_videos, no_of_frames, 64, 64, 1)
train_y = train_y.reshape(num_of_videos, num_of_words)

with open('data.pickle', "wb") as f:

	data = (train_x, train_y, num_of_words)
	pickle.dump(data, f)








#
# train_x, train_y = shuffle_in_unison_scary(train_x, train_y)
#
# print(train_y)
#
# upper = int(num_of_videos*0.2)
#
# test_x = train_x[0:upper,:,:,:,:]
# test_y = train_y[0:upper, :]
#
# train_x = train_x[upper:,:,:,:,:]
# train_y = train_y[upper:, :]
#

#
#
# print(test_x.shape)
# print(test_y.shape)
#
print(train_x.shape)
print(train_y.shape)
