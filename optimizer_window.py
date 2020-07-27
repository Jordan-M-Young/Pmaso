import sys
import PyQt5
from PyQt5 import QtCore as qtc
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg

class Custom_ComboBox(qtw.QComboBox):
    def __init__(self):
    
        super().__init__()
        
        self.addItem('Alpha')
        self.addItem('Beta')
        self.addItem('Returns')
        self.addItem('Returns Standard Deviation')
        self.addItem('Sharpe Ratio')
        
    
class Optimizer_Window(qtw.QMainWindow):
    
    def __init__(self,portfolios):
        super().__init__()
        
        self.setWindowTitle('Optimizer - Version 0.0.1')
        self.left = 100
        self.top = 100
        self.width = 640
        self.height = 480
        self.setGeometry(self.left,self.top,self.width,self.height)
        self.portfolios = portfolios
        
        self.layout = qtw.QGridLayout()
        self.portfolio_label = qtw.QLabel('Portfolio')
        self.ticker_label = qtw.QLabel('Tickers')
        self.opt_label = qtw.QLabel('Optimization Paramter')
        self.portfolio_label.setMaximumSize(500,50)
        self.ticker_label.setMaximumSize(500,50)
        
        
        self.layout.addWidget(self.portfolio_label,0,0,1,1)
        self.layout.addWidget(self.ticker_label,0,1,1,1)
        self.layout.addWidget(self.opt_label,0,2,1,1)
        
        
        
        for i in range(len(portfolios)):
            port_name, tickers = portfolios[i]
            port_label = qtw.QLabel(port_name)
            ticker_label = qtw.QLabel(tickers)
            comboBox = Custom_ComboBox()
            
            self.layout.addWidget(port_label,i+1,0,1,1)
            self.layout.addWidget(ticker_label,i+1,1,1,1)
            self.layout.addWidget(comboBox,i+1,2,1,1)
            
            
        
        
        
        
        self.scrollArea = qtw.QScrollArea()
        
        
        
        self.widget = qtw.QWidget()
        self.widget.setLayout(self.layout)
        self.scrollArea.setVerticalScrollBarPolicy(qtc.Qt.ScrollBarAlwaysOn)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setWidget(self.widget)
        self.setCentralWidget(self.scrollArea)
        
        
    
        
        
        
        
        
        
        
        
        self.show()




if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    mw = Optimizer_Window()
    sys.exit(app.exec())
