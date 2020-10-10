#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  9 15:08:24 2020

@author: fs19144
"""

import plotly.graph_objects as go
import numpy as np

def histograms_1to10(survey):


    x0 = survey.iloc[:, 1].to_numpy()
    x1 = survey.iloc[:, 4].to_numpy()
    
    fig = go.Figure()
    fig.add_trace(go.Histogram(x=x0))
    fig.add_trace(go.Histogram(x=x1))
    
    # Overlay both histograms
    fig.update_layout(barmode='overlay')
    
    # Reduce opacity to see both histograms
    fig.update_traces(opacity=0.75)
    fig.show()