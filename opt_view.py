# -*- coding: utf-8 -*-
"""
Created on Tue Aug 25 09:11:46 2020

@author: jmyou
"""


import sys
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import QPushButton, QWidget, QTabWidget, QHBoxLayout
from PyQt5.QtWidgets import QVBoxLayout, QLabel, QLineEdit,QFormLayout
from PyQt5.QtWidgets import QProgressBar, QGridLayout, QCheckBox, QTableView

from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar 



import pmaso_tools as pmt
from external_worker import External
import pmaso_gui_widgets as pgw


class View(QWidget):
    """View component of the Model-View structure of the optimization window
    class"""
    
    
    #Class signals
    new_dir = pyqtSignal(str)
    get_params = pyqtSignal(str,list,str,str,str,str)
    gen_report = pyqtSignal(str,str)
    send_data = pyqtSignal(str,str)
    send_table = pyqtSignal(str,list)
    
    
    def __init__(self,portfolio_dic,dir_path): 
        """Initializes the View component"""
        
        super(QWidget, self).__init__() 
        self.layout = QVBoxLayout(self) 
        self.portfolio_dic = portfolio_dic
        self.dir_path = dir_path
        self.tab_dic = {}
        self.weight_dic = {}
        self.selection = None
        self.fig_els = {key: {} for key in [key for key in self.portfolio_dic.keys()]}
        # Initialize tab screen 
        self.tabs = QTabWidget() 
        
        self.tabs.resize(300, 200) 
        
        self.tabUI(state='init')
        
        
        
        # Add tabs to widget
        self.tabs.currentChanged.connect(self.current_tab)
        self.layout.addWidget(self.tabs)
        
        self.setLayout(self.layout) 
        
        

      
        
        #Initializes the app GUI
    def tabUI(self,state='init'):
        """Initializes the tab structure of the GUI
        Very messy function, definitley needs to be refactored
        """
        
        
        #Initialization routine for the tab widget architecture
        #This section is run when the app is first opened
        if state == 'init':
            
            #Loops over the number of entries in portfolio_dic
            # and generates a separate tab for each entry
            for key,value in self.portfolio_dic.items():
                
                dic = {}
                
                #Initializes a tab widget and sets its name
                #to the corresponding portfolio name
                tab1 = QWidget()
                tab1.setObjectName(key)
                
                #Initializes a custom combobox for selecting frequency
                freq_combo_box = self.combo_boxUI()
                
                #Initializes a line edit box where tickers can be entered
                #The intial value is set to the value of the current entry
                #in portfolio_dic 
                tick_box = QLineEdit()
                tick_box.setText(value)
                
                #Initializes a line edit widget where a file directory can be set
                tick_dir_box = QLineEdit('')
                tick_dir_box.setObjectName('TickBox')
                
                #If dir_path argument was passed to the Optimization_Window Class
                #This sets that path as the value of the tick_dir lineedit widget
                if self.dir_path:
                    tick_dir_box.setText(self.dir_path)
                
                #Initializes a button that allows the user to set a file directory through
                #a file explorer window
                set_dir_button = QPushButton('Set Directory')
                set_dir_button.setObjectName(key)
                set_dir_button.clicked.connect(self.change_directory)
                
                #Initializes a custom combobox widget that allows a user to set the number
                #of theoretical portfolios to be generated during optimization processes
                num_port_combo_box = self.combo_boxUI('Num_Ports')
                
                #Initializes custom combobox widgets tha allows a user to set
                #Boundary conditions for asset weights in their portfolios
                min_weight_box = self.combo_boxUI('MinW')
                max_weight_box = self.combo_boxUI('MaxW')
                
                # Initializes a line edit that accepts a risk free rate number
                rf_box = QLineEdit()
                rf_box.setText('2.43')
                
                #Initializes a button that commences optimization processes
                button = QPushButton('Optimize')
                button.setObjectName(key)
                button.clicked.connect(self.on_btn_clic)
                
                #Initializes a layout class object
                layout = QFormLayout()
                
                #Initialized widgets are added to the layout
                layout.addRow('Tickers', tick_box)
                layout.addRow('',QLabel(''))
                layout.addRow('Ticker Directory',tick_dir_box)
                layout.addRow('',set_dir_button)
                layout.addRow('',QLabel(''))
                layout.addRow('Select Frequency', freq_combo_box)
                layout.addRow('',QLabel(''))
                layout.addRow('Number of Portfolios',num_port_combo_box)
                layout.addRow('',QLabel(''))
                layout.addRow('Minimum Asset Proportion (%)',min_weight_box)
                layout.addRow('Maximum Asset Proportion (%)',max_weight_box)
                layout.addRow('',QLabel(''))
                layout.addRow('Risk Free Rate (%)',rf_box)
                layout.addRow('',button)
                
                #The tabs layout is set to the generated layout
                tab1.setLayout(layout)
                
                #The current tab is added to the parent tab widget
                self.tabs.addTab(tab1,str(key))
                
                #Generated widgets,widget parameters, the layout, and tab
                #are added to the tab_dic class attribute to be called later
                #for re rendering the GUI
                dic['Tab'] = tab1
                dic['Tickers'] = value
                dic['Layout'] = layout
                dic['Freq'] = freq_combo_box
                dic['Tick_box'] = tick_box
                dic['Dir_box'] = tick_dir_box
                dic['Dir_box_text'] = str(tick_dir_box.text())
                dic['Num_port'] = num_port_combo_box
                dic['Opt_button'] = button
                dic['MinWeight'] = min_weight_box 
                dic['MaxWeight'] = max_weight_box
                dic['Rf_rate'] = rf_box
                self.tab_dic[key] = dic
    
        else:
                
                self.left = 100
                self.top = 100
                self.width = 1050
                self.height = 850
                self.setGeometry(self.left,self.top,self.width,self.height)
    
                
                dic = {}
                current = self.name
                for i in reversed(range(len(self.tab_dic))):
                    self.tabs.removeTab(i)
                    
                
                
                for key,val in self.tab_dic.items():
                    #Loops over the number of entries in tab_dic
                    #number of entries = number of tabs = number of passed portfolios
                    
                    
                    dic[key] = {}
                    #Initializes a blank tab widget
                    tab1 = QWidget()
                    tab1.setObjectName(key)
                    
                    #gets layout from tab_dic
                    layout = val['Layout']
                    
                    #Sets the new tab's layout as the retrieved layout
                    tab1.setLayout(layout)
                    self.tabs.addTab(tab1,str(key))
                    
                    #updates the tab and layout values in tab_dic
                    self.tab_dic[key]['Tab'] = tab1
                    self.tab_dic[key]['Layout'] = layout
                
                self.tabs.setCurrentWidget(self.tabs.findChild(QWidget,current))
                                           
    def current_tab(self):
        """Stores the indexed name of the currently viewed tab"""
        index = self.tabs.currentIndex()
        name = self.tabs.tabText(index)
        self.name = name
        
        
    def combo_selected(self,text):
        """Test function, can be deleted later"""
        print(text)
        
    
    def combo_boxUI(self,box_type='Freq'):
        """Initializes a CustomComboBox class object and returns it to 
        be added into a layout"""
        
        combo_box = pgw.CustomComboBox(box_type)
        combo_box.activated[str].connect(self.combo_selected)
    
        return combo_box
    
    def change_directory(self):
        """Opens a file explorer window, prompts user to select the directory
        from which the necessary ticker files are stored"""
        
        
        sending_button = self.sender()
        name = sending_button.objectName()
        self.new_dir.emit(name)
    
    def update_directory(self,dname,name):
        """Updates the shown directory in the directory line edit widget"""
        
        self.tab_dic[name]['Dir_box_text'] = dname
        self.tab_dic[name]['Dir_box'].setText(dname)
        # self.tabUI(state='update_directory')
        
        self.tabs.setCurrentWidget(self.tabs.findChild(QWidget,name))
    
    def build_report(self,name,tickers):
        """Emits a signal carrying name and tickers arguments to the 
        model component of the optimization window structure, a report
        generation function is then run by the model"""
        
        self.gen_report.emit(name,tickers)
    
    def request_data(self,key,data_type):
        """Sends a signal to the model requesting data specified by 
        data_type and a key corresponding to the current selected tab"""
        
        self.send_data.emit(key,data_type)
    
    def get_data(self,data,data_type):
        """receives data from the model and stores it in a class attribute"""
        
        if data_type == 'Opt':
            self.opt_params = data
        else:
            self.sec_params = data
        
    
    def on_btn_clic(self):
        
        """Handles portfolio optimization and refreshes the relevant
        tab to reflect the results of the optimization process"""
        
        #Gets the tab in which an optimization button was pressed
        sending_button = self.sender()
        name = sending_button.objectName()
        
    
        #Clears the current tab layout
        self.rem_layout = self.tab_dic[name]['Layout']
        self.clear_tab_layout()
        
        #adds a progress Bar in the middle of the tab widget
        for i in range(7):
            self.rem_layout.addRow('',QLabel(""))
        self.progress = QProgressBar(self)
        self.rem_layout.addRow('          ',self.progress)
        
        
        #Optimization work, tickers are passed to the optimization worker
        #thread which handles optimization math and progress bar 
        current_ticks = str(self.tab_dic[name]['Tick_box'].text())
        self.ticker_list = pmt.ticker_parse(current_ticks)
   
        #Arguments required to run the External worker thread 
        num_portfolios = int(self.tab_dic[name]['Num_port'].currentText())
        min_b = int(self.tab_dic[name]['MinWeight'].currentText())
        max_b = int(self.tab_dic[name]['MaxWeight'].currentText())
        
        
        bounds = (min_b,max_b)
        
        #Initializes External worker thread which generates weight set perumutations while running a progress bar
        self.calc = External(self.ticker_list,num_portfolios,bounds,name)
        
        #Connects progress counter signal
        self.calc.countChanged.connect(self.onCountChanged)
        
        #Starts the thread worker
        self.calc.start()
        
        #Accepts signals from the worker thread when its job is completed
        self.calc.weights.connect(self.receive_weights)
        self.calc.finished.connect(self.onFinished)

    def onCountChanged(self, value):
        """sets value of progress bar, connected to the countchanged
        signal in the 'External' thread class object"""
        
        self.progress.setValue(value)
        
    def clear_tab_layout(self):
            """Clears all widgets and layouts from the current tab"""
            
            for i in reversed(range(self.rem_layout.count())):
                widgetToRemove = self.rem_layout.itemAt(i)
                
                if widgetToRemove.widget():
                    wid = widgetToRemove.widget()
                    self.rem_layout.removeWidget(wid)
                    wid.setParent(None)
                    
                    
    def receive_weights(self,weights,name):
        """Stores weight permutation set generated and transmitted by External worker thread
        """""
        self.weight_dic[name] = weights
            
            
    def onFinished(self,fin,name):
        """This function is called when the optimization work is completed,
        the progress bar is cleared and data visualization widgets are 
        rendered on the tab widget"""
        
        
        if fin == 'Finished':
            
            #Ends worker thread
            self.calc.stop()
            
            #Clears progress bar widget from GUI
            self.progress.hide()
            
            #Clears the layout of the current tab
            self.clear_tab_layout()
            
            tickers = self.tab_dic[name]['Tick_box'].text()
            weights = self.weight_dic[name]
            dir_path = self.tab_dic[name]['Dir_box_text']
            freq = str(self.tab_dic[name]['Freq'].currentText())
            rf_rate = self.tab_dic[name]['Rf_rate'].text()
            
            #Generates portfolio parameters
            self.get_params.emit(tickers,weights,dir_path,freq,rf_rate,name)
            
            self.name = name
            
            #stores portfolio parameters in GUI data dictionary
            
            #intializes a graph widget to plot the generated portfolio data
            graphWidget = pgw.CustomCanvas(self.opt_params)
            
            self.tab_dic[name]['graph'] = graphWidget
            
            #Generates a new layout object
            layout = self.resultsUI(name)
            
            #Stores that layout in the tab architecture dictionary
            self.tab_dic[name]['Layout'] = layout
            
            #Renders the new tab layout
            self.tabUI(state='change')
            
            #Sets GUI to the current tab
            self.tabs.setCurrentWidget(self.tabs.findChild(QWidget,name))
            
    def param_gen(self,sec_params,opt_params,ticker_list):
        """Receives signal from model component carrying dictionaries
        containing data on the optimization process and the portfolio 
        securities"""
        
        self.sec_params = sec_params
        self.opt_params = opt_params
        self.ticker_list = ticker_list
    
    
    def resultsUI(self,name):
        """Utilizes the results layout of the working tab after optimization processes have
        finished"""
        
        #Initializes layout widgets
        layout1a = QHBoxLayout()
        layout1 = QVBoxLayout()
        layout2 = QGridLayout()
        
        #Initializes label widgets
        label = QLabel('Plot Items')
        label2 = QLabel('')
        
        #Intializes checkbox widgets and connects functions to them
        chk1 = QCheckBox('Efficient Frontier')
        chk2 = QCheckBox('All Portfolios')
        chk2.setChecked(True)
        self.graph_box_checked(chk1,name)
        self.graph_box_checked(chk2,name)
        chk1.toggled.connect(lambda:self.graph_box_checked(chk1,name))
        chk2.toggled.connect(lambda:self.graph_box_checked(chk2,name))
        
        #Initializes button widgets and connects functions to them
        apply_button = QPushButton('Apply')
        report_button = QPushButton('Generate Report')
        report_button.clicked.connect(lambda:self.build_report(name,self.ticker_list))
        apply_button.setObjectName(name)
        apply_button.clicked.connect(self.apply_plot_settings)
        
        #Initializes a tableviewer for lasso selected portfolios
        tableview = QTableView()
        tableview.setSortingEnabled(True)
        if self.selection:
            print('self Selection exists')
            mod = pgw.TableModel(self.selection,self.ticker_list)
        else:
            mod = pgw.TableModel()
        tableview.setModel(mod)
        
        #Initializes a toolbar for navigating the rendered figure
        graphWidget = self.tab_dic[name]['graph']
        graph_tools = NavigationToolbar(graphWidget,self)
        
        #Initializes Widget wid1 sets layouts and adds child widgets
        wid1 = QWidget()
        layout1.addWidget(graphWidget)
        layout1.addWidget(QLabel(''))
        layout1.addWidget(graph_tools)
        wid1.setLayout(layout1)
        
        #Initalizes Widget wid1a sets layout and adds child widgets
        wid1a = QWidget()
        layout1a.addWidget(tableview)
        layout1a.addWidget(wid1)
        wid1a.setLayout(layout1a)
        
        #Initializes Widget wid2 sets layout and adds child widgets
        wid2 = QWidget()
        layout2.addWidget(label,0,0,1,1)
        layout2.addWidget(label2,1,0,1,1)
        layout2.addWidget(chk1,2,0,1,1)
        layout2.addWidget(chk2,3,0,1,1)
        layout2.addWidget(report_button,3,2,1,1)
        layout2.addWidget(apply_button,2,2,1,1)
        wid2.setLayout(layout2)
        
        #Initializes the main layout 'layout' and adds
        #The previously intializeds widgets to it
        layout = QVBoxLayout()
        layout.addWidget(wid1a)
        layout.addWidget(wid2)
        
        return layout
    
    def apply_plot_settings(self):
         """This function handles redrawing the central figure widget when
         new graph parameters are selected and applied from the GUI
         """
         
         
         #Gets button name for finding relevant entries in f_e dictionary
         sending_button = self.sender()
         name = sending_button.objectName()
         
         #Sets Figure Elements dictionary
         f_e = self.fig_els[name]
         
         #Gets items to be graphed from Figure Elements dictionary
         graph_items = [key for key,val in f_e.items() if val == True]
         
         #Gets optimization paramters dictionary
         self.request_data(name,'Opt')
         opt_params = self.opt_params
         
         #Generates graph Widget
         graphWidget = pgw.CustomCanvas(opt_params,graph_items)
         self.tab_dic[name]['graph'] = graphWidget
         
         
         #Reconstructs the tab layout
         layout = self.resultsUI(name)
         self.tab_dic[name]['Layout'] = layout
         
         
         
         #Renders the GUI
         self.tabUI(state='change')
         self.tabs.setCurrentWidget(self.tabs.findChild(QWidget,self.name))    
        
    def graph_box_checked(self,b,name):
        """Test function to check checkbox functionality, can be deleted at a later point"""
        
        if b.isChecked():
            self.fig_els[name][b.text()] = True
        else:
            self.fig_els[name][b.text()] = False
            
    def keyPressEvent(self, event):
        """This function handles all key events in the GUI"""
        #Ends program event loop
        if event.key() == Qt.Key_Q:
            self.deleteLater()
            
        #Returns the parameters of data points within lasso selection 
        elif event.key() == Qt.Key_Return:
            graphWidget = self.tab_dic[self.name]['graph'] 
            self.lsso = graphWidget.CustomPlot.lsso
            self.request_table(self.name)
           
            f_e = self.fig_els[self.name]
        
            #Gets items to be graphed from Figure Elements dictionary
            graph_items = [key for key,val in f_e.items() if val == True]
            self.request_data(self.name,'Opt')
            opt_params = self.opt_params
            
            
            graphWidget = pgw.CustomCanvas(opt_params,graph_items)
            self.tab_dic[self.name]['graph'] = graphWidget
            layout = self.resultsUI(self.name)
            self.tab_dic[self.name]['Layout'] = layout
            self.tabUI(state='change')
       
            
        event.accept()
    
    def request_table(self,name):
        """Sends selection data to model for processing"""
        sel = list(self.lsso.xys[self.lsso.ind])
        self.send_table.emit(name,sel)
    
    def update_table(self,selection):
        """Receives data from model used to update table values"""
        self.selection = selection