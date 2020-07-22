# -*- coding: utf-8 -*-
"""
Created on Sat Jun 20 11:52:48 2020

@author: jmyou
"""


import numpy as np
import pandas as pd
import csv
import matplotlib.pyplot as plt
from scipy.stats import linregress
import math
import time
from scipy.optimize import leastsq
from scipy.optimize import minimize, LinearConstraint




def format_data(file,start,end):
    
    data = pd.read_csv(file)
    data.index = list(data.iloc[:,0])
    data = data.iloc[:,1:]
    data = data.loc[start:end,:]
    return data


def format_treasury_rates(path):
    
    
    data = pd.read_csv(path)
    dates = list(data.iloc[:,0])
    new_dates = []
    
    for date in dates:
        new_date = date.rsplit('/',2)
        if len(new_date[0]) == 1:
            new_date[0] = '0' + new_date[0]
        
        if len(new_date[1]) == 1:
            new_date[1] = '0' + new_date[1]
            
        new_date = new_date[0] + '/' + new_date[1] + '/' + new_date[2]
        new_dates.append(new_date)
        
    data = data.iloc[:,1:]
    data.index = new_dates
    
    return data

def get_treasury_data(path,start,end):
    
    if start == '01/01/1990':
        treasury_data = None
        print('no treasury data for this date')
    elif int(start.rsplit('/',2)[2]) < 1990:
        treasury_data = None
        print('no treasury data for this date')
    else:
        treasury_data = format_treasury_rates(path)
        treasury_data = treasury_data.loc[start:end,:]

    return treasury_data

def get_std(data):

    std = []
    
    for i in range(3,len(data)):
        x = np.array(data[0:i])
        mu = np.mean(x)
        N = len(x)
        
        sigma = np.sqrt((np.sum((x-mu)**2))/N)
        std.append(sigma)
        
    return np.array(std)
        
        
def gen_covariance(sec_returns,ind_returns):
    
    covariances = []
    for i in range(3,len(sec_returns)):
        
        returns_ind_Ti = np.array(ind_returns[0:i])
        returns_sec_Ti = np.array(sec_returns[0:i])
        
        avg_return_sec_Ti = returns_sec_Ti.mean() 
        avg_return_ind_Ti = returns_ind_Ti.mean() 
        
        cov = ((returns_ind_Ti - avg_return_ind_Ti) * (returns_sec_Ti - avg_return_sec_Ti)).sum() 
        cov = cov / (len(returns_sec_Ti) - 1)
        
        covariances.append(cov)
    
    return np.array(covariances)

def gen_variance(ind_returns):
    
    variances = []
    for i in range(3,len(ind_returns)):
        
        returns_ind_Ti = np.array(ind_returns[0:i])
        avg_return_ind_Ti = returns_ind_Ti.mean() 
        var = (((returns_ind_Ti -avg_return_ind_Ti)**2).sum()) / len(returns_ind_Ti)
        variances.append(var)
    
    return np.array(variances)
        
def get_betas(sec_returns,ind_returns):
    

    
   
     
    
    cov = gen_covariance(sec_returns,ind_returns)
    var = gen_variance(ind_returns)

    betas = cov / var

    return betas




def nan_check(treasury_data,date,mat):
    
    rf = float(treasury_data.loc[date,mat])
    if math.isnan(rf):
            if mat == '2mo':
                mat = '1mo'
                rf = float(treasury_data.loc[date,mat])
                if math.isnan(rf):
                    mat = '3mo'
                    rf = float(treasury_data.loc[date,mat])
                

    
    return rf
    

def get_maturity(dates,freq):
    if freq == 'monthly' or freq == 'Monthly':
        mod = 0.25
    elif freq == 'weekly' or freq == 'Weekly':
        mod = 1
    else:
        mod = 4
    
    
    maturity = []
    for i in range(len(dates)):
        if i == 0:
            maturity.append('1mo')
        elif i == (int(4*mod)):
            maturity.append('1mo')
        elif i == (int(8*mod)):
            maturity.append('2mo')
        elif i == (int(12*mod)):
            maturity.append('3mo')
        elif i == (int(24*mod)):
            maturity.append('6mo')
        elif i == (int(52*mod)):
            maturity.append('1yr')
        elif i == (int(104*mod)):
            maturity.append('2yr')
        elif i == (int(156*mod)):
            maturity.append('3yr')
        elif i == (int(260*mod)):
            maturity.append('5yr')
        elif i == (int(364*mod)):
            maturity.append('7yr')
        elif i == (int(520*mod)):
            maturity.append('10yr')
        elif i == (int(1040*mod)):
            maturity.append('20yr')
        elif i == (int(1560*mod)):
            maturity.append('30yr')
        
        elif i < (int(4*mod)):
            maturity.append('1mo')
        elif i < (int(8*mod)):
            maturity.append('1mo')
        elif i < (int(12*mod)):
            maturity.append('2mo')
        elif i < (int(24*mod)):
            maturity.append('3mo')
        elif i < (int(52*mod)):
            maturity.append('6mo')
        elif i < (int(104*mod)):
            maturity.append('1yr')
        elif i < (int(156*mod)):
            maturity.append('2yr')
        elif i < (int(260*mod)):
            maturity.append('3yr')
        elif i < (int(364*mod)):
            maturity.append('5yr')
        elif i < (int(520*mod)):
            maturity.append('7yr')
        elif i < (int(1040*mod)):
            maturity.append('10yr')
        elif i < (int(1560*mod)):
            maturity.append('20yr')
        elif i > (int(1560*mod)):
            maturity.append('30yr')
        else:
            continue
    
    return [dates,maturity]

