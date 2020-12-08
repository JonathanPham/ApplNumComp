# -*- coding: utf-8 -*-
"""
Created on Wed Oct  7 08:25:49 2020

@author: Ashlee

ODE Example 1
$\frac{dx}{dt} = b1-b2*x
"""

import numpy as np
from scipy.optimize import curve_fit
from scipy.integrate import odeint
import matplotlib.pyplot as plt

# Data for example 2
xaxisData = np.array( [0.5, 1.0, 5.0, 20.0] ) # time, independent variable
# new for > 1 dependent variables: for multiple rows, put each row in a [] and surround the whole thing by ([])
yaxisData = np.array( [ [99.0, 98.0, 50.0, 3.0], [2.0, 4.0, 35.0, 7.0] ] ) # x, dependent variable 

# guesses for parameters
b1guess = 0.01
b2guess = 0.2
parameterguesses = np.array([b1guess, b2guess])

# Need two functions for our model
# 1. to define the system of ODE(s)
# 2. to solve the ODE(s) and return ypredicted values in same shape as yaxisData

# 1. define ODEs
def system_of_ODEs(x,t,parameters): # yvar, xvar, args
    # unpack the parameters
    b1 = parameters[0]
    b2 = parameters[1]
    # unpack the dependent variables
    x1 = x[0]
    x2 = x[1]
    dx1dt = -b1*x1*x2
    dx2dt = b1*x1*x1-b2*x2
    return dx1dt, dx2dt
# end of function

# 2. Solve ODEs at xaxisData points
    # and return calculated yaxisCalculated
    # using current values of the parameters
def model(xaxisData,*params):
    # initial condition(s) for the ODE(s)
    yaxis0 = np.array([100.0,1.0]) # should include a decimal
    # new for > 1 dependent variables:
    numYaxisVariables = 2
    yaxisCalc = np.zeros((xaxisData.size,numYaxisVariables))

    for i in np.arange(0,len(xaxisData)):
        if xaxisData[i] == 0.0: # should include a decimal
            # edit for > 1 dependent variables:            
            yaxisCalc[i,:] = yaxis0
        else:
            xaxisSpan = np.linspace(0.0,xaxisData[i],101)
            ySoln = odeint(system_of_ODEs,yaxis0,xaxisSpan,args = (params,)) # soln for entire xaxisSpan
            # edit for > 1 dependent variables:            
            yaxisCalc[i,:] = ySoln[-1,:] # calculated y at the end of the xaxisSpan
            # at this point yaxisCalc is now 2D matrix with the number of columns set as : to include all yvariables
            # curve_fit needs a 1D vector that has the rows in a certain order, which result from the next two commands
    yaxisOutput = np.transpose(yaxisCalc)
    yaxisOutput = np.ravel(yaxisOutput)
    return yaxisOutput
    # end of for loop
# end of model function 

# Estimate the parameters
# new for > 1 dependent variables:
# np.ravel(yaxisData) transforms yaxisData from a 2D vector into the 1D vector that curve_fit expects.

parametersoln, pcov = curve_fit(model,xaxisData,np.ravel(yaxisData),p0=parameterguesses)
print(parametersoln)
# edit for > 1 dependent variables:
plt.plot(xaxisData, yaxisData[0,:],'o') 
plt.plot(xaxisData, yaxisData[1,:],'x') 
# initial condition(s) for the ODE(s)
yaxis0 = np.array([100.0,1.0]) # should include a decimal
numYaxisVariables = 2

xaxisForPlotting = np.linspace(0,xaxisData[-1],101)

# Two options for getting the solution:
# OptionA call the model, which returns a 1D output and reshape into 2D
# OptionB wrap odeint around system_of_ODEs to solve the differential equations directly

# OptionA
yaxisCalc_OptionA = model(xaxisForPlotting,*parametersoln)
# the answer from model is 1D so we need to reshape it into the expected 2D matrix dimensions for plotting
yaxisCalc_OptionA = np.reshape(yaxisCalc_OptionA,(numYaxisVariables,xaxisForPlotting.size))
plt.plot(xaxisForPlotting, yaxisCalc_OptionA[0,:],'b-',label='x1 fitted')
plt.plot(xaxisForPlotting, yaxisCalc_OptionA[1,:],'r-',label='x2 fitted')

## OptionB
yaxisCalc_OptionB = odeint(system_of_ODEs,yaxis0,xaxisForPlotting,args = (parametersoln,))
plt.plot(xaxisForPlotting, yaxisCalc_OptionB[:,0],'g-',label='x1 fitted')
plt.plot(xaxisForPlotting, yaxisCalc_OptionB[:,1],'y-',label='x2 fitted')
# From the plot we see that OptionA and OptionB give exactly the same result, so you can chose either and not have to use both options.

yaxisCalcFromGuesses = odeint(system_of_ODEs,yaxis0,xaxisForPlotting,args = (parameterguesses,))
plt.plot(xaxisForPlotting,yaxisCalcFromGuesses,'k-') # before fitting
plt.xlabel('t')
plt.ylabel('x')
plt.show()
 
        
        
