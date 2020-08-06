import portfolio_class_tools as pct
import portfolio_optimization as pop



class Portfolio():
    
    def __init__(self,tickers,directory_path,freq=None):
        super().__init__()
        
        self.portfolio = True
        self.ticker_paths = []
        self.directory_path = directory_path
        self.tickers = tickers
        self.freq = freq
        self.params = None
        
    
      
        
    
        
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
        
    
    def weight_check(self,weights):
        
        weight_flag = True
        
        if weights == None and self.weights == None:
            weight_flag = False
            
        elif weights == None:
            weights = self.weights
        else:
            weights = weights
        
        return weights, weight_flag
    
    def weight_error_handler(self):
        
        print('Error: a weights list in method call or set using' +
              ' gen_weights() class method')
    
    def tickers_check(self,tickers):
        
        ticker_flag = True
        
        if tickers == None and self.tickers == None:
            ticker_flag = False
            
        elif tickers == None:
            tickers = self.tickers
        else:
            tickers = tickers
        
        return tickers, ticker_flag
    
    def ticker_error_handler(self):
        
        print('Error: enter a tickers list in method call or set during' +
              'portfolio initialization')
        
    
    def directory_check(self,directory_path):
        
        directory_path_flag = True
        
        if directory_path == None and self.directory_path == None:
            directory_path_flag = False
            
        elif directory_path == None:
            directory_path = self.directory_path
        else:
            directory_path = directory_path
        
        return directory_path, directory_path_flag
    
    def directory_error_handler(self):
        
        print('Error: enter a directory_path string method call or set during' +
              'portfolio initialization')
    
    def ticker_error_handler(self):
        
        print('Error: enter a tickers list in method call or set during' +
              'portfolio initialization')
        
    
    def gen_sec_parameters(self,tickers=None,directory_path=None,start=None,
                           end=None,freq=None,treasury_data_path=None):
        
        
        
        #Checks to see if the necessary inputs have been passed to the method
        #or to the portfolio class on when intialized
        tickers, tickers_flag = self.tickers_check(tickers)
        treasury_data_path, treasury_flag = self.treasury_check(treasury_data_path)
        freq, freq_flag = self.freq_check(freq)
        directory_path, directory_path_flag = self.directory_check(directory_path)
        
        
        #if all variables are there, a parameter dictionary is generated
        if freq_flag and tickers_flag and directory_path_flag:
            
            #generates parameter dictionay
            self.params = pct.gen_params_dic(tickers,
                                             directory_path,
                                             freq,
                                             )
        
        #if not a None type object is returned and an error messgage is displayed
        else:
            self.params = None
                   
            if freq_flag == False:
                self.freq_error_handler()
            if tickers_flag == False:
                self.ticker_error_handler()
            if directory_path_flag == False:
                self.directory_error_handler()
        
        
        
        
        
        return self.params
     

    def gen_weights(self,num_portfolios,bounds):
        
        self.weights = pop.gen_weights(len(self.tickers),num_portfolios,bounds)

        
        return self.weights
    
    def get_opt_portfolios(self,params=None,weights=None,tolerance=0.3):
        
        """performs proportion optimization of your portfolio based on the
        passed parameter type"""
        
        
        params, param_flag = self.param_check(params)
        weights, weight_flag = self.weight_check(weights)
        
        if param_flag == True and weight_flag == True:
            optimization_parameters = pop.optimize_portfolio_weights(params,
                                                                     self.tickers,
                                                                     weights,
                                                                     tolerance)
        
        elif param_flag == True and weight_flag == False:
            self.weight_error_handler()
            optimization_parameters = None
            
        elif param_flag == False and weight_flag == True:
            self.param_error_handler()            
            optimization_parameters = None
        
        else:
            self.weight_error_handler()
            self.param_error_handler()
        
            
        
        return optimization_parameters
