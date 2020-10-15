#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 13 10:02:35 2020

@author: fs19144
"""
import pandas as pd
import sklearn.linear_model as lm
import plotly.graph_objects as go
import numpy as np
from scipy.stats import chisquare

def freq_regression(survey, plot = True, fname = None):

    # Letter frequencies in English language (obtained from https://www3.nd.edu/~busiforc/handouts/cryptography/letterfrequencies.html)
    letter_freq = pd.DataFrame(
            data = {'letter': ["E", "A", "R", "I", "O", "T", "N", "S", "L", "C", "U", "D", "P", "M", "H", "G", "B", "F", "Y", "W", "K", "V", "X", "Z", "J", "Q"],
                    'Percentage': np.divide([11.1607, 8.4966, 7.5809, 7.5448, 7.1635, 6.9509, 6.6544, 5.7351, 5.4893, 4.5388, 3.6308, 3.3844, 3.1671, 3.0129, 3.0034, 2.4705, 2.0720, 1.8121, 1.7779, 1.2899, 1.1016, 1.0074, 0.2902, 0.2722, 0.1965, 0.1962], 100),
                    'Frequency': [56.88, 43.31, 38.64, 38.45, 36.51, 35.43, 33.92, 29.23, 27.98, 23.13, 18.51, 17.25, 16.14, 15.36, 15.31, 12.59, 10.56, 9.24, 9.06, 6.57, 5.61, 5.13, 1.48, 1.39, 1, 1]
                    }
            )  
    
    # Count number of choices in the survey data
    qwert_totals = survey.groupby(survey.columns[3]).count()
    qwert_totals["letter"] = list(qwert_totals.index)
    qwert_totals = qwert_totals.iloc[:,[0, 4]]
    
    # Sort both data frames in the same order so they can be joined
    letter_freq  = letter_freq.sort_values("letter")
    qwert_totals = qwert_totals.sort_values("letter")
    
    # Join qwert_totals to letter_freq
    letter_freq["choices"] = qwert_totals.iloc[:,0].to_numpy()
    
    # Add squared and cubed terms of frequency
    letter_freq["Percentage_2"] = np.power(letter_freq["Percentage"], 2)
    letter_freq["Percentage_3"] = np.power(letter_freq["Percentage"], 3)
    
    # Fit a linear model 
    fit =  lm.LinearRegression(fit_intercept=True).fit(letter_freq[["Percentage", "Percentage_2", "Percentage_3"]], letter_freq.choices)
    print("Intercept: {}, Gradient: {}, R^2:  {}".format(fit.intercept_, fit.coef_, fit.score(letter_freq[["Percentage", "Percentage_2", "Percentage_3"]], letter_freq["choices"])))
    
    if plot:
        
        # Plotly figure
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=letter_freq["Percentage"], 
                                 y=letter_freq["choices"],
                                 mode='text',
                                 name='markers',
                                 text=letter_freq['letter'],
                                 marker=dict(size=16),
                                 hovertext=letter_freq['letter'],
                                 hoverlabel=dict(namelength=0),
                                 hovertemplate='<b>%{hovertext}</b>'
        ))
        
        # Regression line
        fit_line = [fit.intercept_ + fit.coef_[0]*i + fit.coef_[1]*i**2 + fit.coef_[2]*i**3 for i in letter_freq["Percentage"].to_numpy()]
        o = np.argsort(letter_freq["Percentage"].to_numpy())
        fig.add_trace(go.Scatter(x=letter_freq.Percentage.to_numpy()[o], 
                                 y=np.transpose(fit_line)[o],
                                 mode='lines',
                                 name="",
                                 hovertemplate='Regression Line'
        ))
    
        # text properties
        fig.update_traces(texttemplate='<b>%{text}</b>',
                          textfont_size=25)
    

        # If saving image as svg/png then axes are differently labelled
        if fname is not None: 
            fig.update_layout(
                xaxis_title = "English Language Percentage",
                yaxis_title = "Survey Frequency",
                template    = "plotly_white",
                xaxis_tickformat = '%',
                showlegend  = False,
                xaxis       = dict(zeroline=False, showgrid=False), 
                yaxis       = dict(zeroline=False, showgrid=False),
                font = dict(
                    family = "Open Sans",
                    size   = 18,
                    color  = "#34343D"
                )
            )
             
            fig.write_image("plots/" + fname + ".png")
            fig.write_image("plots/svgs/" + fname + ".svg")
            print("Saved plots/{}.png".format(fname))
        else:
            fig.update_layout(
                xaxis_title = "Letter Percentage in English Words",
                yaxis_title = "Number of Times Picked in Survey",
                template    = "plotly_white",
                xaxis_tickformat = '%',
                showlegend  = False
            ) 
    
        fig.show()
    



def same_number(survey, fname = None):
    
    # Extract choices for pick a number between 1 and 10 questions
    number1    = survey.iloc[:,1]
    number2    = survey.iloc[:,4].astype("int")
    difference = number1 - number2
            
    # Get summary statistics: mean, sd and proportion the same number has been picked
    mean = np.round(np.mean((difference)), 2)
    sd   = np.round(np.std((difference)), 2)
    prop_same = np.round(np.sum(difference == 0)/len(difference), 4)*100

    print("{}% picked the same number.".format(prop_same))
    print("The mean difference between first and second pick is {}, with a SD of {}.".format(mean, sd))
    
    # true uniform
    unif = np.vstack((np.random.randint(1, 11, 10000000), np.random.randint(1, 11, 10000000)))
    unif_diff = (unif[0, :] - unif[1, :])
    print("Truth: Mean {} and SD {}.".format(np.mean(unif_diff), np.std(unif_diff)))
    
    # Get totals of differences
    x    = np.sort(np.unique(difference))
    sums = [(difference == i).sum() for i in x]
        
    # Set up figure
    fig = go.Figure(data=[go.Bar(x=x, y=sums,
                hovertemplate="<b>Choice #1 - Choice #2 = %{x}</b><br>%{y} people's choices gave this")
          ])
    
    # Customize design
    fig.update_traces(marker_color="purple", 
                      marker_line_color='rgb(8,48,107)',
                      marker_line_width=1.5, opacity=0.6)
    
    # Add x labels and templates
    fig.update_layout(
          title_text  = 'Distribution of (Choice #1 - Choice #2)',
          xaxis_title = "Frequency",
          yaxis_title = "Selected Number",
          template    = "plotly_white",
          showlegend  = False
    )

    # Add line of uniformity Irwin-Hall distribution (discrete, n=2, triangle distribution)
    fig.add_trace(go.Scatter(x=list(range(-9, 10)), 
                             y=np.hstack((np.linspace(0, 0.1*len(survey), 10), 
                                          np.linspace(0.1*len(survey), 0, 10)[1:10])),
                             mode='lines',
                             line = dict(color = "black", width = 4),
                             name="",
                             hovertemplate='Irwin-Hall PDF (n=2)'
    ))
    
    if fname is not None: 
            fig.write_image("plots/" + fname + ".png")
            fig.write_image("plots/svgs/" + fname + ".svg")
            print("Saved plots/{}.png".format(fname))
            
    fig.show()



def deviation_from_expected(survey):
    
    # Get data from survey dataframe
    x_1to10 = list(range(1, 11))
    x_1to50 = list(range(1, 51))
    y0  = survey.iloc[:, 1].to_numpy()
    y1  = survey.iloc[:, 4].astype("int").to_numpy()
    y50 = survey.iloc[:, 2].astype("int").to_numpy()
    
    # Sum for each integer (1 to 10 or 1 to 50)
    y0_sums  = [(y0 == i).sum() for i in x_1to10]
    y1_sums  = [(y1 == i).sum() for i in x_1to10]
    y50_sums = [(y50 == i).sum() for i in x_1to50]
    
    # normalise to percentage
    n = sum(y0_sums)
    y0_pers  = y0_sums/n
    y1_pers  = y1_sums/n
    y50_pers = y50_sums/n
    
    # Expected Values
    expected_y0  = sum(y0_pers)/x_1to10[len(x_1to10)-1]
    expected_y1  = sum(y1_pers)/x_1to10[len(x_1to10)-1]
    expected_y50 = sum(y50_pers)/x_1to50[len(x_1to50)-1]
    
    # Differences
    diff_y0  = np.abs(y0_pers - expected_y0)
    diff_y1  = np.abs(y1_pers - expected_y1)
    diff_y50 = np.abs(y50_pers- expected_y50)

    # Proportion difference for 1 and 10
    edge_y0_1 = sum(y0_sums)/x_1to10[len(x_1to10)-1] - y0_sums[0]
    edge_y0_2 = sum(y0_sums)/x_1to10[len(x_1to10)-1] - y0_sums[-1]
    edge_y1_1 = sum(y1_sums)/x_1to10[len(x_1to10)-1] - y1_sums[0]
    edge_y1_2 = sum(y1_sums)/x_1to10[len(x_1to10)-1] - y1_sums[-1]
    
    mean_y0_edge_per = np.mean([edge_y0_1/n*100, edge_y0_2/n*100])
    mean_y1_edge_per = np.mean([edge_y1_1/n*100, edge_y1_2/n*100])

    # Display output
    print("Mean deviation for 1 to 10 QA: {}%".format(np.round(np.mean(diff_y0)*100, 3)))
    print("Mean deviation for 1 to 10 QB: {}%".format(np.round(np.mean(diff_y1)*100, 3)))
    print("Mean deviation for 1 to 50   : {}%".format(np.round(np.mean(diff_y50)*100, 3)))

    print("Mean difference in edges QA {}%".format(np.round(mean_y0_edge_per, 3)))
    print("Mean difference in edges QB {}%".format(np.round(mean_y1_edge_per, 3)))



def chi_square(survey):
    
    # Get data from survey dataframe
    x_1to10 = list(range(1, 11))
    x_1to50 = list(range(1, 51))
    y0  = survey.iloc[:, 1].to_numpy()
    y1  = survey.iloc[:, 4].astype("int").to_numpy()
    y50 = survey.iloc[:, 2].astype("int").to_numpy()

    # Sum for each integer (1 to 10 or 1 to 50)
    y0_sums  = [(y0 == i).sum() for i in x_1to10]
    y1_sums  = [(y1 == i).sum() for i in x_1to10]
    y50_sums = [(y50 == i).sum() for i in x_1to50]
    
    n = sum(y0_sums)
    expected_y   = n/x_1to10[len(x_1to10)-1]
    expected_y50 = n/x_1to50[len(x_1to50)-1]
    
    y0_chi  = chisquare(y0_sums, np.repeat(expected_y, 10))
    y1_chi  = chisquare(y1_sums, np.repeat(expected_y, 10))
    y50_chi = chisquare(y50_sums, np.repeat(expected_y50, 50))

    print("Chi square statitics:")
    print("QA: Val: {}, p-val: {}".format(np.round(y0_chi[0], 3), np.round(y0_chi[1], 7)))
    print("QB: Val: {}, p-val: {}".format(np.round(y1_chi[0], 3), np.round(y1_chi[1], 7)))
    print("1 to 50 Q: Val: {}, p-val: {}".format(np.round(y50_chi[0], 3), np.round(y50_chi[1], 7)))


def analyse_1to50(survey):

    # Extract data    
    x = list(range(1, 51))
    y = survey.iloc[:, 2].astype("int").to_numpy()
    n = len(y)
    sums = [(y == i).sum() for i in x]
    
    # Proportion of people who picked a multiple of 10
    sums10 = np.array(sums)[[i-1 for i in range(10, 60, 10)]]
    print("{}% of people picked a multiple of 10".format(np.round(sum(sums10)/n*100, 2)))

    # Proportion of people who picked a 7 number
    sums7  = np.array(sums)[[i-1 for i in range(7, 57, 10)]]
    print("{}% of people picked a 7 number".format(np.round(sum(sums7)/n*100, 2)))
    
    # Proportion of people who picked the min and max
    min_ind = np.argmin(sums)
    max_ind = np.argmax(sums)
    per_min = np.round(sums[min_ind]/n*100, 2)
    per_max = np.round(sums[max_ind]/n*100, 2)
    print("{}% of people picked {}".format(per_min, x[min_ind]))
    print("{}% of people picked {}".format(per_max, x[max_ind]))
    




















