# Working directories
import os, sys
os.chdir("/home/fs19144/Documents/Personal_Projects/randomchoices/")
sys.path.append('/home/fs19144/Documents/Personal_Projects/randomchoices/')
sys.path.append('/home/fs19144/Documents/Personal_Projects/randomchoices/code')

# Imports
import data_funs as dat
import visualise_funs as vis
import analysis_funs as an

# Read data
survey = dat.read_data()

# Analysis: print interesting statistics/values/percentages 
an.chi_square(survey)
an.deviation_from_expected(survey)

# Visualisations: barcharts, keyboard heatmap, regression and distribution of differences
vis.barcharts(survey)
vis.keyboard_heatmap(survey, htmlname = "keyboard_heatmap")
an.freq_regression(survey, True, htmlname = "freq_regression")
an.same_number(survey, htmlname = "deviation")
