# naiveBayes.py
# -------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

import util
import classificationMethod
import math

class NaiveBayesClassifier(classificationMethod.ClassificationMethod):
  """
  See the project description for the specifications of the Naive Bayes classifier.
  
  Note that the variable 'datum' in this code refers to a counter of features
  (not to a raw samples.Datum).
  """
  def __init__(self, legalLabels):
    self.legalLabels = legalLabels
    self.type = "naivebayes"
    self.k = 1 # this is the smoothing parameter, ** use it in your train method **
    self.automaticTuning = False # Look at this flag to decide whether to choose k automatically ** use this in your train method **
    
  def setSmoothing(self, k):
    """
    This is used by the main method to change the smoothing parameter before training.
    Do not modify this method.
    """
    self.k = k

  def train(self, trainingData, trainingLabels, validationData, validationLabels):
    """
    Outside shell to call your method. Do not modify this method.
    """  
      
    # might be useful in your code later...
    # this is a list of all features in the training set.
    self.features = list(set([ f for datum in trainingData for f in datum.keys() ]));
    
    if (self.automaticTuning):
        kgrid = [0.001, 0.01, 0.05, 0.1, 0.5, 1, 5, 10, 20, 50]
    else:
        kgrid = [self.k]
        
    self.trainAndTune(trainingData, trainingLabels, validationData, validationLabels, kgrid)


  def trainAndTune(self, trainingData, trainingLabels, validationData, validationLabels, kgrid):
    """
    Trains the classifier by collecting counts over the training data, and
    stores the Laplace smoothed estimates so that they can be used to classify.
    Evaluate each value of k in kgrid to choose the smoothing parameter
    that gives the best accuracy on the held-out validationData.

    trainingData and validationData are lists of feature Counters.  The corresponding
    label lists contain the correct label for each datum.

    To get the list of all possible features or labels, use self.features and
    self.legalLabels.
    """

    cOfY = util.Counter()     # count of instances of Y
    count = util.Counter()    # count of instances of feature (0 or 1) in Y
    self.PEst = util.Counter()     # estimation of the prior distribution
    n = float(len(trainingLabels))
    self.distfeatures = []
    for i in self.legalLabels:
      cOfY[i] = float(trainingLabels.count(i))
      self.PEst[i] = float(cOfY[i]/n)

    # get count of each distinct feature at each pixel
    for i in range(len(trainingData)):
      for feature in trainingData[i]:
        pixel = util.Counter()
        pixel[feature] = trainingData[i][feature]
        if pixel[feature] not in self.distfeatures:
          self.distfeatures.append(pixel[feature])
        count[feature, pixel[feature], trainingLabels[i]] += 1           # counter of number of instances of a feature
                                                                         # at pixel for each y value
    # now we do the predictions with each k
    bestaccuracy = 0
    bestk = 0
    for k in kgrid:
      self.conditionalprob = util.Counter() # this is a dictionary of P(f|y) for all F pixels
      for pixel in tuple(self.features):
        for y in trainingLabels:
          totalCount = 0.0 # this is the denominator of the P(f|y) equation
          for option in self.distfeatures:
            totalCount += count[pixel, option, y]
          for option in self.distfeatures:
              cond = (float(count[pixel, option, y]) + k) / (totalCount + k)
              self.conditionalprob[pixel, option, y] = cond
      # validate
      self.conditionalprob    # maybe normalize here? not sure
      prediction = self.classify(validationData)
      correct = 0
      for m in range(len(validationLabels)):
        if prediction[m]==validationLabels[m]:
          correct+=1
      accuracy = 100.0*correct/len(validationLabels)
      if accuracy>bestaccuracy:
        bestaccuracy = accuracy
        bestk = k
      print "For validation data where k=" + str(k) + " accuracy was " + str(accuracy) + "%"
    print "Best k=" + str(bestk) + " with accuracy " + str(bestaccuracy) + "%"
    self.k = bestk
    # after this we have to compare the prediction results validation labels

  def classify(self, testData):
    """
    Classify the data based on the posterior distribution over labels.

    You shouldn't modify this method.
    """
    guesses = []
    self.posteriors = [] # Log posteriors are stored for later data analysis (autograder).
    for datum in testData:
      posterior = self.calculateLogJointProbabilities(datum)
      guesses.append(posterior.argMax())
      self.posteriors.append(posterior)
    return guesses

  def calculateLogJointProbabilities(self, datum):
    """
    Returns the log-joint distribution over legal labels and the datum.
    Each log-probability should be stored in the log-joint counter, e.g.
    logJoint[3] = <Estimate of log( P(Label = 3, datum) )>

    To get the list of all possible features or labels, use self.features and
    self.legalLabels.
    """
    logJoint = util.Counter()
    for label in self.legalLabels:
      logJoint[label] = math.log(self.PEst[label])     # set up P(y)
      for feature in datum:
          prob = self.conditionalprob[feature, datum[feature], label]  # add log of each conditional probability INCLUDES
          logJoint[label] += math.log(prob)               # 0s AND 1s so maybe here is the problem
    return logJoint
  
  def findHighOddsFeatures(self, label1, label2):
    """
    Returns the 100 best features for the odds ratio:
            P(feature=1 | label1)/P(feature=1 | label2) 
    
    Note: you may find 'self.features' a useful way to loop through all possible features
    """
    featuresOdds = []
       
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

    return featuresOdds


    
      
