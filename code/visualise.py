#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  9 15:40:26 2020

@author: fs19144
"""
import os, sys
os.chdir("/home/fs19144/Documents/Personal_Projects/randomchoices/")
sys.path.append('/home/fs19144/Documents/Personal_Projects/randomchoices/')
sys.path.append('/home/fs19144/Documents/Personal_Projects/randomchoices/code')
print(os.getcwd())

import data_funs as dat
import visualise_funs as vis
import analysis_funs as an

survey = dat.read_data()
# vis.histograms_1to10(survey)
#vis.barcharts_1to10(survey)

# vis.test_heatmap()
# vis.keyboard_heatmap(survey)

#an.freq_regression(survey, True)
an.same_number(survey)