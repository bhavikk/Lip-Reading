import cv2
import time
import os
from os.path import basename, dirname
from config import *
import subprocess
import signal
import dlib

import numpy as np
from scipy.misc import imresize

"""

This is just the initail tinkering with the 40 GB data set downloaded from `http://spandh.dcs.shef.ac.uk/gridcorpus/`


The code in this directory is too naive and far from complete
But it serves the basic purpose of reading video files from one folder and reading transcript from another and align them together

For directory structure look at the screenshots I have uploaded in the screenshot folder

"""


# Util to read files in a directory
class Reader(object):


	def __init__(self, dir, filetype):

		self.dir = dir
		self.filetype = filetype

	def check_filetype(self, filename):
		if filename.endswith(self.filetype):
			return True
		return False

	def get(self):
		# This is a bug! os.listdir doesn't necessarily returns files in any order.
		# It is not guaranteed will get same video file with same align file.
		# Possible fix is to collect in list and sort and then stream it again.
		# Need more thougts
		return (self.dir+'/'+i for i in os.listdir(self.dir) if self.check_filetype(i))

# Object that handles the align file
class AlignObject(object):

	def __init__(self, filename):

		self.filename = filename
		self.align_s = dict()
		self.align_e = dict()

		# Data of just one align file
		self.local_word_repo = dict()

		self.read()

	def read(self):
		with open(self.filename) as f:
			for line in f:
				x = line.split(' ')
				start = round(int(x[0])/1000.0)
				end = round(int(x[1])/1000.0)
				word = x[-1].strip('\n')

				# Make a local list of VideoFragments for the word
				# if word not in self.local_word_repo:
					# self.local_word_repo[x[-1].strip('\n')] = []
				self.local_word_repo[word] = VideoFragment(working_dir + "data/videos/" + basename(self.filename)[0:-6] + ".mpg", start,end)

				self.align_s[start] = word
				self.align_e[end] = word

	def get_starts(self):
		return self.align_s

	def get_ends(self):
		return self.align_e

	def get_word(self, word, pos):

		if pos in self.align_s: return self.align_s[pos]
		return word


# Object that handles the video file
class VideoObject(cv2.VideoCapture):


	def __init__(self, filename):
		super().__init__(filename)

		self.filename = filename

	def get_frame_with_pos(self):
		ret, frame = self.read()
		pos = self.get(cv2.CAP_PROP_POS_FRAMES)

		return frame, pos

# Data Object stores a part of video, corresponds to a word in a video
class VideoFragment(object):

	def __init__(self, filename, start_pos, end_pos):
		self.filename = filename
		self.start_pos = start_pos
		self.end_pos = end_pos

	def __str__(self):
		return "[ " + self.filename + ", " + str(self.start_pos) + ", " + str(self.end_pos) + " ]"

	__repr__ = __str__

# This object reads the alignments and stores all VideoFragments for a word
# It also stores each frame of a word spoken
class WordRepository(object):

	def __init__(self, videos, aligns):
		# Get all aligns
		self.aligns = aligns

		# Data of all the files
		self.global_word_repo = dict()

		self.read()
		self.extract_frames(working_dir + "data/cleaned")

	# Method extract all frames for a given word and writes it in the given location
	# File Format : {base_dir}/{word}/{video_from_which_the_word_is_extracted}/{frame_position}.jpg
	def extract_frames(self, base_dir):
		for word, video_fragments in self.global_word_repo.items():
			for video_fragment in video_fragments:
				# Issue with creating VideoObject. Getting: Fatal Python error: GC object already tracked
				# After reading 2 video objects. Google isn't helping
				# Tried using video_object.release() but its not working! Looking for a fix
				# This system call solves the issue
				os.system(command_python + ' frame_extractor.py ' + base_dir + ' ' + word + ' ' + video_fragment.filename + ' ' + str(video_fragment.start_pos) + ' ' + str(video_fragment.end_pos))




	def read(self):
		while True:
			try:
				align = next(self.aligns)
			except:
				break
				# pass

			align = AlignObject(align)

			for word, fragment in align.local_word_repo.items():
				# Make a global list of word if it does not exist
				if word not in self.global_word_repo:
					self.global_word_repo[word] = []

				self.global_word_repo[word].append(fragment)

		print(self.global_word_repo)

