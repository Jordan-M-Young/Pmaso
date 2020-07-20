import os
import numpy as np
import pandas as pd
import pyFolio_tools as pft




class Portfolio():
    
    """portfolio class object"""
    
    def __init__(self,tickers,directory_path,start=None,end=None,treasury_data_path=None,freq=None):
        super().__init__()
        
        self.portfolio = True
        self.ticker_paths = []
        self.directory_path = directory_path
        self.treasury_data_path = treasury_data_path
        self.tickers = tickers
        self.freq = freq
        
        for ticker in self.tickers:
            ticker = ticker + '.csv'
            self.ticker_paths.append(os.path.join(self.directory_path,ticker))
        
        self.start = start
        self.end = end
        

        

    def gen_stock_betas(self,start=None,end=None):
        
        if self.start == None:
            start = start
        else:
            start = self.start
        
        if self.end == None:
            end = end
        else:
            end = self.end
        
        
        self.betas = {}
        for i in range(len(self.tickers)):
            betas, data = pft.get_betas(self.ticker_paths[i],start,end)
            self.betas[self.tickers[i]] = np.array(betas)
        
        return self.betas
    
    
    def port_beta_math(self,proportions,start,end):
        proportions, prop_type = pft.check_proportion_list(proportions)
        betas = self.gen_stock_betas(start,end)
        pb = []
        
        
        if prop_type == 'list':
            for counter, value in enumerate(betas):
                if counter == 0:
                    arr = betas[value]
                    p = proportions[counter]
                    val = arr * p
                    port_betas = val
                else:
                    arr = betas[value]
                    p = proportions[counter]
                    val = arr * p
                    
                    port_betas += val
            
        elif prop_type == 'list/list':
            for prop_set in proportions:
                for counter, value in enumerate(betas):
                    if counter == 0:
                        arr = betas[value]
                        p = prop_set[counter]
                        val = arr * p
                        port_betas = val
                    else:
                        arr = betas[value]
                        p = prop_set[counter]
                        val = arr * p
                        
                        port_betas += val
                pb.append(port_betas)
            
            port_betas = pb[0]
            port_betas = port_betas.reshape(517,1).T   
            for i in range(len((proportions))-1):
                port_betas = np.concatenate((port_betas,pb[i+1].reshape(517,1).T))
        
        else:
            port_betas = None
        
        
        return port_betas
    
    def start_end_check(self,start,end):
        start_flag = True
        end_flag = True
        
        if self.start == None and start == None:
            start_flag = False
            
        elif start == None:
            start = self.start
            
        else:
            start = start
            
        
        if self.end == None and end == None:
            end_flag = False
            
            
        elif end == None:
            end = self.end
            
        else:
            end = end
        
        return start, end, start_flag, end_flag
    
    def start_end_error_handler(self,start_flag,end_flag):
        
        if start_flag == False and end_flag == True:
            print('Error: Enter a start date during method call or object initialization')
            
        elif start_flag == True and end_flag == False:
            print('Error: Enter an end date during method call or object initialization')
            
        else:
            print('Error: Enter a start and end date during method call or object initialization')
    
    def treasury_check(self,treasury_data_path):
        treasury_flag = True
        
        if self.treasury_data_path == None and treasury_data_path == None:
            treasury_flag = False
            
        elif treasury_data_path == None:
            treasury_data_path = self.treasury_data_path
            
        else:
            treasury_data_path = treasury_data_path
        
        return treasury_data_path, treasury_flag
    
    def treasury_error_handler(self):
        print('Error: Enter a treasury filepath during method call or object initialization\n')
        
    def freq_check(self,freq):
        freq_flag = True
        
        if self.freq == None and freq == None:
            freq_flag = False
            
        elif freq == None:
            freq = self.freq
            
        else:
            freq = freq
        
        return freq, freq_flag
    
    def freq_error_handler(self):
        print('Error: Enter a frequency value ("Weekly","Monthly", or "Daily")' 
               + 'in method call or object initialization\n')
    
    
    def gen_portfolio_betas(self,proportions=None,start=None,end=None):
        if proportions == None:
            proportions = []
            prop_el = float(1) / float(len(self.tickers))
            for i in range(len(self.tickers)):
                proportions.append(prop_el)
        
        start, end, start_flag, end_flag = self.start_end_check(start,end)
        
        
        if start_flag and end_flag:
            port_betas = self.port_beta_math(proportions,start,end)
            
        else:
            self.start_end_error_handler(start_flag,end_flag)
            port_betas = None
        
        return port_betas
        
    def gen_risk_free(self,treasury_data_path=None,start=None,end=None,freq=None):
        
        
        start, end, start_flag, end_flag = self.start_end_check(start,end)
        treasury_data_path, treasury_flag = self.treasury_check(treasury_data_path)
        freq, freq_flag = self.freq_check(freq)
        
        if start_flag and end_flag and treasury_flag and freq_flag:
            
            dates = pft.get_dates(self.ticker_paths[0],start,end)
            risk_free = pft.get_risk_free(dates,treasury_data_path,start,end,freq)

        else:
            risk_free = None
            
            if start_flag == False or end_flag == False:
                self.start_end_error_handler(start_flag,end_flag)
            if treasury_flag == False:
                self.treasury_error_handler()
            if freq_flag == False:
                self.freq_error_handler()
            
        
        
        
        
        
        return np.array(risk_free)
    
    def gen_alphas(self,portfolio_returns,risk_free,market_returns,betas):
        
        R = portfolio_returns
        Rf = risk_free
        Beta = betas
        Rm = market_returns
        alpha = R - Rf - (Beta*(Rm-Rf))
        
        
        
        
        return alpha
        
