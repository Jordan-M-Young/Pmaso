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





def format_data(file):
    
    """reads the relevant security .csv file into a pandas dataframe
    and formats the dataframe"""
    
    
    data = pd.read_csv(file)
    data.index = list(data.iloc[:,0])
    data = data.iloc[:,1:]
    
    return data


def format_treasury_rates(path):
    
    """writes a pandas dataframe containing US treasury bond rates,
    and formats the dataframe for further use"""
    
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
    
    """collects US treasury bond rates of different maturities, from
    the included treasury_rates.csv"""
    
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

def get_betas(file,start,end):
    
    """calculates betas for a given security by
    analyzing a formatted .csv file"""
        



    data = format_data(file)
    data = data.loc[start:end,:]        
     

    
    close_SP5 = data.iloc[:,0]
    close_PFE = data.iloc[:,1]
    
    returns_SP5 = data.iloc[:,2]
    returns_PFE = data.iloc[:,3]
     
    
    betas = []
    for i in range(3,len(data)):
        closeSP5_Ti = np.array(close_SP5[0:i])
        close_PFE_Ti = np.array(close_PFE[0:i])
        returns_SP5_Ti = np.array(returns_SP5[0:i])
        returns_PFE_Ti = np.array(returns_PFE[0:i])
        
        avg_return_PFE_Ti = returns_PFE_Ti.mean() 
        avg_return_SP5_Ti = returns_SP5_Ti.mean() 
        var = (((returns_SP5_Ti -avg_return_SP5_Ti)**2).sum()) / len(returns_SP5_Ti)
        
        cov = ((returns_SP5_Ti - avg_return_SP5_Ti) * (returns_PFE_Ti - avg_return_PFE_Ti)).sum() 
        cov = cov / (len(returns_SP5_Ti) - 1)
        
        
        beta = cov / var
        betas.append(beta)
    
    

    

    return betas,data


def nan_check(treasury_data,date,mat):
    """makes sure selected treasury dataframe element
    is not nan"""
    
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
    
    """determines the correct maturity of treasury bond to use
    based on the current time interval's relationship to the starting 
    date selected"""
    
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
    
    """if the date selected does not occur in the treasury bond
    dataframe index, this script looks for another day that is one
    or two days ahead or behind the original date and in the treasury 
    bond dataframe index"""
    
    new_date = date.split('/')
    new_date[1] = str(int(new_date[1]) + num)
    if len(new_date[1]) == 1:
        new_date[1] = '0' + new_date[1]
    new_date = '/'.join(new_date)
    rf = nan_check(treasury_data,new_date,mat)

    return rf

def get_risk_free(dates,treasury_data_path,start,end,freq):
    
    """determines  risk free rates of a set of dates between
    the start and end parameters"""

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




def get_alphas(portfolio_returns,risk_free,market_returns,betas):
    
    """generates the alphas of a portfolio for a certain historical interval"""
    
    R = portfolio_returns
    Rf = risk_free
    Beta = betas
    Rm = market_returns
    alpha = R - Rf - (Beta*(Rm-Rf))
    
    return alpha



def check_proportion_list(proportions):
    
    """makes sure that the proportion set(s) are the correct
    data type: list of integers or list of lists of integers. makes 
    sure that the elements of each proportion set = 1."""
    
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
    

def get_dates(file,start,end):
    
    """gets a list of dates between the start and end dates
    passed to this function"""
    
    data = format_data(file)
    data = data.loc[start:end,:] 
    dates = list(data.index)
    
    return dates




