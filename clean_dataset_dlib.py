import os
import cv2
import numpy as np
from multiprocessing import Pool


# CLEAN_DATA = "/home/ubuntu/cleaned_dataset"
CLEAN_DATA = "/home/jigar/Desktop/cleaned_dataseta"
# UNCLEAN_DATA = "/home/ubuntu/zipped_dataset"
UNCLEAN_DATA = "/home/jigar/Desktop/zipped_dataseta"

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

		self.speaker_dir = filename.split("/")[-3]

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
				self.local_word_repo[word] = VideoFragment(UNCLEAN_DATA +"/"+self.speaker_dir+"/videos/"+ os.path.basename(self.filename)[0:-6] + ".mpg", start,end)

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

	def __init__(self, videos, aligns,speaker):
		# Get all aligns
		self.aligns = aligns

		# Data of all the files
		self.global_word_repo = dict()

		self.read()
		self.extract_frames(f"{CLEAN_DATA}/{speaker}")

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

		# print(self.global_word_repo)

	def extract_frames(self, base_dir):
		for word, video_fragments in self.global_word_repo.items():
			for video_fragment in video_fragments:
				# Issue with creating VideoObject. Getting: Fatal Python error: GC object already tracked
				# After reading 2 video objects. Google isn't helping
				# Tried using video_object.release() but its not working! Looking for a fix
				# This system call solves the issue
				os.system('python3 frame_extractor_dlib.py ' + base_dir + ' ' + word + ' ' + video_fragment.filename + ' ' + str(video_fragment.start_pos) + ' ' + str(video_fragment.end_pos))

def task(dir):
	dir_base_path = os.path.join(UNCLEAN_DATA,dir)

	videos = Reader(os.path.join(dir_base_path,"videos"), 'mpg').get()

	aligns = Reader(os.path.join(dir_base_path,"align"),'align').get()

	WordRepository(videos, aligns,dir)

def driver():

	with Pool(processes = 4) as pool:
		dirs = [dir for dir in os.listdir(UNCLEAN_DATA) if dir not in ["s14","s19","s31"]]
		pool.map(task,dirs)



if __name__ == "__main__":

	driver()



