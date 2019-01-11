import numpy as np

import h5py
import time
import copy
from random import randint

#Load MNIST data
MNIST_data = h5py.File('F:\CS598\MNISTdata.hdf5', 'r')
x_train = np.float32(MNIST_data['x_train'][:] )
y_train = np.int32(np.array(MNIST_data['y_train'][:, 0]))
x_test = np.float32( MNIST_data['x_test'][:] )
y_test = np.int32( np.array( MNIST_data['y_test'][:,0]))
MNIST_data.close()

#Implementation of stochastic gradient descent algorithm
#number of hidden layers
dH=100
#number of inputs
num_inputs = 28*28
#number of outputs
num_outputs = 10

#initialisation
model = {}
model['W1'] = np.random.randn(dH, num_inputs) / np.sqrt(num_inputs)
model['b1'] = np.zeros(dH)
model['C'] =  np.random.randn(num_outputs, dH) / np.sqrt(dH)
model['b2'] = np.zeros(num_outputs)

model_grads = copy.deepcopy(model)

def softmax_function(z):
    ZZ = np.exp(z)/np.sum(np.exp(z))
    return ZZ

def relu_function(z):
    relu = np.zeros(len(z))
    for i in range(len(z)):
        relu[i] = max(0, z[i])
    return relu

def de_relu(z):
    dlu = np.zeros(len(z))
    for i in range(len(z)):
        if(z[i]>=0):
            dlu[i]=1
        else:
            dlu[i]=0
    return dlu

def backward(x, y, z, h, u, p, model, model_grads):
    p[y] = p[y] - 1
    delta = np.dot(np.transpose(model['C']), p)
    model_grads['C'] = np.dot(p.reshape(len(p),1), h.reshape(1,dH))
    model_grads['b2'] = p
    qb = delta * de_relu(z)
    model_grads['b1'] = qb
    model_grads['W1'] = np.dot(qb.reshape(len(qb), 1), x.reshape(1, num_inputs))
    return model_grads

time1 = time.time()
LR = .01
num_epochs = 20
train_accuracy = np.zeros(num_epochs)

for epochs in range(num_epochs):
#Learning rate schedule
    if (epochs > 5):
        LR = 0.001
    if (epochs > 10):
        LR = 0.0001
    if (epochs > 15):
        LR = 0.00001

    total_correct = 0

    for n in range( len(x_train)):
        n_random = randint(0,len(x_train)-1 )
        y = y_train[n_random]
        x = x_train[n_random][:]
        #Forward Step
        z = np.dot(model['W1'], x) + model['b1']
        h = relu_function(z)
        u = np.dot(model['C'], h) + model['b2']
        p = softmax_function(u)

        prediction = np.argmax(p)
        if (prediction == y):
            total_correct += 1

        model_grads = backward(x, y, z, h, u, p, model, model_grads)
        model['C'] = model['C'] - LR * model_grads['C']
        model['b2'] = model['b2'] - LR * model_grads['b2']
        model['b1'] = model['b1'] - LR * model_grads['b1']
        model['W1'] = model['W1'] - LR * model_grads['W1']
    train_accuracy[epochs] = total_correct / np.float(len(x_train))
    print(train_accuracy[epochs])

time2 = time.time()
print(time2 - time1)
######################################################
# test data
total_correct = 0
for n in range(len(x_test)):
    y = y_test[n]
    x = x_test[n][:]
    z = np.dot(model['W1'], x) + model['b1']
    h = relu_function(z)
    u = np.dot(model['C'], h) + model['b2']
    p = softmax_function(u)

    prediction = np.argmax(p)
    if (prediction == y):
        total_correct += 1
test_accuracy = np.array([total_correct / np.float(len(x_test))])
print(test_accuracy)
######################################################
#output results
import sys
import numpy as np

file_name1 = sys.path[0] + "\\train_accuracy.csv"
file_name2 = sys.path[0] + "\\test_accuracy.csv"
np.savetxt(file_name1, train_accuracy, delimiter=',')
np.savetxt(file_name2, test_accuracy, delimiter=',')











