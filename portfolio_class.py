import portfolio_class_tools as pct
import portfolio_optimization as pop



class Portfolio():
    """Portfolio class. 
    
    Initialized with a tickers list, directory path 
    ( where the historical data is stored ), and optional frequency arguments. 
    """
    
    def __init__(self,tickers,directory_path,Rf_rate=None,freq=None):
        super().__init__()
        
        self.portfolio = True
        self.ticker_paths = []
        self.directory_path = directory_path
        self.tickers = tickers
        self.freq = freq
        self.params = None
        self.Rf_rate = Rf_rate
        
      
        
    
        
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
        """checks to see if a weights argument has been passed to the 
        parent function or was passed to the portfolio class during 
        object initialization
        """
        
        weight_flag = True
        
        if weights == None and self.weights == None:
            weight_flag = False
            
        elif weights == None:
            weights = self.weights
        else:
            weights = weights
        
        return weights, weight_flag
    
    def weight_error_handler(self):
        """Displays error message if no weights object was passed"""
        
        print('Error: a weights list in method call or set using' +
              ' gen_weights() class method')
    
    def tickers_check(self,tickers):
        """checks to see if a tickers argument has been passed to the 
        parent function or was passed to the portfolio class during 
        object initialization
        """
        
        ticker_flag = True
        
        if tickers == None and self.tickers == None:
            ticker_flag = False
            
        elif tickers == None:
            tickers = self.tickers
        else:
            tickers = tickers
        
        return tickers, ticker_flag
    
    def ticker_error_handler(self):
        """Displays error message if no ticker object was passed"""
        
        print('Error: enter a tickers list in method call or set during' +
              'portfolio initialization')
        
    
    def directory_check(self,directory_path):
        """checks to see if a directory_path argument has been passed to the 
        parent function or was passed to the portfolio class during 
        object initialization
        """
        
        directory_path_flag = True
        
        if directory_path == None and self.directory_path == None:
            directory_path_flag = False
            
        elif directory_path == None:
            directory_path = self.directory_path
        else:
            directory_path = directory_path
        
        return directory_path, directory_path_flag
    
    def directory_error_handler(self):
        
        print('Error: enter a directory_path string during method call or'  +
              'set during portfolio initialization')
    
   
    def risk_free_check(self,Rf_rate):
        
        rf_flag = True
        
        if Rf_rate == None and self.Rf_rate == None:
            rf_flag = False
            
        elif Rf_rate == None:
            Rf_rate = self.Rf_rate
        else:
            Rf_rate = Rf_rate
        
        return Rf_rate, rf_flag
    
    def risk_free_error_handler(self):
        print('Error: enter a risk free float/int  during method call or ' +
              'set during portfolio initialization')
        
    
    def gen_sec_parameters(self,tickers=None,directory_path=None,freq=None):
        """Generates a dictionary of the following portfolio parameters:
            (1) Annualized Dates (list)
            (2) Annualized Market Returns (numpy array)
            (3) Annualized Market Returns Standard Deviation
            (4) Annualized Asset Returns (dictionary with tickers as keys and numpy arrays as values) 
            (5) Periodic Asset Returns Data (dictionary with tickers as keys and pandas dataframes as values) 
            (6) Periodic Dates (dictionary with tickers as keys and lists as values)
            (7) Periodic Returns (dictionary with tickers as keys and numpy arrays as values)
            """
        
        
        #Checks to see if the necessary inputs have been passed to the method
        #or to the portfolio class on when intialized
        tickers, tickers_flag = self.tickers_check(tickers)
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
     

    def gen_weights(self,num_portfolios,bounds,count=None):
        
        """Generates a set of asset weight permutations based
        on the number of assets in your portfolio, the number of
        portfolios you wish to generate and the boundary asset proportion
        conditions passed"""     
        
        self.weights = pop.gen_weights(len(self.tickers),num_portfolios,bounds)

            
        
        return self.weights
    
    def get_opt_portfolios(self,params=None,weights=None,Rf_rate=None,tolerance=0.3):
        
        """Generates a set of portfolios based on a params dictionary,
        weight list, and optional tolerance arguments. 
       
        This function generates an optimization_parameters dictionary
        object that contains the following parameters:
            (1) Asset Expected Returns
            (2) Asset Standard Deviations of expected Returns or 'Risk'
            (3) Asset Variance
            (4) 'Best' Portfolios (dictionary)
            (5) Efficient Frontier Portfolios
            (6) Efficient Frontier Returns and Standard Deviations
            (7) Portfolio weight set
            (8) Entire Portfolio set Expected Returns
            (9) Entire Portfolio set Standard Deviations
            """
        params, param_flag = self.param_check(params)
        weights, weight_flag = self.weight_check(weights)
        Rf_rate, rf_flag = self.risk_free_check(Rf_rate)
        
        if param_flag == True and weight_flag == True and rf_flag == True:
            try:
                optimization_parameters = pop.optimize_portfolio_weights(params,
                                                           self.tickers,
                                                           weights,
                                                           Rf_rate,
                                                           tolerance)
            except ValueError:
                optimization_parameters = pop.optimize_portfolio_weights(params,
                                                           self.tickers,
                                                           weights,
                                                           Rf_rate,
                                                           tolerance)
        
        else:
            if weight_flag == False:
                self.weight_error_handler()
                optimization_parameters = None
            
            if param_flag == False:
                self.param_error_handler()            
                optimization_parameters = None
        
        
            
        
        return optimization_parameters
