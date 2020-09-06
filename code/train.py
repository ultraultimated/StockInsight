from models import build_model
from preprocess import transform_data
import os
import tensorflow as tf
DATA_PATH = '../Data/AAPL.csv'
MODEL_PATH = '../model/'
Xtrain, ytrain = transform_data(DATA_PATH)

md = build_model()

checkpoint_path = MODEL_PATH+"model_0_.ckpt"
checkpoint_dir = os.path.dirname(checkpoint_path)

# Create a callback that saves the model's weights
cp_callback = tf.keras.callbacks.ModelCheckpoint(filepath=checkpoint_path,
                                                 save_weights_only=True,
                                                 verbose=1)

md.fit(x = Xtrain, y = ytrain, batch_size = 32, epochs = 2, callbacks=[cp_callback])
