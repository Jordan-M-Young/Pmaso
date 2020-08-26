# -*- coding: utf-8 -*-
"""
Created on Tue Aug 25 11:51:27 2020

@author: jmyou
"""
from PyQt5.QtCore import pyqtSignal,QThread
import pmaso_tools as pmt
import numpy as np

class External(QThread):
    """Runs a counter thread. That runs and updates progress bars
    displayed during the optimization process
    """
    
    #Thread signals
    countChanged = pyqtSignal(int)
    finished = pyqtSignal(str,str)
    weights = pyqtSignal(list,str)
    
    def __init__(self, tickers, num_portfolios, bounds, name, parent=None):
        """initializes the class, this thread requires that a tickers,
        num__portfolios and boudary conditions argument respectively be
        passed.
        """
        
        super().__init__()
        
        self.tickers = tickers
        self.data = None
        self.num_portfolios = num_portfolios
        self.bounds = bounds
        self.name = name
        
    def run(self):
        """Runs the weight set generations routine while simultaneously
        updating a displayed progress bar in the window. I need to fix this function;
        too messy/cluttered and barely functional
        """
        
        
        perms = pmt.get_perms(len(self.tickers),self.bounds)
        
        
        count = 0
        while count < 100:
            counter = self.num_portfolios
            step = 100 / counter
            total = []
            
            
            p_list = list(perms)
            pnum = len(p_list)

                                    
            for i in range(pnum):
                if np.sum(np.array(list(p_list[i]))/100) == 1:
                    total.append(list(np.array(p_list[i])/100))
                    counter = counter - 1
                    count = count + step
                    self.countChanged.emit(count)
                if i == pnum - 1:
                    count = 100
            
        
        
        perms = None
        p_list = None
        
        self.weight = total
        self.weights.emit(self.weight,self.name)
        self.finished.emit('Finished',self.name)
        
        
    def stop(self):
       """Ends Thread?
       """
       
       self.wait()
       self.quit()