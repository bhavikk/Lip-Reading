from model import createModel
from generate_dataset import *
import pickle

pickle_in = open("model.pickle","rb")

model = pickle.load(pickle_in)





model.summary()
model.fit(train_x, train_y, batch_size = 4, epochs = 4, verbose = 1)
pickle.dump(model, pickle_out)
pickle_out.close()
