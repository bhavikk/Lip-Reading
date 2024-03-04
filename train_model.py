from model import createModel
# from generate_dataset import *
import pickle
from pprint import pprint
data = None

with open("data.pickle", "rb") as f:
    data = pickle.load(f)


train_x, train_y, num_of_words = data


#
# pprint(train_x)
# pprint(train_y)

#
# print(train_x)



pickle_out = open("model.pickle","wb")
# data = None
#
# with open()




model = createModel(num_of_words)
model.summary()
model.fit(train_x, train_y, batch_size = 1, epochs = 50,shuffle=True, verbose = 1, validation_split=0.5)
pickle.dump(model, pickle_out)
pickle_out.close()
