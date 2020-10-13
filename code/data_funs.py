#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  9 15:09:24 2020

@author: fs19144
"""

import pandas as pd
import numpy as np

def read_data():
    survey = pd.read_csv("data/survey.csv")
    
    # Remove columns with any NaNs
    any_nans = np.repeat(False, np.shape(survey)[0])
    for i in [1, 2, 4]:
        any_nans = any_nans ^ np.isnan(survey.iloc[:,i])    
    survey = survey.loc[~any_nans, :]
    
    # Remove letters that aren't in the alphabet
    upper_letters = [chr(x) for x in range(65, 91)]
    survey.iloc[:, 3] = survey.iloc[:, 3].str.upper()
    letters_in = np.repeat(False, np.shape(survey)[0])
    for i in range(np.shape(survey)[0]):
        letters_in[i] = survey.iloc[i, 3] in upper_letters
    survey = survey.loc[letters_in, :]
    print("{} ({}%) people picked a letter that isn't in the alphabet".format(sum(~letters_in), np.round(sum(~letters_in)/len(~letters_in), 4)*100 ))
    
    # Remove numbers which are decimals
    decimal_inputs = np.repeat(False, np.shape(survey)[0])
    for i in [1, 2, 4]:
        decimal_inputs = decimal_inputs ^ np.round(survey.iloc[:,i]) - survey.iloc[:,i] > 0
    survey = survey.loc[~decimal_inputs, :]
    print("{} ({}%) people picked at least one number as a decimal".format(sum(decimal_inputs), np.round(sum(decimal_inputs)/len(decimal_inputs), 4)*100 ))

    return survey