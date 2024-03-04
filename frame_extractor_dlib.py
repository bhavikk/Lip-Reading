import cv2
import sys
from playground import VideoObject
import os
import dlib
import numpy as np
from scipy.misc import imresize


class DlibMouthExtracter(object):

	def __init__(self):
		self.detector = dlib.get_frontal_face_detector()
		self.predictor = dlib.shape_predictor('./shape_predictor_68_face_landmarks.dat')
		self.MOUTH_WIDTH = 100
		self.MOUTH_HEIGHT = 50
		self.HORIZONTAL_PAD = 0.19
		self.normalize_ratio = None

	def extract_mouth(self,frame):
		dets = self.detector(frame, 1)
		shape = None
		for k, d in enumerate(dets):
			shape = self.predictor(frame, d)
			i = -1
		if shape is None: # Detector doesn't detect face, just return as is
			print("HUGA IDUA")
		mouth_points = []
		for part in shape.parts():
			i += 1
			if i < 48: # Only take mouth region
				continue
			mouth_points.append((part.x,part.y))
		np_mouth_points = np.array(mouth_points)

		mouth_centroid = np.mean(np_mouth_points[:, -2:], axis=0)

		if self.normalize_ratio is None:
			mouth_left = np.min(np_mouth_points[:, :-1]) * (1.0 - self.HORIZONTAL_PAD)
			mouth_right = np.max(np_mouth_points[:, :-1]) * (1.0 + self.HORIZONTAL_PAD)

			self.normalize_ratio = self.MOUTH_WIDTH / float(mouth_right - mouth_left)

		new_img_shape = (int(frame.shape[0] * self.normalize_ratio), int(frame.shape[1] * self.normalize_ratio))
		resized_img = imresize(frame, new_img_shape)

		mouth_centroid_norm = mouth_centroid * self.normalize_ratio

		mouth_l = int(mouth_centroid_norm[0] - self.MOUTH_WIDTH / 2)
		mouth_r = int(mouth_centroid_norm[0] + self.MOUTH_WIDTH / 2)
		mouth_t = int(mouth_centroid_norm[1] - self.MOUTH_HEIGHT / 2)
		mouth_b = int(mouth_centroid_norm[1] + self.MOUTH_HEIGHT / 2)

		mouth_crop_image = resized_img[mouth_t:mouth_b, mouth_l:mouth_r]

		return mouth_crop_image

if __name__ == "__main__":
	base_dir = sys.argv[1]
	word = sys.argv[2]
	filename = sys.argv[3]
	start_pos = float(sys.argv[4])
	end_pos = float(sys.argv[5])

	dlib_mouth_extractor = DlibMouthExtracter()

	video_obj = None;
	try:
		video_obj = VideoObject(filename)
		video_obj.set(cv2.CAP_PROP_POS_FRAMES, start_pos)
	except Exception as e:
		print(e)
		print("This file does not exist..", end = " ")
		print(filename)
		exit(0)

	while True:
		# get frame and it's position
		ret, frame = video_obj.read()
		if not ret:
			# Continue if nothing to read
			break

		pos = video_obj.get(cv2.CAP_PROP_POS_FRAMES)
		if(pos >= end_pos):
			# Continue if reached the end
			break

		real_filename = base_dir + "/" + word + "/" + os.path.basename(filename)[0:-4] + "/" + str(pos) + ".jpg"

		# Create directory if not exists
		if not os.path.exists(os.path.dirname(real_filename)):
			os.makedirs(os.path.dirname(real_filename))

		gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		crop_frame = dlib_mouth_extractor.extract_mouth(gray_frame)
		# Write frame
		cv2.imwrite(real_filename, crop_frame)

	# Failed attempt to avoid memory leaks
	video_obj.release()
	print("Completed processing for word: ", end="")
	print(word, end = " ")
	print("In file: ", end = "")
	print(filename)