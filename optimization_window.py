
import sys
from PyQt5 import QtWidgets as qtw
import opt_view as ov
import opt_model as om
class Optimization_Window(qtw.QMainWindow):
    
    def __init__(self,portfolio_dic,dir_path):
        """Optimization Window class object
    
        Window that allows the user to generate a space of portfolios based
        on passed tickers and weight set argument, allows for analysis (in the future)
        and facilitates analysis reports
        """    
        
        super().__init__()
        
        
        #Window settings
        self.setWindowTitle('Results')
        self.left = 100
        self.top = 100
        self.width = 640
        self.height = 480
        self.setGeometry(self.left,self.top,self.width,self.height)
        
        
        #Window arguments
        self.dir_path = dir_path
        self.portfolio_dic = portfolio_dic
        self.data = {}
        
        self.weights = None
        self.selection = None
    
        #Model portion of this window
        self.model = om.Model()
    
    
        #View portion of this window
        self.view = ov.View(self.portfolio_dic,self.dir_path)
        self.setCentralWidget(self.view)
        

    
        """Slots and Signals"""
        
        #Directory update signals
        self.view.new_dir.connect(self.model.update_directory)
        self.model.new_dir.connect(self.view.update_directory)
        
        #Parameter generation signals
        self.view.get_params.connect(self.model.param_gen)
        self.model.get_params.connect(self.view.param_gen)
        
        #Report writing signals
        self.view.gen_report.connect(self.model.gen_report)
        
        #Data request signals
        self.view.send_data.connect(self.model.get_data)
        self.model.send_data.connect(self.view.get_data)
        
        #Table widget update signals
        self.view.send_table.connect(self.model.update_table)
        self.model.send_table.connect(self.view.update_table)
        

        
        
        
        self.show()
        
        



if __name__ == '__main__':
    pd = {'Hello':'AIG,BA,CVX','22':'CVX,IBM'}
    app = qtw.QApplication(sys.argv)
    mw = Optimization_Window(pd,'E:/PythonProjects/Stocks_with_Phil/Formatted_Stocks_Monthly')
    sys.exit(app.exec_())
   
