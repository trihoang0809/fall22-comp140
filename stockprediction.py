"""
Stock market prediction using Markov chains.

For each function, replace the return statement with your code.  Add
whatever helper functions you deem necessary.
"""

import comp140_module3 as stocks
from collections import defaultdict
import random

### Model

def markov_chain(data, order):
    """
    Create a Markov chain with the given order from the given data.

    inputs:
        - data: a list of ints or floats representing previously collected data
        - order: an integer repesenting the desired order of the markov chain

    returns: a dictionary that represents the Markov chain
    """
#create a default dictionary    
    chain = defaultdict(dict)
#idx represent the index of the bin after a state    
    for idx in range(order, len(data)):
        next_bin = data[idx]
#find the state, which is represented by a tuple containing 'order' 
#elements
        chain_key = ()
        for num in range(order):
            chain_key = chain_key + (data[idx - order + num],)
#if the next_bin is in the chain_value, add 1 to the value of 
#that bin; if it's not in yet then set it to 1; -> values in 
#the chain_value dictionary are currently the number of times 
#that bin appears after the state
        chain_value = chain[chain_key]
        if next_bin in chain_value:
            chain_value[next_bin] += 1
        else:
            chain_value[next_bin] = 1
#go through the chain dictionary and change the values in each 
#chain_value dictionary to the probabilities of the corresponding key 
#being the next bin.
    for chain_val in chain.values():
        total = sum(chain_val.values())
        for nextbin in chain_val:
            chain_val[nextbin] = chain_val[nextbin] / total
    return chain
         
             

### Predict

def predict(model, last, num):
    """
    Predict the next num values given the model and the last values.

    inputs:
        - model: a dictionary representing a Markov chain
        - last: a list (with length of the order of the Markov chain)
                representing the previous states
        - num: an integer representing the number of desired future states

    returns: a list of integers that are the next num states
    """
    next_states = []
#iterate num times to find the next num predictions
    for dummy in range(num):
        key = tuple(last)
#if key is in the given model, use the probabilities of the Markov chain 
#to predict the next state; otherwise, all states 0-3 have equal 
#probabilities -> use random.randint
        if key in model:
            possibilities = model[key]
#create a new dictionary whose values are tuples of two elements 
#representing the probabilities of the next state being in that key. 
#The first and the second value of that tuple represent the range
#for example: probabilities = {1: (0, 0.66), 3: (0.66, 1)}
            probabilities = {}
            counter = 0
            for pos_key, pos_value in possibilities.items():
                probabilities[pos_key] = (counter, counter + pos_value)
                counter += pos_value
#generate a random number between 0 and 1; go through the keys and 
#values of the probabilities list and append the key whose value is the
#range that includes the random number to the next_states list.
            rand = random.random()
            for pro_key, pro_value in probabilities.items():
                if pro_value[0] <= rand < pro_value[1]:
                    next_states.append(pro_key)
        else:
            next_states.append(random.randint(0, 3))
#the latest list of data is updated after adding a predicted state 
#before making the next prediction
        last = last[1:] + [next_states[-1]]
    return next_states
                


### Error

def mse(result, expected):
    """
    Calculate the mean squared error between two data sets.

    The length of the inputs, result and expected, must be the same.

    inputs:
        - result: a list of integers or floats representing the actual output
        - expected: a list of integers or floats representing the predicted output

    returns: a float that is the mean squared error between the two data sets
    """
#mse = sum of the square of every difference between the predicted and 
#the actual result / the number of elements in the list
#->iterate through each index and find the square of the difference 
#between the expected and the actual output at that index and add them 
#up.
    numerator = 0
    for idx in range(len(result)):
        numerator += (expected[idx] - result[idx]) ** 2
    return numerator / len(result)


### Experiment

def run_experiment(train, order, test, future, actual, trials):
    """
    Run an experiment to predict the future of the test
    data given the training data.

    inputs:
        - train: a list of integers representing past stock price data
        - order: an integer representing the order of the markov chain
                 that will be used
        - test: a list of integers of length "order" representing past
                stock price data (different time period than "train")
        - future: an integer representing the number of future days to
                  predict
        - actual: a list representing the actual results for the next
                  "future" days
        - trials: an integer representing the number of trials to run

    returns: a float that is the mean squared error over the number of trials
    """
#sum up all the mean squared error after 'trials' experiments; divide 
#that by 'trials' -> average mean squared error
    error = 0
    for dummy in range(trials):
        predicted = predict(markov_chain(train, order), test, future)
        error += mse(actual, predicted) 
    return error / trials


### Application

def run():
    """
    Run application.

    You do not need to modify any code in this function.  You should
    feel free to look it over and understand it, though.
    """
    # Get the supported stock symbols
    symbols = stocks.get_supported_symbols()

    # Get stock data and process it

    # Training data
    changes = {}
    bins = {}
    for symbol in symbols:
        prices = stocks.get_historical_prices(symbol)
        changes[symbol] = stocks.compute_daily_change(prices)
        bins[symbol] = stocks.bin_daily_changes(changes[symbol])

    # Test data
    testchanges = {}
    testbins = {}
    for symbol in symbols:
        testprices = stocks.get_test_prices(symbol)
        testchanges[symbol] = stocks.compute_daily_change(testprices)
        testbins[symbol] = stocks.bin_daily_changes(testchanges[symbol])

    # Display data
    #   Comment these 2 lines out if you don't want to see the plots
    stocks.plot_daily_change(changes)
    stocks.plot_bin_histogram(bins)

    # Run experiments
    orders = [1, 3, 5, 7, 9]
    ntrials = 500
    days = 5

    for symbol in symbols:
        print(symbol)
        print("====")
        print("Actual:", testbins[symbol][-days:])
        for order in orders:
            error = run_experiment(bins[symbol], order,
                                   testbins[symbol][-order-days:-days], days,
                                   testbins[symbol][-days:], ntrials)
            print("Order", order, ":", error)
        print()

# You might want to comment out the call to run while you are
# developing your code.  Uncomment it when you are ready to run your
# code on the provided data.

#run()
