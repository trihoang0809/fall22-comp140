"""
Sports Analytics
"""

import numeric
import codeskulptor
from urllib import request
import comp140_module6 as sports

def read_matrix(filename):
    """
    Parse data from the file with the given filename into a matrix.

    input:
        - filename: a string representing the name of the file

    returns: a matrix containing the elements in the given file
    """
#read the file    
    url = codeskulptor.file2url(filename)
    file = request.urlopen(url)
    mat_data = []
#decode    
    for line in file.readlines():
        row = line.decode('utf-8')
        nums = row.split(",")
#change the numberrs into floats and add it to the list        
        for idx in range(len(nums)):
            num = float(nums[idx])
            nums[idx] = num
        mat_data.append(nums)
    return numeric.Matrix(mat_data)

class LinearModel:
    """
    A class used to represent a Linear statistical
    model of multiple variables. This model takes
    a vector of input variables and predicts that
    the measured variable will be their weighted sum.
    """

    def __init__(self, weights):
        """
        Create a new LinearModel.

        inputs:
            - weights: an m x 1 matrix of weights
        """
        self._weights = weights

    def __str__(self):
        """
        Return: weights as a human readable string.
        """
        return str(self._weights)

    def get_weights(self):
        """
        Return: the weights associated with the model.
        """
        return self._weights

    def generate_predictions(self, inputs):
        """
        Use this model to predict a matrix of
        measured variables given a matrix of input data.

        inputs:
            - inputs: an n x m matrix of explanatory variables

        Returns: an n x 1 matrix of predictions
        """
        return inputs @ self.get_weights()

    def prediction_error(self, inputs, actual_result):
        """
        Calculate the MSE between the actual measured
        data and the predictions generated by this model
        based on the input data.

        inputs:
            - inputs: inputs: an n x m matrix of explanatory variables
            - actual_result: an n x 1 matrix of the corresponding
                             actual values for the measured variables

        Returns: a float that is the MSE between the generated
        data and the actual data
        """
#find the predictions        
        predictions = self.generate_predictions(inputs)
        numerator = 0
#find the number of rows        
        predictions_shape = predictions.shape()
        rows = predictions_shape[0]
        for row in range(rows):
            numerator += (predictions[(row, 0)] - actual_result[(row, 0)]) ** 2
        mse = numerator / rows
        return mse
    

def fit_least_squares(input_data, output_data):
    """
    Create a Linear Model which predicts the output vector
    given the input matrix with minimal Mean-Squared Error.

    inputs:
        - input_data: an n x m matrix
        - output_data: an n x 1 matrix

    returns: a LinearModel object which has been fit to approximately
    match the data
    """
#implement the given formula
    input_transpose = input_data.transpose()
    xt_x = input_transpose @ input_data
    xt_x_inv = xt_x.inverse()
    xt_x_inv_transpose = xt_x_inv.transpose()
    model = xt_x_inv_transpose @ input_transpose @ output_data
    return LinearModel(model)
    
def soft_threshold(x_val, t_val):
    """
    This function represents the mathematical function for the 'shooting' 
    method, which moves x_val closer to 0 by distance t.
    Inputs:
        - x_val: a floating point number representing the x value
        - t_val: a floating point number representing the distance t
    Output: x_t: a floating point number representing the result of moving
    x closer to 0 by distance t.
    """
#implement the given mathematical function
    x_t = 0
    if x_val > t_val:
        x_t = (x_val - t_val)
    elif abs(x_val) <= t_val:
        x_t = 0
    elif x_val < -t_val:
        x_t = (x_val + t_val)
    return x_t

def fit_lasso(param, iterations, input_data, output_data):
    """
    Create a Linear Model which predicts the output vector
    given the input matrix using the LASSO method.

    inputs:
        - param: a float representing the lambda parameter
        - iterations: an integer representing the number of iterations
        - input_data: an n x m matrix
        - output_data: an n x 1 matrix

    returns: a LinearModel object which has been fit to approximately
    match the data
    """
    weights = fit_least_squares(input_data, output_data)
    weights_matrix = weights.get_weights()
    num = 0
    columns = input_data.shape()[1]
#values in the formula
    x_transpose = input_data.transpose()
    xt_x = x_transpose @ input_data
    xt_y = x_transpose @ output_data
    
    while num < iterations:
        w_old = weights_matrix.copy()
        for row in range(columns):
#calculating a_j            
            second_part_numerator = xt_x.getrow(row) @ weights_matrix
            second_part_numerator00 = second_part_numerator[(0,0)]
            numerator_aj = xt_y[(row, 0)] - second_part_numerator00
            denominator_aj = xt_x[(row,row)]
            a_j = numerator_aj / denominator_aj
#calculating b_j           
            denominator_bj = 2 * (xt_x[(row, row)])
            b_j = param / denominator_bj            
            weights_matrix[(row, 0)] = soft_threshold(weights_matrix[(row, 0)] + a_j, b_j)
#complexity
        if ((weights_matrix - w_old).abs().summation()) < (10**-5):
            break
        num += 1
    return LinearModel(weights_matrix)

def run_experiment(iterations):
    """
    Using some historical data from 1954-2000, as
    training data, generate weights for a Linear Model
    using both the Least-Squares method and the
    LASSO method (with several different lambda values).

    Test each of these models using the historical
    data from 2001-2012 as test data.

    inputs:
        - iterations: an integer representing the number of iterations to use

    Print out the model's prediction error on the two data sets
    """
#create models    
    stat_train = read_matrix("comp140_analytics_baseball.txt")
    win_train = read_matrix("comp140_analytics_wins.txt")
    stat_test = read_matrix("comp140_analytics_baseball_test.txt")
    win_test = read_matrix("comp140_analytics_wins_test.txt")
    training_lse = fit_least_squares(stat_train, win_train)
    training_lasso_1 = fit_lasso(1000, iterations, stat_train, win_train)
    training_lasso_2 = fit_lasso(10000, iterations, stat_train, win_train)
    training_lasso_3 = fit_lasso(100000, iterations, stat_train, win_train)  	
    sports.print_weights(training_lse)
#calculate error on the 1954-2000 data    
    error_lse_train = training_lse.prediction_error(stat_train, win_train)
    error_lasso1_train = training_lasso_1.prediction_error(stat_train, win_train)
    error_lasso2_train = training_lasso_2.prediction_error(stat_train, win_train)
    error_lasso3_train = training_lasso_3.prediction_error(stat_train, win_train)
#calculate error on the 2001-2012 data	
    error_lse_test = training_lse.prediction_error(stat_test, win_test)
    error_lasso1_test = training_lasso_1.prediction_error(stat_test, win_test)
    error_lasso2_test = training_lasso_2.prediction_error(stat_test, win_test)
    error_lasso3_test = training_lasso_3.prediction_error(stat_test, win_test)
#print error
    print("Error on the training data with LSE")
    print(error_lse_train)
    print("======")
    print("Error on the training data with LASSO")
    print(error_lasso1_train)
    print(error_lasso2_train)
    print(error_lasso3_train)
    print("======")
    print("Error on the testing data with LSE")
    print(error_lse_test)
    print("======")
    print("Error on the testing data with LASSO")    
    print(error_lasso1_test)
    print(error_lasso2_test)
    print(error_lasso3_test)

#run_experiment(50)
#sports.print_weights(training_lse)