def check_another_date(date,mat,treasury_data,num):
    
    new_date = date.split('/')
    new_date[1] = str(int(new_date[1]) + num)
    if len(new_date[1]) == 1:
        new_date[1] = '0' + new_date[1]
    new_date = '/'.join(new_date)
    rf = nan_check(treasury_data,new_date,mat)

    return rf

def get_risk_free(dates,treasury_data_path,start,end,freq):

    treasury_data = get_treasury_data(treasury_data_path,start,end)
    
    dates = get_maturity(dates,freq)
    
    # print(dates)
    
    risk_free = []
    for j in range(len(dates[0])):
        date = dates[0][j]
        
        mat = dates[1][j]
        try:
            rf = nan_check(treasury_data,date,mat)
            risk_free.append(float(rf))
        except KeyError:
            try:
                check_another_date(date,mat,treasury_data,1)
                risk_free.append(float(rf))
            except KeyError:
                try:
                    check_another_date(date,mat,treasury_data,-1)
                    risk_free.append(float(rf))
                except KeyError:
                   try:
                        check_another_date(date,mat,treasury_data,2)
                        risk_free.append(float(rf))
                        
                   except KeyError:
                       print('Fail')

    
    return risk_free


    
        

def get_sharpe_ratios(portfolio_returns,risk_free,returns_std):
    
    Rp = portfolio_returns
    Rf = risk_free
    sigma_p = returns_std
    
    sharpe_ratio = (Rp - Rf) / sigma_p

    return sharpe_ratio


def get_alphas(returns,risk_free,market_returns,betas):
    
    R = returns
    Rf = risk_free
    Beta = betas
    Rm = market_returns
    alpha = R - Rf - (Beta*(Rm-Rf))
    
    return alpha



def check_proportion_list(proportions):
    if str(type(proportions[0])) == "<class 'float'>":
        prop_type = 'list'
        count = 0.00
        for element in proportions:
            count += float(element)
        
        if count != float(1):
            diff = 1 - count
            bad_prop = proportions[-1]
            proportions[-1] = round(float(proportions[-1]) + diff,6)
            print('Proportion Set 0:\n----------------\n' +
                  'Entered proportions not equivalent to 1,\n' 
                  + str(bad_prop) + ' changed to ' + str(proportions[-1])
                  + '\n')
        
        
        
    
    elif str(type(proportions[0])) ==  "<class 'list'>":
        for i in range(len(proportions)):
            prop_type = 'list/list'
            count = 0.00
            for element in proportions[i]:
                count += float(element)
                
            if count != float(1):
                diff = 1 - count
                bad_prop = proportions[i][-1]
                proportions[i][-1] = round(float(proportions[i][-1]) + diff,6)
                print('Proportion Set ' + str(i) + ':\n----------------\n' +
                      'Entered proportions not equivalent to 1,\n' 
                      + str(bad_prop) + ' changed to ' + str(proportions[i][-1])
                      + '\n')
    
            

    return proportions, prop_type
    

def get_dates(data,start,end):
    
    """Gets a list of dates between the start and end dates"""
    
    data = data.loc[start:end,:] 
    dates = list(data.index)
    
    return dates


def obj_func_neg_inverse(x,constants):
    
    """objective function where the output is equivalent to one over the
    dot product of the parameter values for each indiviudal stock in the 
    portfolio(constants) and the proportions of each stock held(x) multiplied
    by -1. This allows minimization of any parameter whose ideal value is in 
    the range:   0 < value < 1 (beta)"""
    
    y =  1 / -x.dot(constants)
    
    return y

def obj_func_neg(x,constants):
    
    """objective function where the output is equivalent to the
    dot product of the parameter values for each indiviudal stock in the 
    portfolio(constants) and the proportions of each stock held(x) multiplied
    by -1. This allows minimization of any parameter whose ideal value is in 
    the range:   0 < value (alpha,returns,etc)"""
    
    y =  -x.dot(constants)
    
    return y

def obj_func_call(x0,constants,constraint,bounds,parameter_type):
    
    """calls the correct objective function for portfolio 
    proportion optimiziation"""
    
    
    if parameter_type == 'beta':
      
          res = minimize(obj_func_neg_inverse,x0=x0,args=(constants),
                          constraints=constraint,
                          bounds=bounds)
            
    else:
        
        res = minimize(obj_func_neg,x0=x0,args=(constants),
                        constraints=constraint,
                        bounds=bounds)
    
    
    
    return res
            
            
        
def prop_optimizer(params,parameter_type='beta'):
    
    """Handles the job of optimizing the proportions of the stocks in your
    portfolio based on the parameter you've chosen."""
    
    
    props = []
    
    for i in range(len(params['1'])):
        
        constants = []
        
        for key, value in params.items():
            constant = np.array(value).reshape(1,len(value))[0][i]
            constants.append(constant)
            
        constants = np.array(constants)
        
        con_sum = 1.0
        constraint = LinearConstraint(np.ones(3), lb=1.0, ub=1.0)
        bounds = [(0,1),(0,1),(0,1)]
        
        
        x0 = np.array([0.1,0.7,0.2])
        
        res = obj_func_call(x0,constants,constraint,bounds,parameter_type)
        
        prop = list(res.x)
        props.append(prop)


    return np.array(props)

