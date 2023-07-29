import pickle
from tensorflow import keras
from keras.optimizers import Adam
from keras.layers import Dense
import numpy as np
from sklearn.preprocessing import MinMaxScaler

with open('chef_data.pickle', 'rb') as f:
    (x_train, y_train), (x_test, y_test) = pickle.load(f)

# Sources:
# https://stackoverflow.com/questions/29661574/normalize-numpy-array-columns-in-python
# https://numpy.org/doc/stable/reference/generated/numpy.matrix.std.html
# https://stackoverflow.com/questions/38179248/absolute-difference-of-two-numpy-arrays
# https://machinelearningmastery.com/how-to-transform-target-variables-for-regression-with-scikit-learn/
# Reference regression sample code from the class lecture.
# Received help from Pablo on how to use Keras.

# The input size
num_inputs = 20
# The output size
num_outputs = 4
# The number of epochs
num_epochs = 100
# The batch size
batch_size = 8

# Scale the output values to a [0, 1] range
scalar = MinMaxScaler()
scalar.fit(y_train)

# Scale the output values for the training set
y_train = scalar.transform(y_train)
# Scale the output values for the test set
y_test = scalar.transform(y_test)

# Add a single layer with linear activation, which means no transforms applied. This corresponds to linear regression.
# The input layer for the network
input_layer = keras.Input(shape=num_inputs, name='input_layer')
hidden_layer1 = Dense(units=50, activation="relu", name="hidden_layer1")(input_layer)
# The output layer for the network
output_layer = Dense(num_outputs, activation='relu', name='output_layer')(hidden_layer1)

# Build the model
model = keras.Model(inputs=input_layer, outputs=output_layer)

# Compile the model
model.compile(loss='mse', optimizer=Adam(), metrics=['mse'])

# Print the model summary
model.summary()

# Train the model
history = model.fit(x_train, y_train, batch_size=batch_size, epochs=num_epochs, verbose=2, validation_data=(x_test, y_test))

# Check the classification performance of the trained network on the test data 
final_train_loss, final_train_accuracy = model.evaluate(x_train, y_train, verbose=0)
final_test_loss, final_test_accuracy = model.evaluate(x_test, y_test, verbose=0)

# Make predictions using the test data
prediction = model.predict(x_test)

# Rescale the output values back their original ranges. 
prediction = scalar.inverse_transform(prediction)
y_test = scalar.inverse_transform(y_test)

# Find the difference between the test data and the predictions
diff = np.absolute(np.array(y_test) - np.array(prediction))
# Calculate the standard deviation for the calculated error
std = diff.std(0)

# Print number of epochs used
print('Number of epochs used:', num_epochs)
# Batch size used
print('Batch size used:', batch_size)
# Print activation function
print('Activation function: mean square error')
# Print training loss
print('Final training loss (mean square error):', final_train_loss)
# Print test loss
print('Final test loss (mean square error):', final_test_loss)
# Print standard deviation
print('Standard deviation between test and prediction:', std)