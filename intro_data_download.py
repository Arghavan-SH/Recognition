# -*- coding: utf-8 -*-
"""intro. data download.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1KdF2hcAbdx8IaXhkAHOG_I5t_oZN-DZq
"""

from google.colab import drive
drive.mount('/gdrive')

ls /gdrive/My\ Drive/notebooks/

cd /gdrive/My\ Drive/

ls

pwd

!wget https://repod.pon.edu.pl/dataset/23e5fd6f-bcd1-4958-95fc-eb09acf0a2fc/resource/8db9b107-0c78-4d8d-971f-5e86022bd87d/download/subject2.mat

ls ../../dataset

ls /content/*

cd /gdrive/My\ Drive/notebooks/vafaei

ls ../../dataset

"""# You will need to read from here:"""

from google.colab import drive
drive.mount('/gdrive')

cd /gdrive/My\ Drive/notebooks/vafaei

import h5py
from scipy.io import loadmat
import numpy as np
import pylab as plt

f1 = h5py.File('../../dataset/subject1.mat', 'r')
# print(f.keys())

f2 = h5py.File('../../dataset/subject2.mat', 'r')
# print(f.keys())

list(f1.items())

list(f1['Data'].items())

# a = list(f1['Data']['Category'])[0]

# for i in f['#refs#']

# help(f['#refs#'])

data = []
for f in [f1,f2]:
    for key in list(f['#refs#'].keys()):
        ddd = f['#refs#'][key]
        if(ddd.shape==(64, 1201, 306)):
            data.append(ddd)
del ddd

y = []
for i in range(24):
    for j in range(64):
        y.append(i)
y = np.array(y)

# pca = sklearn.decomposition.PCA()

Xp = np.concatenate(data,axis=0)
del data

Xp = np.swapaxes(Xp,1,2)

Xp.shape

for i in range(3072):
    for j in range(306):
        Xp[i,j,:601] = np.real(np.fft.rfft(Xp[i,j,:]))
Xp = Xp[:,:,:601]







X = Xp[:,:,:1000:10].reshape(1536,-1)#[:,:1000]

inds = np.arange(X.shape[0])

inds

np.random.shuffle(inds)

inds

X.shape

X_train = X[inds[:1000]]
y_train = y[inds[:1000]]
X_test = X[inds[1000:]]
y_test = y[inds[1000:]]
print(X_train.shape,y_train.shape,X_test.shape,y_test.shape)

from sklearn.ensemble import RandomForestClassifier as RFC

rfc = RFC(n_estimators=100)

rfc.fit(X_train,y_train)

rfc.score(X_test,y_test)

"""# Now lets' see how changing the window can make a difference."""

for i in range(0,1201,10):

    X = Xp[:,i:i+10,:].reshape(1536,-1)
    inds = np.arange(X.shape[0])
    np.random.shuffle(inds)

    X_train = X[inds[:1000]]
    y_train = y[inds[:1000]]
    X_test = X[inds[1000:]]
    y_test = y[inds[1000:]]

    rfc = RFC(n_estimators=20)
    rfc.fit(X_train,y_train)
    acc = rfc.score(X_test,y_test)
    print('window time is between {} and {}, acc is {}'.format(i,i+10,acc))

"""# CNN"""

X = Xp+0
inds = np.arange(X.shape[0])
np.random.shuffle(inds)

X_train = X[inds[:1000]]
y_train = y[inds[:1000]]
X_test = X[inds[1000:]]
y_test = y[inds[1000:]]


xmax = X.max()
X_train = X_train.astype('float32')
X_test = X_test.astype('float32')
X_train /= xmax
X_test /= xmax
del X


n_train, img_rows, img_cols = X_train.shape
X_train = X_train.reshape(n_train, img_rows, img_cols, 1)
n_test, img_rows, img_cols = X_test.shape
X_test = X_test.reshape(n_test, img_rows, img_cols, 1)
input_shape = (img_rows, img_cols, 1)

def indices_to_one_hot(data, nb_classes):
    """Convert an iterable of indices to one-hot encoded labels."""
    targets = np.array(data).reshape(-1)
    return np.eye(nb_classes)[targets]

y_train = indices_to_one_hot(y_train, 24)
y_test = indices_to_one_hot(y_test, 24)

print('x_train shape:', X_train.shape)
print(X_train.shape[0], 'train samples')
print(X_test.shape[0], 'test samples')
print(X_train.shape,y_train.shape,X_test.shape,y_test.shape)

# from sklearn.preprocessing import OneHotEncoder
# enc = OneHotEncoder()
# y_train2 = enc.fit_transform(y_train)
# print(y_train2.shape)

from __future__ import print_function
import keras
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras import backend as K

model = Sequential()
model.add(Conv2D(8, kernel_size=(3, 3),
                 activation='relu',
                 input_shape=input_shape,
                 padding='same'))
model.add(Conv2D(16, (3, 3), activation='relu',padding='same'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Conv2D(16, (3, 3), activation='relu',padding='same'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Conv2D(16, (3, 3), activation='relu',padding='same'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Conv2D(32, (3, 3), activation='relu',padding='same'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Conv2D(32, (3, 3), activation='relu',padding='same'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Conv2D(16, (3, 3), activation='relu',padding='same'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Dropout(0.25))
model.add(Flatten())
model.add(Dense(128, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(num_classes, activation='softmax'))

model.compile(loss=keras.losses.categorical_crossentropy,
              optimizer=keras.optimizers.Adadelta(),
              metrics=['accuracy'])
model.summary()

batch_size = 2
epochs = 10
model.fit(X_train, y_train,
          batch_size=batch_size,
          epochs=epochs,
          verbose=1,
          validation_data=(X_test, y_test))
score = model.evaluate(X_test, y_test, verbose=0)
print('Test loss:', score[0])
print('Test accuracy:', score[1])





dd = loadmat('../../dataset/subject1.mat')













sample = np.array(f['#refs#']['3b'])#.__array__()

sample.shape

plt.plot(sample[0,0,:])

