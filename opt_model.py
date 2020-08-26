# -*- coding: utf-8 -*-

"""
Created on Tue Aug 25 08:55:07 2020

@author: jmyou
"""



from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtWidgets import  QFileDialog
from portfolio_class import Portfolio
import pmaso_tools as pmt

class Model(QObject):
    
    new_dir = pyqtSignal(str,str)
    get_params = pyqtSignal(dict,dict,list)
    send_data = pyqtSignal(dict,str)
    send_table = pyqtSignal(list)
    
    def __init__(self):
        super().__init__()
        self.data = {}
        self.weights = {}
    
    
    def update_directory(self,name):
        """Calls a file dialog window and gets user input to choose a 
        file directory"""
        
        dname = QFileDialog.getExistingDirectory(None,'Select a directory')
        self.new_dir.emit(dname,name)
        
    def param_gen(self,tickers,weights,dir_path,freq,rf_rate,name):
        """Initializes a Portfolio class object for the current tab,
        then portfolio class methods are called to generate portfolio
        parameters
        """
        
        #Sets arguments to be passed to Portfolio class on initialization
        ticker_list = pmt.ticker_parse(tickers)
        
        #Initializes Portfolio class object
        portfolio = Portfolio(ticker_list,dir_path,float(rf_rate),freq)
        
        #Generates portfolio parameters
        sec_params = portfolio.gen_sec_parameters()
        opt_params = portfolio.get_opt_portfolios(sec_params,weights)
        
        #Adds portfolio data to the GUI data dictionary for later use
        self.data[name] = {'Sec':sec_params,'Opt':opt_params}
        self.weights[name] = weights
        
        self.get_params.emit(sec_params,opt_params,ticker_list)
        #returns the parameter dictionaries generated
    
    def gen_report(self,name,tickers):
        """This function allows the user to save key information regarding their generated
        portfolio data to an excel file, which is commonly used in financial services
        """
        #Opens a file explorer window for the user to set a save file name/directory
        fname, _ = QFileDialog.getSaveFileName(self,
                                                   'Save File',
                                                   'c:/',
                                                   'Excel Files (*.xlsx)')
        
      
       
        #Generates the report
        pmt.gen_report(tickers,self.data[name]['Opt'],fname)
    
    def get_data(self,name,data_type):
        """Grabs data from model class 'data' attribute and fulfills request
        made by view component"""
        
        data = self.data[name][data_type]
        self.send_data.emit(data,data_type)
        
        
    def update_table(self,name,sel):
        """Creates a selection list that contains pertinent portfolio 
        parameters. Entries in this list correspond to each data point selected
        with the lasso tool in the view component"""
        
        #Gets optimization parameters dictionary
        opt_params = self.data[name]['Opt']
        
        #Unpacks the selection array
        x = [list(sel[i].data) for i in range(len(sel))]
        
        #Returns of the selection array
        rets = [float(x[i][1]) for i in range(0,len(x))]
        
        #Pertinent portfolio parameters
        alphas = opt_params['Alphas']
        betas = opt_params['Betas']
        stds = opt_params['Portfolio_Space_Stds']
        returns = opt_params['Portfolio_Space_Returns']
        sharpes = opt_params['Portfolio_Sharpe_Ratios']
        weights = opt_params['Weights']

        #Index numbers of selection values in the returns array
        inds = [returns.index(rets[i]) for i in range(len(rets))]
        
        #Gets all information on each selection data point based on indices
        selection = [[float(stds[inds[i]]),
              float(returns[inds[i]]),
              float(sharpes[inds[i]]),
              float(alphas[inds[i]]),
              float(betas[inds[i]])] for i in range(len(inds))]
        
        #Packs all values into a list of lists
        num = len(selection[0]) 
        for j in range(len(selection)):
            for i in reversed(range(len(weights[0]))):
                selection[j].insert(num,float(weights[j][i]))
        
        #Sends list to view component
        self.send_table.emit(selection)