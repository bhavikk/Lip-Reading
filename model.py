from keras.models import Sequential
from keras.layers.convolutional_recurrent import ConvLSTM2D
from keras.layers.normalization import BatchNormalization
from keras.layers import GlobalAveragePooling2D, Reshape, Dense, Conv3D
# https://github.com/tflearn/tflearn/issues/387

no_of_frames = 3


def createModel(num_of_words):
	seq = Sequential()
	seq.add(ConvLSTM2D(filters=40, kernel_size=(3, 3),activation='relu', input_shape=(no_of_frames, 64, 64, 1), padding='valid', return_sequences=False, dropout=0.2))
	# seq.add(Dropout(0.25))
	# seq.add(BatchNormalization())
	#
	#
	#
	seq.add(ConvLSTM2D(filters=3, kernel_size=(7, 7), padding='same', return_sequences=True))
	# seq.add(Dropout(0.25))
	# seq.add(BatchNormalization())
	#
	seq.add(ConvLSTM2D(filters=40, kernel_size=(3, 3), padding='same', return_sequences=True, dropout=0.25))
	# # seq.add(Dropout(0.25))
	# seq.add(BatchNormalization())

	# seq.add(ConvLSTM2D(filters=3, kernel_size=(3, 3), activation='relu', padding='same', dropout=0.5))
	seq.add(GlobalAveragePooling2D())
	seq.add(Dense(units = num_of_words, activation='softmax'))	
	seq.compile(loss='binary_crossentropy', optimizer='adadelta', metrics=['accuracy'])
	return seq
	