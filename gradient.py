#TensorFLow can make this
import numpy as np

#Getting some data for our linear regression
data_x = np.linspace(1.0, 10.0, 100)[:, np.newaxis]
data_y = np.sin(data_x) + 0.1*np.power(data_x,2) + 0.5*np.random.randn(100,1)
data_x /= np.max(data_x)

# Take w and b(intercept) in one matrix.
# So we dont have to make a second calculation with b
data_x = np.hstack((np.ones_like(data_x), data_x))

# Random ordering
order = np.random.permutation(len(data_x))
portion = 20
test_x = data_x[order[:portion]]
test_y = data_y[order[:portion]]
train_x = data_x[order[portion:]]
train_y = data_y[order[portion:]]

# w = real price of house. Doing the partial derivitive
# Python uses Fortran in numpy
def  get_gradient(w, x, y):
     y_estimate = x.dot(w).flatten()
     error = (y.flatten() - y_estimate)
     gradient = -(1.0/len(x)) * error.dot(x)
     return gradient, np.pow(error, 2)


w = np.random.randn(2)
alpha = 0.5
tolerance = 1e-5
# Perform Gradient Descent
iterations = 1
while True:
    gradient, error = get_gradient(w, train_x, train_y)
    new_w = w - alpha * gradient

    # Stopping Condition
    if np.sum(abs(new_w - w)) < tolerance:
        print("Converged.")
        break

    # Print error every 50 iterations
    if iterations % 100 == 0:
        print("Iteration: %d - Error: %.4f" %(iterations, error))

    iterations += 1
    w = new_w



