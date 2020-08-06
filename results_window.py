import sys
import PyQt5
from PyQt5 import QtCore as qtc
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg

import portfolio_class_tools as pct
from portfolio_class import Portfolio


class External(qtc.QThread):
    """
    Runs a counter thread.
    """
    countChanged = qtc.pyqtSignal(int)
    finished = qtc.pyqtSignal(str)
    
    def run(self):
        self.threadactive = True
        count = 0
        while count < 100:
            count += 0.0001
            self.countChanged.emit(count)
        
        self.finished.emit('Finished')
    
    def stop(self):
       self.wait()
       
       
class tabdemo(qtw.QTabWidget):
    
    def __init__(self,portfolio_dic, parent = None):
        super(tabdemo, self).__init__(parent)
        self.tabs = qtw.QTabWidget()
        self.tab_dic = {}
        self.portfolio_dic = portfolio_dic
        for key,value in self.portfolio_dic.items():
            dic = {}
            tab1 = qtw.QWidget()
            layout = qtw.QFormLayout()
            layout.addRow('Item 1', qtw.QLineEdit(self))
            layout.addRow('Item 2', qtw.QLineEdit(self))
            button = qtw.QPushButton('Hello')
            button.setObjectName(key)
            button.clicked.connect(self.on_btn_clic)
            
            layout.addRow('',button)
            tab1.setLayout(layout)
            self.tabs.addTab(tab1,str(key))
            
            
            
            dic['Tab'] = tab1
            dic['Tickers'] = value
            dic['Layout'] = layout
            dic['Button'] = button
            
            
            self.tab_dic[key] = dic
      
    
      
        self.layout = qtw.QVBoxLayout(self)
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)
       
    

    def on_btn_clic(self):
        sending_button = self.sender()
        self.name = sending_button.objectName()
        self.rem_layout = self.tab_dic[self.name]['Layout']
        self.clear_tab_layout()

        for i in range(7):
            self.rem_layout.addRow('',qtw.QLabel("Prog"))
        self.progress = qtw.QProgressBar(self)
        self.rem_layout.addRow('          ',self.progress)
        
        
        self.calc = External()
        self.calc.countChanged.connect(self.onCountChanged)
        self.calc.start()
        self.calc.finished.connect(self.onFinished)
            
        
    def onFinished(self,fin):
        if fin == 'Finished':
            self.calc.stop()
            self.progress.hide()
            self.clear_tab_layout()
            self.rem_layout = qtw.QVBoxLayout()
            self.rem_layout.addWidget(qtw.QLabel('YOOO'))
            tab1 = self.tab_dic[self.name]['Tab']
            tab1.setLayout(self.rem_layout)
            self.tab_dic[self.name]['Tab'] = tab1
            
            self.tabs = qtw.QTabWidget()
            for key,value in self.tab_dic.items():
                
                tab = self.tab_dic[key]['Tab']
                value = self.tab_dic[key]['Tickers']
                layout = self.tab_dic[key]['Layout']
                button = self.tab_dic[key]['Button']
                
                tab1 = tab
                layout1 = layout
                layout.addRow('Item 3', qtw.QLineEdit(self))
                layout.addRow('Item 4', qtw.QLineEdit(self))
                button = qtw.QPushButton('Hello')
                button.setObjectName(key)
                button.clicked.connect(self.on_btn_clic)
                
                layout.addRow('',button)
                tab1.setLayout(layout)
                self.tabs.addTab(tab,str(key))
                
            print(self.tabs)
            self.layout = qtw.QVBoxLayout(self)
            self.layout.addWidget(self.tabs)
            self.setLayout(self.layout)
            
                
                
                
            
            
            
            
            
            
            
            
            
            
    def clear_tab_layout(self):
        
        for i in reversed(range(self.rem_layout.count())):
            widgetToRemove = self.rem_layout.itemAt(i)
            
            if widgetToRemove.widget():
                wid = widgetToRemove.widget()
                self.rem_layout.removeWidget(wid)
                wid.setParent(None)
        
    def onCountChanged(self, value):
        self.progress.setValue(value)
      
class Results_Window(qtw.QMainWindow):
    
    def __init__(self,portfolio_dic,dir_path):
        super().__init__()
        
        
        self.setWindowTitle('Results')
        self.left = 100
        self.top = 100
        self.width = 640
        self.height = 480
        self.dir_path = dir_path
        self.portfolio_dic = portfolio_dic
        
        self.setGeometry(self.left,self.top,self.width,self.height)
        
        
        self.table_widget = tabdemo(portfolio_dic)
        self.setCentralWidget(self.table_widget)
        
        
        menu = self.menuBar()
        menu.addMenu('File')
        
        self.show()
        
        
        
if __name__ == '__main__':
    pd = {'Hello':'XXX,PDD','22':'XXX,DDD,SSS'}
    app = qtw.QApplication(sys.argv)
    mw = Results_Window(pd,'E:/')
    sys.exit(app.exec())
