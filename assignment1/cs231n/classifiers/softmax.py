import numpy as np
from random import shuffle

def softmax_loss_naive(W, X, y, reg):
  """
  Softmax loss function, naive implementation (with loops)

  Inputs have dimension D, there are C classes, and we operate on minibatches
  of N examples.

  Inputs:
  - W: A numpy array of shape (D, C) containing weights.
  - X: A numpy array of shape (N, D) containing a minibatch of data.
  - y: A numpy array of shape (N,) containing training labels; y[i] = c means
    that X[i] has label c, where 0 <= c < C.
  - reg: (float) regularization strength

  Returns a tuple of:
  - loss as single float
  - gradient with respect to weights W; an array of same shape as W
  """
  # Initialize the loss and gradient to zero.
  loss = 0.0
  dW = np.zeros_like(W)

  #############################################################################
  # TODO: Compute the softmax loss and its gradient using explicit loops.     #
  # Store the loss in loss and the gradient in dW. If you are not careful     #
  # here, it is easy to run into numeric instability. Don't forget the        #
  # regularization!                                                           #
  #############################################################################

  # compute the loss and the gradient
  num_classes = W.shape[1]
  num_train = X.shape[0]
  for i in range(num_train):
    scores = X[i].dot(W)
    # Fix for numerical stability by subtracting max from score vector.
    shifted_scores = scores - np.max(scores)
    # Calculate loss
    exp_shifted_scores = np.exp(shifted_scores)
    sum_exp_shifted_scores = np.sum(exp_shifted_scores, dtype=np.float64)
    loss += -shifted_scores[y[i]] + np.log(sum_exp_shifted_scores)
    # Calculate gradient
    dW[:, y[i]] -= X[i]
    inv_sum = 1 / sum_exp_shifted_scores
    for j in range(num_classes):
      dW[:, j] += inv_sum*exp_shifted_scores[j]*X[i]

  # Right now the loss is a sum over all training examples, but we want it
  # to be an average instead so we divide by num_train.
  loss /= num_train
  dW /= num_train

  # Add regularization to the loss.
  loss += reg * np.sum(W * W)
  dW += reg * 2 * W

  #############################################################################
  #                          END OF YOUR CODE                                 #
  #############################################################################

  return loss, dW


def softmax_loss_vectorized(W, X, y, reg):
  """
  Softmax loss function, vectorized version.

  Inputs and outputs are the same as softmax_loss_naive.
  """
  # Initialize the loss and gradient to zero.
  loss = 0.0
  dW = np.zeros_like(W)

  #############################################################################
  # TODO: Compute the softmax loss and its gradient using no explicit loops.  #
  # Store the loss in loss and the gradient in dW. If you are not careful     #
  # here, it is easy to run into numeric instability. Don't forget the        #
  # regularization!                                                           #
  #############################################################################
  # Compute the loss and the gradient
  num_classes = W.shape[1]
  num_train = X.shape[0]
  scores = X.dot(W)
  # Calculate loss
  shifted_scores = scores - np.max(scores, axis=1)[:, np.newaxis]
  exp_shifted_scores = np.exp(shifted_scores)
  sum_exp_shifted_scores = np.sum(exp_shifted_scores, dtype=np.float64, axis=1)
  loss = np.mean(-shifted_scores[range(num_train), y] + np.log(sum_exp_shifted_scores))
  loss += reg * np.sum(W * W)
  # Calculate gradient
  inv_sum = 1 / sum_exp_shifted_scores
  coefficients = inv_sum[:,np.newaxis]*exp_shifted_scores
  coefficients[range(num_train), y] -= 1
  dW = X.T.dot(coefficients) / num_train
  dW += reg * 2 * W
  #############################################################################
  #                          END OF YOUR CODE                                 #
  #############################################################################

  return loss, dW

