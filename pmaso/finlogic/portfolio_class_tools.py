import numpy as np
import pandas as pd


def format_data(file):
    

    
    data = pd.read_csv(file)
    data.index = list(data.iloc[:,0])
    data = data.iloc[:,1:]
    

    
    return data

def get_annual_dates(data,ann_ret):
    for i in range(len(ann_ret)):
        if i == 0:
            annual_dates = data.iloc[0,:]
        else:
            annual_dates = pd.concat([annual_dates,data.iloc[12*i,:]],axis=1)


    annual_dates = list(annual_dates.T.index)
    
    return annual_dates



def get_annualized_returns(data,freq,target='Asset'):   
    ann_returns = []
    
    if freq == 'Monthly' or freq == 'monthly':
        num = 12
    elif freq == 'Daily' or freq == 'daily':
        num = 52
    else:
        num = 365
    
    if target == 'Market':
        col = 2
    else:
        col = 3
    
    years = len(data) / num
    for i in range(int(years)):
        year_data = data.iloc[(i*num):num*(i+1),col]
        ann_returns.append(float(np.sum(year_data)))
        
    
    return np.array(ann_returns)

           



def get_dates(data):
    
    """Gets a list of dates between the start and end dates"""
    
    data = data.loc[:,:] 
    dates = list(data.index)
    
    return dates


    
def gen_params_dic(tickers,data_dir,freq,obj='Asset'):
    
    
    
    params = {'Annualized_Returns':{},
              'Annualized_Market_Returns':{},
              'Annualized_Market_Returns_std':{},
              freq + '_Returns':{},
              freq + '_Returns_std':{},
              'Data':{},
              freq +'_Dates':{}}
    
    for ticker in tickers:
        
        data_path = data_dir + '/' + ticker + '.csv'
        data = format_data(data_path)
        
        ann_ret = get_annualized_returns(data,freq)
        ann_dates = get_annual_dates(data,ann_ret)
        
        
        dates = get_dates(data)
        returns = np.array(data.iloc[:,3])
        
            

        params['Annualized_Returns'][ticker] = ann_ret
        params[freq +'_Returns'][ticker] = returns
        params['Data'][ticker] = data
        params[freq +'_Dates'][ticker] = dates
        params['Annualized_Dates'] = ann_dates
        params[freq + '_Returns_std'][ticker] = np.std(ann_ret)
        
    ann_mkt_ret = get_annualized_returns(data, freq, target='Market')
    ann_mkt_ret_std = np.std(ann_mkt_ret)

    params['Annualized_Market_Returns'] = ann_mkt_ret
    params['Annualized_Market_Returns_std'] = np.std(ann_mkt_ret)
    params['Annualized_Market_Returns_Variance '] = np.std(ann_mkt_ret)**2
    params['Annualized_Periodic_Market_Returns_std'] = ann_mkt_ret_std
    
    
    return params
