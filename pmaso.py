import sys
import PyQt5
from PyQt5 import QtCore
from PyQt5 import QtWidgets as qtw

from optimization_window import Optimization_Window
import portfolio_class_tools as pct

class MainWindow(qtw.QMainWindow):
    """Opening window of pmaso software portfolio names and tickers
    are entered here and then are passed to an optimizer window"""
    
    def __init__(self):
        super().__init__()
        
        #Window settings
        self.setWindowTitle('PyFolio - Version 0.0.1')
        self.left = 100
        self.top = 100
        self.width = 640
        self.height = 480
        self.setGeometry(self.left,self.top,self.width,self.height)
        
        #Window data
        self.portfolio_flags = []
        self.portfolios = {}
        self.portfolio_rows = 1
        self.directory_path = None
        
        
        #Main Widget Labels
        self.name_label = qtw.QLabel('Portfolio')
        self.tickers_label = qtw.QLabel('Tickers')
        self.name_label.setMaximumSize(500,50)
        self.tickers_label.setMaximumSize(500,50)
        
        
        #Main Widget Portfolio Entry
        self.save_portfolio_button = qtw.QPushButton('Save')
        self.save_portfolio_button.clicked.connect(lambda:self.click_save_button(self.save_portfolio_button))
        self.load_portfolio_button = qtw.QPushButton('Load')
        self.load_portfolio_button.clicked.connect(lambda:self.click_load_button(self.load_portfolio_button))
        self.port_name = qtw.QTextEdit()
        self.port_tickers = qtw.QTextEdit()
        self.row1_check_box = qtw.QCheckBox()
        
        
        
        #Main Widget Add portfolio Button
        self.add_port_button = qtw.QPushButton()
        self.add_port_button.setText('Add Portfolio')
        self.add_port_button.clicked.connect(self.add_portfolio_row)
        self.rem_port_button = qtw.QPushButton()
        self.rem_port_button.setText('Remove Portfolio')
        self.rem_port_button.clicked.connect(self.remove_portfolio_row)
        self.main_layout = qtw.QGridLayout()
        
        self.main_layout.addWidget(self.name_label,0,2,1,1)
        self.main_layout.addWidget(self.tickers_label,0,3,1,1)
        self.main_layout.addWidget(self.save_portfolio_button,1,0,1,1)
        self.main_layout.addWidget(self.load_portfolio_button,1,1,1,1)
        self.main_layout.addWidget(self.port_name,1,2,1,1)
        self.main_layout.addWidget(self.port_tickers,1,3,1,1)
        self.main_layout.addWidget(self.row1_check_box,1,4,1,1)
        self.main_layout.addWidget(self.add_port_button,self.portfolio_rows+1,0,1,1)
        self.main_layout.addWidget(self.rem_port_button,self.portfolio_rows+1,1,1,1)
        
        
        self.main_widget = qtw.QWidget()
        self.main_widget.setLayout(self.main_layout)
        self.scrollArea = qtw.QScrollArea()
        self.scrollArea.setWidget(self.main_widget)
        self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scrollArea.setWidgetResizable(True)



            
        
        self.centralWidget = self.setCentralWidget(self.scrollArea)
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        #App Menu
        menu = self.menuBar()
        
        #File Menu
        file_menu = menu.addMenu('File')
        set_data_directory = file_menu.addAction('Set Data Directory')
        set_data_directory.triggered.connect(self.set_file_directory)
        
        #Tools Menu
        tools_menu = menu.addMenu('Tools')
        format_files = tools_menu.addAction('Format Files')
        optimize_portfolio = tools_menu.addAction('Optimize Portfolios')
        optimize_portfolio.triggered.connect(self.collect_portfolios)
        
        
        
        
        
        #Status Bar
        status_bar = qtw.QStatusBar()
        self.setStatusBar(status_bar)
        status_bar.showMessage('This is a status bar')
        
        
        self.show()
        
        

    def remove_element(self,i):
        """Removes an element from the GUI layout"""
        
        widgetToRemove = self.main_layout.itemAt(i).widget()
        if str(type(widgetToRemove)) != "<class 'NoneType'>":
            self.main_layout.removeWidget(widgetToRemove)
            widgetToRemove.setParent(None)
        
        
    def add_portfolio_row(self):
        """Adds a new row of widgets for entering a new portfolio"""
        
        #Deletes elements in the way of new row
        for i in reversed(range(self.main_layout.count())):
            if  i == (3 + 5*self.portfolio_rows) or i == (2 + 5*self.portfolio_rows):
                self.remove_element(i)
                
           
        self.portfolio_rows += 1
        
        for i in reversed(range(self.main_layout.count())):
            widgetToRemove = self.main_layout.itemAt(i).widget()
           
       
                    
                    
        #Adds new widgets
        new_save_button = qtw.QPushButton('Save')
        new_save_button.clicked.connect(lambda:self.click_save_button(new_save_button))
        new_load_button = qtw.QPushButton('Load')
        new_load_button.clicked.connect(lambda:self.click_load_button(new_load_button))
        
        self.main_layout.addWidget(new_save_button,self.portfolio_rows,0,1,1)
        self.main_layout.addWidget(new_load_button,self.portfolio_rows,1,1,1)
        self.main_layout.addWidget(qtw.QTextEdit(),self.portfolio_rows,2,1,1)
        self.main_layout.addWidget(qtw.QTextEdit(),self.portfolio_rows,3,1,1)
        self.main_layout.addWidget(qtw.QCheckBox(),self.portfolio_rows,4,1,1)
        self.main_layout.addWidget(self.add_port_button,self.portfolio_rows+1,0,1,1)
        self.main_layout.addWidget(self.rem_port_button,self.portfolio_rows+1,1,1,1)
        
        
        
        
        
        
    
        
        
        
    def remove_portfolio_row(self):
        """Removes a row of widgets if you want to drop a portfolio entry"""
        
        if self.portfolio_rows != 1:
            for i in reversed(range(self.main_layout.count())):
                if i >  5*self.portfolio_rows - 4:
                    self.remove_element(i)
                    print(i)
        
        
            self.portfolio_rows -= 1
            print(self.portfolio_rows)
            
            
            self.main_layout.addWidget(self.add_port_button,self.portfolio_rows+1,0,1,1)
            self.main_layout.addWidget(self.rem_port_button,self.portfolio_rows+1,1,1,1)
    
    
    
    
    
    
    
    
    
    def set_file_directory(self):
        """Sets file directory"""
        
        dname = qtw.QFileDialog.getExistingDirectory(self,'Select a directory')
        self.directory_path = dname
    
    def click_save_button(self,b):
        """Saves portfolio settings to a text file"""
        
        for i in (range(self.main_layout.count())):
            widgetToRemove = self.main_layout.itemAt(i).widget()
            if widgetToRemove == b:
                fname, _ = qtw.QFileDialog.getSaveFileName(self,'Save File')
                pct.write_port(self.main_layout.itemAt(i+2).widget().toPlainText(), 
                               self.main_layout.itemAt(i+3).widget().toPlainText(), 
                               fname)
                
    def click_load_button(self,b):
        """Loads portfolio settings text file"""
        
        for i in (range(self.main_layout.count())):
            widgetToRemove = self.main_layout.itemAt(i).widget()
            if widgetToRemove == b:
                fname, _ = qtw.QFileDialog.getOpenFileName(self,'Save File')
                portfolio, tickers = pct.load_port(fname)
                self.main_layout.itemAt(i+1).widget().setText(portfolio)
                self.main_layout.itemAt(i+2).widget().setText(tickers)
                               
                
            
    def collect_portfolios(self):
        """Gathers all the portfolio entries and passes them to an instance
        of the Optimization_Window class"""
        
        portfolios = {}
        for i in (range(self.main_layout.count())):
            widgetToRemove = self.main_layout.itemAt(i).widget()
            if type(widgetToRemove) == PyQt5.QtWidgets.QCheckBox:
                if widgetToRemove.isChecked():
                    tickers = self.main_layout.itemAt(i-1).widget().toPlainText()
                    port_name= self.main_layout.itemAt(i-2).widget().toPlainText()
                    portfolios[port_name] = tickers
                    
                    
                    
                    
                    
                    
        self.res = Optimization_Window(portfolios,
                                    self.directory_path
                                    )
        
        
        
        
        
        
        self.res.show()
        
        
        
if __name__ == '__main__':
    
    app = qtw.QApplication(sys.argv)
    mw = MainWindow()
    sys.exit(app.exec())
    
