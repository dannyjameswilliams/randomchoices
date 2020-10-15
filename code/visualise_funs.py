#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  9 15:08:24 2020

@author: fs19144
"""

import plotly.graph_objects as go
import pandas as pd
import numpy as np
from PIL import Image
    
def plotly_bar(x, sums, select = "Scale", col = "red", 
               fname=None, ymax = None):
    
    # Initialise some variables
    n = sum(sums)
    expected_val = sum(sums)/x[len(x)-1]
    
    # hover labels
    labels = sums - expected_val
    labels = np.round(labels, 3)
    labels = list(map(str, labels))
    
    # Set up figure
    fig = go.Figure(data = [go.Bar(
                              x = x, y = sums,
                              hovertext  = labels,
                              hoverlabel = dict(namelength=0),
                              hovertemplate = 'Number chosen: %{x}<br><b>Count: %{y}</b><br>Difference from uniformity: %{hovertext}')
          ])
    
    # Customize design
    fig.update_traces(marker_color=col)
    
    # Y-axis maximum
    if ymax is None:
        ymax = max(sums)
    fig.update_layout(yaxis = dict(range=[0, ymax]))
    
    # Add line of expected value
    fig.add_shape(
            type = "line",
            x0   = 0.5,
            y0   = expected_val,
            x1   = x[len(x)-1] + 0.5,
            y1   = expected_val,
            line = dict(
                color = "grey",
                width = 3.5,
                dash  = "dash"
            ),
    )
    
    # If we are saving the image, then it has different properties
    if fname is not None: 
        
        fig.update_layout(
                xaxis=dict(zeroline=False, showgrid=False), 
                yaxis=dict(zeroline=False, showgrid=False)
                )

        fig.update_layout(
          title_text  = '',
          yaxis_title = "Frequency",
          xaxis_title = "Number",
          template    = "plotly_white" ,
          font=dict(
                family = "Open Sans",
                size   = 18,
                color  = "#34343D"
            )
        )
            
        fig.update_yaxes(
                showticklabels=False,
                tickfont = dict(size = 13)
        )
        fig.update_xaxes(
                ticktext = x,
                tickvals = x,
                tickfont = dict(size = 13)
        )
    
        fig.write_image("plots/" + fname + ".png")
        fig.write_image("plots/svgs/" + fname + ".svg")
        print("Saved plots/{}.png".format(fname))
        
    else:
        
        # Add binomial variance 
        var = n*(1/x[len(x)-1])*(1-(1/x[len(x)-1]))
        fig.add_shape(
                type = "line",
                x0   = 0.5,
                y0   = expected_val + 1.96*var**0.5,
                x1   = x[len(x)-1] + 0.5,
                y1   = expected_val + 1.96*var**0.5,
                line = dict(
                    color = "grey",
                    width = 2,
                    dash  = "dashdot"
                ),
        )
        fig.add_shape(
                type = "line",
                x0   = 0.5,
                y0   = expected_val - 1.96*var**0.5,
                x1   = x[len(x)-1] + 0.5,
                y1   = expected_val - 1.96*var**0.5,
                line = dict(
                    color = "grey",
                    width = 2,
                    dash  = "dashdot"
                ),
        )
        
        # Add x labels and templates
        fig.update_layout(
              title_text  = 'Select a random number between 1 and 10 [' + select + ' selection]',
              yaxis_title = "Frequency",
              xaxis_title = "Selected Number",
              template    = "plotly_white"    
        )

    fig.show()
    
    
        

    
    
def barcharts(survey):
    
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
    
    ymax = np.max(np.hstack((y0_sums, y1_sums)))
    
    plotly_bar(x_1to10, y0_sums, "Scale", "#D0021B", "hist_1to10_1", ymax)
    plotly_bar(x_1to10, y1_sums, "Input", "#8AE8FF", "hist_1to10_2", ymax)
    plotly_bar(x_1to50, y50_sums, "", "#8AE8FF", "hist_1to50", None)   
    
    
def keyboard_heatmap(survey, fname = None):
    
    # Get the third question and total it
    abc = survey.columns[3]
    qwert_totals = survey.groupby(abc).count()
    
    # Create 'Letter' column and order it by keyboard ordering
    qwert_totals["Letter"] = list(qwert_totals.index)
    qwert_totals = qwert_totals.iloc[:,[0, 4]]
    qwert_totals["Letter"] = pd.Categorical(qwert_totals["Letter"],
                                  ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P",
                                    "A", "S", "D", "F", "G", "H", "J", "K", "L",
                                     "Z", "X", "C", "V", "B", "N", "M"]
                                  )
    
    # Sort and convert the array to separate vectors
    qwert_totals = qwert_totals.sort_values("Letter")
    letters = qwert_totals.iloc[:, 1].to_numpy()
    counts = qwert_totals.iloc[:, 0].to_numpy()
    
    # Create matrix for heatmap plot
    qwert_mat = np.vstack((
            np.repeat(counts[0:10], 3),
            np.hstack((0, np.repeat(counts[10:19], 3), 0, 0)),
            np.hstack((np.repeat(0, 2), np.repeat(counts[19:26], 3), np.repeat(0, 7)))
            ))
    
    # Create matrix of labels for hover info
    none_message = "Not a letter!"
    label_mat = np.vstack((
            np.repeat(letters[0:10], 3),
            np.hstack((none_message, np.repeat(letters[10:19], 3), none_message, none_message)),
            np.hstack((np.repeat(none_message, 2), np.repeat(letters[19:26], 3), np.repeat(none_message, 7)))
            ))
    
    # Set up irregular grid in the shape of a keyboard
    biggest_diff = 1
    big_diff = 0.75
    min_diff = 0.25
    x_seq = [min_diff, big_diff, biggest_diff]
    x_along = np.array([0])
    for i in range(10):
        x_along = np.hstack((x_along, np.add(x_seq, i)))
    y_along = [2, 1, 0]

    # Create the heatmap figure, plotting the frequencies on the keyboard grid
    fig = go.Figure(data=go.Heatmap(
              x = x_along,
              y = y_along,
              z = qwert_mat,
              zsmooth = "best",
              type = 'heatmap',
              colorscale = [[0.0, 'rgba(255,255,255,0)'], [1.0, 'blue']],
              hoverongaps = False,
              hovertext = label_mat,
              hoverlabel = dict(namelength=0),
              hovertemplate ='<b>%{hovertext}</b> <br>Times chosen: %{z}'))
    
    # Add the image of the keyboard to the background
    image1 = Image.open("images/keyboard.jpg")
    fig.add_layout_image(
        dict(
            source=image1,
            xref="x",
            yref="y",
            x=0,
            y=2.5,
            sizex=10,
            sizey=3,
            sizing="stretch",
            opacity=1,
            layer="below")
        )
    
    # Add some figure properties
    fig.update_traces(opacity=0.7)
    fig.update_layout(
            template="plotly_white",
            xaxis=dict(zeroline=False, showgrid=False), 
            yaxis=dict(zeroline=False, showgrid=False)
            )
    fig.update_xaxes(showticklabels=False)
    fig.update_yaxes(showticklabels=False)
    
    # Save the figure if filename is present
    if fname is not None: 
        fig.write_image("plots/" + fname + ".png")
        fig.write_image("plots/svgs/" + fname + ".svg", width = 741, height = 360)
        print("Saved plots/{}.png".format(fname))
    
    fig.show()  
    
    
    
    
    
    
    
    
    
    
    
    
    
    