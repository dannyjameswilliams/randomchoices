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

def histograms_1to10(survey):


    x0 = survey.iloc[:, 1].to_numpy()
    x1 = survey.iloc[:, 4].astype("int").to_numpy()
    
    fig = go.Figure()
    fig.add_trace(go.Histogram(x=x0))
    fig.add_trace(go.Histogram(x=x1))
    
    # Overlay both histograms
    fig.update_layout(
        barmode='overlay',
        xaxis_title = "Frequency",
        yaxis_title = "Selected Number",
        template = "plotly_white"    
    )
    
    # Reduce opacity to see both histograms
    fig.update_traces(opacity=0.5)
    fig.show()
    
def barcharts_1to10(survey):
    
    # Get data and labels
    x = list(range(1, 11))
    y0 = survey.iloc[:, 1].to_numpy()
    y1 = survey.iloc[:, 4].astype("int").to_numpy()
    y0_sums = [(y0 == i).sum() for i in range(1,11)]
    y1_sums = [(y1 == i).sum() for i in range(1,11)]
    
    def plotly_bar(x, sums, select = "Scale", col = "red"):
        # hover labels
        labels = sums/sum(sums) - (1/10)
        labels = np.round(labels, 3)
        labels = list(map(str, labels))
        
        # Set up figure
        fig = go.Figure(data=[go.Bar(x=x, y=sums,
                    hovertext=labels,
                    hoverlabel=dict(namelength=0),
                    hovertemplate='Number chosen: %{x}<br><b>Count: %{y}</b><br>Difference from uniformity: %{hovertext}')
              ])
        
        # Customize design
        fig.update_traces(marker_color=col, marker_line_color='rgb(8,48,107)',
                          marker_line_width=1.5, opacity=0.6)
        
        # Add x labels and templates
        fig.update_layout(
              title_text='Select a random number between 1 and 10 [' + select + ' selection]',
              xaxis_title = "Frequency",
              yaxis_title = "Selected Number",
              template = "plotly_white"    
        )
        
        # Add line of uniformity
        fig.update_layout(shapes = [
                dict(
                    type = "line",
                    xref = 'paper', x0 = 0, x1 = 1,
                    yref = 'y', y0 = sum(sums)/10, y1 = sum(sums)/10
                )
                ])
        fig.show()
    
    plotly_bar(x, y0_sums, "Scale", "red")
    plotly_bar(x, y1_sums, "Input", "blue")
    
    
    
def test_heatmap():
    # Build the rectangles as a heatmap
    # specify the edges of the heatmap squares
    phi = (1 + np.sqrt(5) )/2. # golden ratio
    xe = [0, 1, 1+(1/(phi**4)), 1+(1/(phi**3)), phi]
    ye = [0, 1/(phi**3), 1/phi**3+1/phi**4, 1/(phi**2), 1]
    
    z = [ [13,3,3,5],
          [13,2,1,5],
          [13,10,11,12],
          [13,8,8,8]
        ]
    
    fig = go.Figure(data=go.Heatmap(
              x = np.sort(xe),
              y = np.sort(ye),
              z = z,
              type = 'heatmap',
              colorscale = 'Viridis'))
    fig.show()
    
    
    
    
def keyboard_heatmap(survey):
    
    abc = survey.columns[3]
    qwert_totals = survey.groupby(abc).count()
    qwert_totals["Letter"] = list(qwert_totals.index)
    qwert_totals = qwert_totals.iloc[:,[0, 4]]
    qwert_totals["Letter"] = pd.Categorical(qwert_totals["Letter"],
                                  ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P",
                                    "A", "S", "D", "F", "G", "H", "J", "K", "L",
                                     "Z", "X", "C", "V", "B", "N", "M"]
                                  )
    qwert_totals = qwert_totals.sort_values("Letter")
    letters = qwert_totals.iloc[:, 1].to_numpy()
    counts = qwert_totals.iloc[:, 0].to_numpy()
    
    qwert_mat = np.vstack((
            np.repeat(counts[0:10], 3),
            np.hstack((0, np.repeat(counts[10:19], 3), 0, 0)),
            np.hstack((np.repeat(0, 2), np.repeat(counts[19:26], 3), np.repeat(0, 7)))
            ))
    
    none_message = "Not a letter!"
    label_mat = np.vstack((
            np.repeat(letters[0:10], 3),
            np.hstack((none_message, np.repeat(letters[10:19], 3), none_message, none_message)),
            np.hstack((np.repeat(none_message, 2), np.repeat(letters[19:26], 3), np.repeat(none_message, 7)))
            ))
    
    
    biggest_diff = 1
    big_diff = 0.75
    min_diff = 0.25
    # key_diff = 0.1
    
    x_seq = [min_diff, big_diff, biggest_diff]
    x_along = np.array([0])
    for i in range(10):
        x_along = np.hstack((x_along, np.add(x_seq, i)))
    y_along = [2, 1, 0]
    
    fig = go.Figure(data=go.Heatmap(
              x = x_along,
              y = y_along,
              z = qwert_mat,
              zsmooth = "best",
              type = 'heatmap',
              colorscale = 'Viridis',
              hoverongaps = False,
              hovertext = label_mat,
              hoverlabel = dict(namelength=0),
              hovertemplate ='<b>%{hovertext}</b> <br>Times chosen: %{z}'))
    
    image1 = Image.open("images/keyboard22.jpg")
    
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
    
    fig.update_traces(opacity=0.7)

    fig.update_layout(
            template="plotly_white",
            xaxis=dict(zeroline=False, showgrid=False), 
            yaxis=dict(zeroline=False, showgrid=False)
            )

    fig.update_xaxes(showticklabels=False)
    fig.update_yaxes(showticklabels=False)
    
    fig.show()  
    
    
    
    
def test_keyboard():
    
    test_z_mat = np.vstack((
             [-1, 0, 1]*10,
             [-1, 0, 1]*10,
             [-1, 0, 1]*10
             ))
    
    biggest_diff = 1
    big_diff = 0.75
    min_diff = 0.25
    # key_diff = 0.1
    
    x_seq = [min_diff, big_diff, biggest_diff]
    x_along = np.array([0])
    for i in range(10):
        x_along = np.hstack((x_along, np.add(x_seq, i)))
    y_along = [2, 1, 0]
    
    fig = go.Figure(data=go.Heatmap(
              x = x_along,
              y = y_along,
              z = test_z_mat,
              zsmooth = "best",
              type = 'heatmap',
              colorscale = 'Viridis'))
    
    image1 = Image.open("images/keyboard22.jpg")
    
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
    
    fig.update_traces(opacity=0.7)

    fig.update_layout(
            title_text = str(x_seq),
            template="plotly_white",
            xaxis=dict(zeroline=False, showgrid=False), 
            yaxis=dict(zeroline=False, showgrid=False)
            )

    fig.show()  
    
    
    
    
    
    
    
    
    
    
    