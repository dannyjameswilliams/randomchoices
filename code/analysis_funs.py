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

def freq_regression(survey, plot = True):

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
    
        # Plot properties
        fig.update_layout(
            xaxis_title = "Letter Percentage in English Words",
            yaxis_title = "Number of Times Picked in Survey",
            template = "plotly_white",
            xaxis_tickformat = '%',
            showlegend=False
        )
        
        fig.show()
    



def same_number(survey):
    
    # Extract 
    number1    = survey.iloc[:,1]
    number2    = survey.iloc[:,4].astype("int")
    difference = number1 - number2
            
    
    mean = np.round(np.mean(np.abs(difference)), 2)
    sd   = np.round(np.std(np.abs(difference)), 2)
    prop_same = np.round(np.sum(difference == 0)/len(difference), 4)*100

    print("{}% picked the same number.".format(prop_same))
    print("The mean difference between first and second pick is {}, with a SD of {}.".format(mean, sd))
    

    x = np.sort(np.unique(difference))
    sums = [(difference == i).sum() for i in x]
        
    # Set up figure
    fig = go.Figure(data=[go.Bar(x=x, y=sums,
                hovertemplate="<b>Choice #1 - Choice #2 = %{x}</b><br>%{y} people's choices gave this")
          ])
    
    # Customize design
    fig.update_traces(marker_color="purple", marker_line_color='rgb(8,48,107)',
                      marker_line_width=1.5, opacity=0.6)
    
    # Add x labels and templates
    fig.update_layout(
          title_text  ='Distribution of (Choice #1 - Choice #2)',
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
    
    fig.show()
         
    return prop_same - mean - sd













