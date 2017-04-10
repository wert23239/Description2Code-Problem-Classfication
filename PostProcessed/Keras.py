import numpy as np
np.random.seed(123)  # for reproducibility
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Convolution2D, MaxPooling2D, normalization
from keras.utils import np_utils
from keras.datasets import mnist, cifar10
from keras.layers.advanced_activations import LeakyReLU
from sklearn.decomposition import PCA

Train = False

# Basic Prepocess function for MNIST
# Uses PCA and Normalization
def pca_mnist(X, X_test):
    X = X.astype('float32') / 255.
    X_test = X_test.astype('float32') / 255.
    X = X.reshape((len(X), np.prod(X.shape[1:])))
    X_test = X_test.reshape((len(X_test), np.prod(X_test.shape[1:])))
    print(X.shape)
    pca = PCA(n_components=100)
    pca.fit(X)
    X = pca.inverse_transform(pca.transform(X))
    X_test = pca.inverse_transform(pca.transform(X_test))
    X = X.reshape(X.shape[0], 1, 28, 28)
    X_test = X_test.reshape(X_test.shape[0], 1, 28, 28)
    print(X.shape)
    return X, X_test

#Preprocess for cifar10
#Doesn't really affect performance
def pca_cifar_pre(X):
    X2 = np.transpose(X, (3, 0, 1, 2))
    temp1 = 0
    temp2 = 0
    temp3 = 0
    for i in range(3): #individual PCA for each color 
        temp_X = X2[i][:][:][:]
        temp_X = np.transpose(temp_X, (0, 2, 1))
        temp_X = pca_cifar(temp_X)
        if i == 0:
            temp1 = temp_X
        elif i == 1:
            temp2 = temp_X
        else:
            temp3 = temp_X
    X_temp = np.array([temp1, temp2, temp3])
    # print(X.shape)
    X = np.transpose(X, (1, 2, 3, 0))
    X = X.astype('float32') / 255.
    X = X.reshape(X.shape[0], 3, 32, 32)
    return X


def pca_cifar(X):
    X = X.astype('float32') / 255.
    X = X.reshape((len(X), np.prod(X.shape[1:])))
    print(X.shape)
    pca = PCA(n_components=1024)
    pca.fit(X)
    X = pca.inverse_transform(pca.transform(X))
    X = X.reshape(X.shape[0], 32, 32)
    print(X.shape)
    return X


# Load data depedent on the data set
if Train == True:
    (X_train, y_train), (X_test, y_test) = mnist.load_data()
if Train == False:
    (X_train, y_train), (X_test, y_test) = cifar10.load_data()
print(X_train.shape)

# 5. Preprocess input data PCA here
if Train == True:
    X_train, X_test = pca_mnist(X_train, X_test)
else:
    X_train = pca_cifar_pre(X_train)
    X_test = pca_cifar_pre(X_test)

# 6. Preprocess class labels
Y_train = np_utils.to_categorical(y_train, 10)
Y_test = np_utils.to_categorical(y_test, 10)

# 7. Define model architecture
model = Sequential()

if Train == True: #Add init layer based on image demensions 
    model.add(Convolution2D(64, 5, 5, activation='relu',
                            input_shape=(1, 28, 28), dim_ordering='th'))
else:
    model.add(Convolution2D(64, 5, 5, activation='relu',
                            input_shape=(3, 32, 32), dim_ordering='th'))

print(model.output_shape)
model.add(Convolution2D(64, 5, 5, activation='linear')) #Convolutinal Leaky Layer
model.add(LeakyReLU(alpha=.001))
print(model.output_shape)
model.add(MaxPooling2D(pool_size=(2, 2))) #Vanila Pooling
print(model.output_shape)
model.add(Dropout(0.25))

model.add(Flatten())
print(model.output_shape)
model.add(Dense(128, activation='relu'))
print(model.output_shape)
model.add(Dropout(0.5))
model.add(Dense(10, activation='softmax'))


model.summary

#Compile model
model.compile(loss='categorical_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])
    
#Fit model on training data
model.fit(X_train, Y_train, batch_size=32, nb_epoch=20, verbose=1)


#Evaluate model on test data
score = model.evaluate(X_test, Y_test, verbose=1)
print(score)
