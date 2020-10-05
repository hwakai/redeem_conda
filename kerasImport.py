#import plaidml.keras
#plaidml.keras.install_backend()
import keras
print(keras.backend.backend())
from keras.models import model_from_json
from keras.layers import Input
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import Activation
from keras.layers import BatchNormalization
from keras.models import Model
from keras.callbacks import EarlyStopping
from keras.utils.np_utils import to_categorical
from keras.wrappers.scikit_learn import KerasRegressor
from keras.layers import LeakyReLU
from keras import initializers
from keras import callbacks
from keras.utils import plot_model