if __name__ == "__main__":
	# Generator for Video files directory
	videos = Reader('./data/videos', 'mpg').get()


	# generator for align file directory
	aligns = Reader('./data/s1/align/','align').get()



	# WordRepository(videos, aligns)
	# Iterating through generator
	# video = next(videos)
	# align = next(aligns)

	#
	# video = next(videos)
	# align = next(aligns)
	#
	#
	#

	# Generator for Video files directory
	videos = Reader('./data/videos', 'mpg').get()


	# generator for align file directory
	aligns = Reader('./data/s1/align/','align').get()

	video = next(videos)
	align = next(aligns)

	video = next(videos)


	# see if it's working
	# print(video)
	# print(align)


	# Create align and video object
	align_obj = AlignObject(align)  
	video_obj = VideoObject(video)





	word = ''

	frames = []
	# loop that prints the video stream
	while True:

		# get frame and it's position
		frame, pos = video_obj.get_frame_with_pos()
		print(pos)


		if frame is None:
			break

		frames.append(frame)

		# break
		# get word for the position
		# word = align_obj.get_word(word, pos)


		# # write word to frame
		# font = cv2.FONT_HERSHEY_SIMPLEX
		# cv2.putText(frame,word,(10,500), font, 4,(255,255,255),2,cv2.LINE_AA)


		# # show frame
		# cv2.imshow('Hello', frame)

		# # wait if q is pressed quit
		# if cv2.waitKey(100) == 'q':
			# break
	# frames = [frame]
	detector = dlib.get_frontal_face_detector()
	predictor = dlib.shape_predictor('./shape_predictor_68_face_landmarks.dat')
	MOUTH_WIDTH = 100
	MOUTH_HEIGHT = 50
	HORIZONTAL_PAD = 0.19
	normalize_ratio = None
	mouth_frames = []
	for frame in frames:
		dets = detector(frame, 1)
		shape = None
		for k, d in enumerate(dets):
			shape = predictor(frame, d)
			i = -1
		if shape is None: # Detector doesn't detect face, just return as is
			print("Some error occured")

		mouth_points = []
		for part in shape.parts():
			i += 1
			if i < 48: # Only take mouth region
				continue
			mouth_points.append((part.x,part.y))
		np_mouth_points = np.array(mouth_points)

		mouth_centroid = np.mean(np_mouth_points[:, -2:], axis=0)

		if normalize_ratio is None:
			mouth_left = np.min(np_mouth_points[:, :-1]) * (1.0 - HORIZONTAL_PAD)
			mouth_right = np.max(np_mouth_points[:, :-1]) * (1.0 + HORIZONTAL_PAD)

			normalize_ratio = MOUTH_WIDTH / float(mouth_right - mouth_left)

		new_img_shape = (int(frame.shape[0] * normalize_ratio), int(frame.shape[1] * normalize_ratio))
		resized_img = imresize(frame, new_img_shape)

		mouth_centroid_norm = mouth_centroid * normalize_ratio

		mouth_l = int(mouth_centroid_norm[0] - MOUTH_WIDTH / 2)
		mouth_r = int(mouth_centroid_norm[0] + MOUTH_WIDTH / 2)
		mouth_t = int(mouth_centroid_norm[1] - MOUTH_HEIGHT / 2)
		mouth_b = int(mouth_centroid_norm[1] + MOUTH_HEIGHT / 2)

		mouth_crop_image = resized_img[mouth_t:mouth_b, mouth_l:mouth_r]

		mouth_frames.append(mouth_crop_image)

	face = np.array(frames)
	mouth = np.array(mouth_frames)




	# set_data(mouth_frames)

	for i in mouth_frames:
		cv2.imshow('andkit lund, jigar chutiya, Bhavikk bhadwa, Chaitya jhatu', i)
		cv2.waitKey(0)

