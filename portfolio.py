import os
import numpy as np
import pandas as pd
import portfolio_class_tools as pct




class Portfolio():
    
    """Portfolio class object"""
    
    def __init__(self,tickers,directory_path,start=None,end=None,treasury_data_path=None,freq=None):
        super().__init__()
        
        self.portfolio = True
        self.ticker_paths = []
        self.directory_path = directory_path
        self.treasury_data_path = treasury_data_path
        self.tickers = tickers
        self.freq = freq
        
        
        
        self.start = start
        self.end = end
        
    def start_end_check(self,start,end):
        """Makes sure that a start and end arg has been passed to the 
        parent function this function is nested in or has been passed to the
        class during initialization"""
        
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
        """Alerts user that an error has occurred regarding the
        start and/or end arguments"""
        
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

    def param_check(self,params):
        
        """checks to see if a params argument has been passed to the 
        parent function or was passed to the portfolio class during 
        object initialization"""
        
        param_flag = True

        if params == None and self.params == None:
            param_flag = False
            
        elif params == None:
            params = self.params
        
        else:
            params = params
        
        return params, param_flag
    
    
    def param_error_handler(self):
        
        """displays and error if a params argument was not passed to the parent
        function"""
        
        print('Error: Enter a parameter dictionary in method call or' +
              'during portfolio object initialization.')
        
    def gen_sec_parameters(self,tickers=None,directory_path=None,start=None,
                           end=None,freq=None,treasury_data_path=None):
        
        
        
        #Checks to see if the necessary inputs have been passed to the method
        #or to the portfolio class on when intialized
        start, end, start_flag, end_flag = self.start_end_check(start,end)
        treasury_data_path, treasury_flag = self.treasury_check(treasury_data_path)
        freq, freq_flag = self.freq_check(freq)
        
        #if all variables are there, a parameter dictionary is generated
        if start_flag and end_flag and treasury_flag and freq_flag:
            
            #generates parameter dictionay
            self.params = pct.gen_params_dic(tickers,
                                         directory_path,
                                         start,
                                         end,
                                         freq,
                                         treasury_data_path)
        
        #if not a None type object is returned and an error messgage is displayed
        else:
            self.params = None
            
            if start_flag == False or end_flag == False:
                self.start_end_error_handler(start_flag,end_flag)
            if treasury_flag == False:
                self.treasury_error_handler()
            if freq_flag == False:
                self.freq_error_handler()
        
        
        
        
        
        return self.params
     
     
    def gen_portfolio_parameters(self,proportions,tickers=None,directory_path=None,start=None,
                                  end=None,freq=None,treasury_data_path=None):
        
        params = self.gen_sec_parameters(tickers,
                                        directory_path,
                                        start,
                                        end,
                                        freq,
                                        treasury_data_path)
             
        portfolio_params = {}
        
        proportions, prop_type = pct.check_proportion_list(proportions)
        
        if prop_type == 'list':
            proportions = [proportions]
    
        
        
        
        for proportion in proportions:
            prop_params = {}
            
            for key,value in params.items():
                p_dic = list(enumerate(value))
               
                for i in range(len(p_dic)):
                   if i == 0:
                       param = proportion[i]*value[p_dic[i][1]]
                   else:
                       param = param + (proportion[i]*value[p_dic[i][1]])
                
                prop_params[key] = param
                
            portfolio_params[str(proportion)] = prop_params
               
        
        self.portfolio_parms = portfolio_params
        
        return portfolio_params
    
    def get_opt_prop(self,params=None,parameter_type='Beta'):
        
        """performs proportion optimization of your portfolio based on the
        passed parameter type"""
        
        
        params, param_flag = self.param_check(params)
        
        if param_flag:
            props = pct.prop_optimizer(params, self.tickers, parameter_type)
        
        else:
            self.param_error_handler()            
            props = None
            
        
        return props
