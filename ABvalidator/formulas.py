from scipy.stats import binom, chi2
from scipy import stats
from sklearn.utils import resample

import statsmodels.api as sm
import math, statistics
import pandas as pd
import numpy as np



def isRatioSignificantlyCorrect(variant_users, total_users, division, threshold):
    alpha = threshold #significance p-value
    
    lower_bound, upper_bound = binom.interval(1 - alpha, total_users, division)
    
    isSig = (variant_users > lower_bound and variant_users < upper_bound)

    return isSig, lower_bound, upper_bound

def srmTest(df):
	#formula in: https://github.com/ernstmul/ABvalidator/docs/data_quality.md
	chi_sum = 0
	total_users = df[0].sum()

	for index, row in df.iterrows():
		O = row[0] 					# Observed user count
		E = total_users * row[1]	# Expected user count

		chi_sum += ((O - E)**2) / E

		
	p = 1 - chi2.cdf(chi_sum, 1)
	return p

def noveltyTest(variant_list):
	#formula in https://github.com/ernstmul/ABvalidator/docs/novelty_effect.md

	r2 = computeNoveltyRegression(variant_list)

	#check if R2 meets threshold
	if r2 >= 0.8:
		#so check if monotonic
		if isMonotonic(variant_list):
			return True

	return False


def computeNoveltyRegression(variant_list):
    number_of_intervals = len(variant_list)
   
    X = getIndependentVariables(number_of_intervals)
    y = getDependentVariable(variant_list)

    model = sm.OLS(y, X).fit()
    predictions = model.predict(X)    

    return model.rsquared	

def getDependentVariable(variant_list):
    data = {"y":variant_list} 

    return pd.DataFrame(data)        

def getIndependentVariables(number_of_days):
    data = {"x1": [], "x2": []}
    for t in range(1, (number_of_days + 1)):
        data['x1'].append((1/(math.pow(t,0.35))))
        data['x2'].append((1/(math.pow(t,2)))) 

    return pd.DataFrame(data) 

def isMonotonic(variant_list):

	if len(variant_list) < 2:
		return False #no novelty effect detectable when less than 2 intervals

	if variant_list[0] < variant_list[1]:
		trend = "up"
	else:
		trend = "down"

	previous = None
	for value in variant_list:
		if previous is None:
			previous = value
		elif trend == "up" and value <= previous:
			return False
		elif trend == "down" and value >= previous:
			return False	
		else:
			previous = value
	
	return True	

def detect_outliers(variant_list):
	threshold = 3 # Any Z score greater than 3, or less than -3 is considered an outlier

	z = np.abs(stats.zscore(variant_list))	
	outliers = np.where(z > threshold)

	return outliers[0]	

def calculateStdViaBootstrapMethod(variant_list):

    sample_size = int(round(len(variant_list) * 0.8))
    boot = resample(variant_list, replace=True, n_samples=sample_size, random_state=1)
    return np.std(boot)  	

def calculateMinimalSampleSize(std, change_percentage, variant_list):
	#formula from paper
    denominator = (math.pow(change_percentage * statistics.mean(variant_list), 2))

    if denominator == 0:
        return 0

    #compute rest of formula    
    n = (16 * math.pow(std,2)) / denominator

    return int(math.floor(n))    		
						

