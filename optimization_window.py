import sys
from PyQt5 import QtCore as qtc
from PyQt5 import QtWidgets as qtw
from portfolio_class import Portfolio
import pmaso_tools as pmt
import numpy as np
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar 
import pmaso_gui_widgets as pgw


class External(qtc.QThread):
    """Runs a counter thread. That runs and updates progress bars
    displayed during the optimization process
    """
    
    #Thread signals
    countChanged = qtc.pyqtSignal(int)
    finished = qtc.pyqtSignal(str)
    weights = qtc.pyqtSignal(list)
    
    def __init__(self, tickers, num_portfolios, bounds, parent=None):
        """initializes the class, this thread requires that a tickers,
        num__portfolios and boudary conditions argument respectively be
        passed.
        """
        
        super().__init__()
        
        self.tickers = tickers
        self.data = None
        self.num_portfolios = num_portfolios
        self.bounds = bounds
        
        
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
        self.weights.emit(self.weight)
        self.finished.emit('Finished')
        
        
    def stop(self):
       """Ends Thread?
       """
       self.wait()
       
       
      
class Optimization_Window(qtw.QMainWindow):
    """Optimization Window class object
    
    Window that allows the user to generate a space of portfolios based
    on passed tickers and weight set argument, allows for analysis (in the future)
    and facilitates analysis reports
    """    
    def __init__(self,portfolio_dic,dir_path=None):
        super().__init__()
        
        #Basic GUI properties
        self.setWindowTitle('Results')
        self.left = 100
        self.top = 100
        self.width = 640
        self.height = 480
        self.setGeometry(self.left,self.top,self.width,self.height)
        
        #Attributes used in portfolio optimization, plotting results
        #and data storage
        self.dir_path = dir_path
        self.portfolio_dic = portfolio_dic
        self.data = {}
        self.fig_els = {key: {} for key in [key for key in self.portfolio_dic.keys()]}
        self.weights = None
        
        #Initializes the main tab widget for the GUI
        self.tabs = qtw.QTabWidget()
        self.tab_dic = {}
        
        #Initializes the app GUI
        self.tabUI()
        
        #adds a menu bar
        menu = self.menuBar()
        menu.addMenu('File')
        
        #renders GUI
        self.show()
    
    
    
    
    def combo_selected(self,text):
        """Test function, can be deleted later"""
        print(text)
        
    
    def combo_boxUI(self,box_type='Freq'):
        """Initializes a CustomComboBox class object and returns it to 
        be added into a layout"""
        
        combo_box = pgw.CustomComboBox(box_type)
        combo_box.activated[str].connect(self.combo_selected)
    
        return combo_box
        
    
    def tabUI(self,state='init'):
        """Initializes the tab structure of the GUI
        Very messy function, definitley needs to be refactored
        """
        
        
        self.tabdemo = qtw.QTabWidget()
        
        #Initialization routine for the tab widget architecture
        #This section is run when the app is first opened
        if state == 'init':
            
            #Loops over the number of entries in portfolio_dic
            # and generates a separate tab for each entry
            for key,value in self.portfolio_dic.items():
                
                dic = {}
                
                #Initializes a tab widget and sets its name
                #to the corresponding portfolio name
                tab1 = qtw.QWidget()
                tab1.setObjectName(key)
                
                #Initializes a custom combobox for selecting frequency
                freq_combo_box = self.combo_boxUI()
                
                #Initializes a line edit box where tickers can be entered
                #The intial value is set to the value of the current entry
                #in portfolio_dic 
                tick_box = qtw.QLineEdit()
                tick_box.setText(value)
                
                #Initializes a line edit widget where a file directory can be set
                tick_dir_box = qtw.QLineEdit('')
                tick_dir_box.setObjectName('TickBox')
                
                #Initializes a button that allows the user to set a file directory through
                #a file explorer window
                set_dir_button = qtw.QPushButton('Set Directory')
                set_dir_button.setObjectName(key)
                set_dir_button.clicked.connect(lambda:self.set_directory(tick_dir_box))
                
                #Initializes a custom combobox widget that allows a user to set the number
                #of theoretical portfolios to be generated during optimization processes
                num_port_combo_box = self.combo_boxUI('Num_Ports')
                
                #Initializes custom combobox widgets tha allows a user to set
                #Boundary conditions for asset weights in their portfolios
                min_weight_box = self.combo_boxUI('MinW')
                max_weight_box = self.combo_boxUI('MaxW')
                
                #If dir_path argument was passed to the Optimization_Window Class
                #This sets that path as the value of the tick_dir lineedit widget
                if self.dir_path:
                    tick_dir_box.setText(self.dir_path)
                
                #Initializes a button that commences optimization processes
                button = qtw.QPushButton('Optimize')
                button.setObjectName(key)
                button.clicked.connect(self.on_btn_clic)
                
                #Initializes a layout class object
                layout = qtw.QFormLayout()
                
                #Initialized widgets are added to the layout
                layout.addRow('Tickers', tick_box)
                layout.addRow('',qtw.QLabel(''))
                layout.addRow('Ticker Directory',tick_dir_box)
                layout.addRow('',set_dir_button)
                layout.addRow('',qtw.QLabel(''))
                layout.addRow('Select Frequency', freq_combo_box)
                layout.addRow('',qtw.QLabel(''))
                layout.addRow('Number of Portfolios',num_port_combo_box)
                layout.addRow('',qtw.QLabel(''))
                layout.addRow('Minimum Asset Proportion (%)',min_weight_box)
                layout.addRow('Maximum Asset Proportion (%)',max_weight_box)
                layout.addRow('',button)
                
                #The tabs layout is set to the generated layout
                tab1.setLayout(layout)
                
                #The current tab is added to the parent tab widget
                self.tabdemo.addTab(tab1,str(key))
                
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
                dic['MinWeight'] = min_weight_box = self.combo_boxUI('MinW')
                dic['MaxWeight'] = max_weight_box
                
                self.tab_dic[key] = dic
        
        #This routine is run when the initial tab GUI needs to be updated/re rendered
        elif state == 'update_directory':
            dic = {}
            #Loops over the number of entries in the tab_dic class attribute
            #Number of entries = number of tabs = number of passed portfolios
            for key,val in self.tab_dic.items():
                dic[key] = {}
                tab1 = qtw.QWidget()
                tab1.setObjectName(key)
                layout = val['Layout']
                
                #Checks for a directory line edit widgets and
                #Updates their displayed text to the new directory chosen
                for i in range(layout.count()):
                    tick_box = layout.itemAt(i).widget()
                    name = tick_box.objectName()
                    if name == 'TickBox':
                        print(name)
                        tick_box.setText(val['Dir_box_text'])
                
                
                #Adds sets the updated layout as the new tab's layout
                tab1.setLayout(layout)
                self.tabdemo.addTab(tab1,str(key))
                
                #Updates entries of the changed widgets in the tab_dic attribute
                self.tab_dic[key]['Tab'] = tab1
                self.tab_dic[key]['Layout'] = layout
                self.tab_dic[key]['Dir_box_text'] = val['Dir_box_text']
            
            
            
            
            
            
        #This is run after the optimization process     
        else:
            
            self.left = 100
            self.top = 100
            self.width = 700
            self.height = 850
            self.setGeometry(self.left,self.top,self.width,self.height)

            
            dic = {}
            for key,val in self.tab_dic.items():
                #Loops over the number of entries in tab_dic
                #number of entries = number of tabs = number of passed portfolios
                
                dic[key] = {}
                #Initializes a blank tab widget
                tab1 = qtw.QWidget()
                tab1.setObjectName(key)
                
                #gets layout from tab_dic
                layout = val['Layout']
                
                #Sets the new tab's layout as the retrieved layout
                tab1.setLayout(layout)
                self.tabdemo.addTab(tab1,str(key))
                
                #updates the tab and layout values in tab_dic
                self.tab_dic[key]['Tab'] = tab1
                self.tab_dic[key]['Layout'] = layout
                
            
         
        #Renders the whole widget
        self.layout = qtw.QVBoxLayout()
        self.tabdemo.setLayout(self.layout)
        self.table_widget = self.tabdemo
        self.setCentralWidget(self.table_widget)
            

    def set_directory(self,box):
        """Opens a file explorer window, prompts user to select the directory
        from which the necessary ticker files are stored"""
        
        
        sending_button = self.sender()
        self.name = sending_button.objectName()
        dname = qtw.QFileDialog.getExistingDirectory(self,'Select a directory')
        
        self.tab_dic[self.name]['Dir_box_text'] = dname
        
        self.tabUI(state='update_directory')
        
        self.tabdemo.setCurrentWidget(self.tabdemo.findChild(qtw.QWidget,self.name))
        
        
    def clear_tab_layout(self):
        """Clears all widgets and layouts from the current tab"""
        
        for i in reversed(range(self.rem_layout.count())):
            widgetToRemove = self.rem_layout.itemAt(i)
            
            if widgetToRemove.widget():
                wid = widgetToRemove.widget()
                self.rem_layout.removeWidget(wid)
                wid.setParent(None)
        
    def onCountChanged(self, value):
        """sets value of progress bar, connected to the countchanged
        signal in the 'External' thread class object"""
        
        self.progress.setValue(value)
        
        
    def on_btn_clic(self):
        
        """Handles portfolio optimization and refreshes the relevant
        tab to reflect the results of the optimization process"""
        
        #Gets the tab in which an optimization button was pressed
        sending_button = self.sender()
        self.name = sending_button.objectName()
        
        
    
        #Clears the current tab layout
        self.rem_layout = self.tab_dic[self.name]['Layout']
        self.clear_tab_layout()
        
        #adds a progress Bar in the middle of the tab widget
        for i in range(7):
            self.rem_layout.addRow('',qtw.QLabel(""))
        self.progress = qtw.QProgressBar(self)
        self.rem_layout.addRow('          ',self.progress)
        
        
        #Optimization work, tickers are passed to the optimization worker
        #thread which handles optimization math and progress bar 
        current_ticks = str(self.tab_dic[self.name]['Tick_box'].text())
        self.ticker_list = pmt.ticker_parse(current_ticks)
   
        #Arguments required to run the External worker thread 
        num_portfolios = int(self.tab_dic[self.name]['Num_port'].currentText())
        min_b = int(self.tab_dic[self.name]['MinWeight'].currentText())
        max_b = int(self.tab_dic[self.name]['MaxWeight'].currentText())
        bounds = (min_b,max_b)
        
        #Initializes External worker thread which generates weight set perumutations while running a progress bar
        self.calc = External(self.ticker_list,num_portfolios,bounds)
        
        #Connects progress counter signal
        self.calc.countChanged.connect(self.onCountChanged)
        
        #Starts the thread worker
        self.calc.start()
        
        #Accepts signals from the worker thread when its job is completed
        self.calc.weights.connect(self.receive_data)
        self.calc.finished.connect(self.onFinished)
    
    def receive_data(self,weights):
        """Stores weight permutation set generated and transmitted by External worker thread
        """""
        
        self.weights = None
        if weights:
            self.weights = weights
    
    
    def graph_box_checked(self,b):
        """Test function to check checkbox functionality, can be deleted at a later point"""
        
        if b.isChecked():
            self.fig_els[self.name][b.text()] = True
        else:
            self.fig_els[self.name][b.text()] = False
            
        
    
    
    def param_gen(self):
        """Initializes a Portfolio class object for the current tab,
        then portfolio class methods are called to generate portfolio
        parameters
        """
        
        #Sets arguments to be passed to Portfolio class on initialization
        weights = self.weights
        dir_path = self.tab_dic[self.name]['Dir_box_text']
        freq = str(self.tab_dic[self.name]['Freq'].currentText())
        
        #Initializes Portfolio class object
        portfolio = Portfolio(self.ticker_list,dir_path,freq)
        
        #Generates portfolio parameters
        sec_params = portfolio.gen_sec_parameters()
        opt_params = portfolio.get_opt_portfolios(sec_params,weights,tolerance=0.2)
        
        #Adds portfolio data to the GUI data dictionary for later use
        self.data[self.name] = {'Params':sec_params,
                                'Optimization_Params':opt_params}
        
        #returns the parameter dictionaries generated
        
        return sec_params, opt_params
        
    def onFinished(self,fin):
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
            
            #Generates portfolio parameters
            sec_params, opt_params= self.param_gen()
            
            #stores portfolio parameters in GUI data dictionary
            self.data[self.name] ={'Securities':sec_params,
                                   'Optimization':opt_params}
            
            #intializes a graph widget to plot the generated portfolio data
            self.graphWidget = pgw.CustomCanvas(opt_params)
            
            
            #Generates a new layout object
            layout = self.resultsUI()
            
            #Stores that layout in the tab architecture dictionary
            self.tab_dic[self.name]['Layout'] = layout
            
            #Renders the new tab layout
            self.tabUI(state='change')
            
            #Sets GUI to the current tab
            self.tabdemo.setCurrentWidget(self.tabdemo.findChild(qtw.QWidget,self.name))
    
    def apply_plot_settings(self):
        """This function handles redrawing the central figure widget when
        new graph parameters are selected and applied from the GUI
        """
        
        
        #Gets button name for finding relevant entries in f_e dictionary
        sending_button = self.sender()
        self.name = sending_button.objectName()
        
        #Sets Figure Elements dictionary
        f_e = self.fig_els[self.name]
        
        #Gets items to be graphed from Figure Elements dictionary
        self.graph_items = [key for key,val in f_e.items() if val == True]
        
        #Gets optimization paramters dictionary
        opt_params = self.data[self.name]['Optimization']
        
        #Generates graph Widget
        self.graphWidget = pgw.CustomCanvas(opt_params,self.graph_items)
        
        #Reconstructs the tab layout
        layout = self.resultsUI()
        self.tab_dic[self.name]['Layout'] = layout
        
        #sets fig_els values to False. Boxes must be checked again to replot
        for key in self.fig_els[self.name].keys():
            self.fig_els[self.name][key] = False
        
        #Renders the GUI
        self.tabUI(state='change')
        self.tabdemo.setCurrentWidget(self.tabdemo.findChild(qtw.QWidget,self.name))
        
    def gen_report(self):
        """This function allows the user to save key information regarding their generated
        portfolio data to an excel file, which is commonly used in financial services
        """
        #Opens a file explorer window for the user to set a save file name/directory
        fname, _ = qtw.QFileDialog.getSaveFileName(self,
                                                   'Save File',
                                                   'c:/',
                                                   'Excel Files (*.xlsx)')
        
        
        #Gets list of portfolio asset tickers
        current_ticks = str(self.tab_dic[self.name]['Tick_box'].text())
        tickers = pmt.ticker_parse(current_ticks) 
        
        #Generates the report
        pmt.gen_report(tickers,self.data[self.name]['Optimization'],fname)
        
        
            
    def resultsUI(self):
        """Utilizes the results layout of the working tab after optimization processes have
        finished"""
        
        #Initializes layout widgets
        layout1a = qtw.QHBoxLayout()
        layout1 = qtw.QVBoxLayout()
        layout2 = qtw.QGridLayout()
        
        #Initializes label widgets
        label = qtw.QLabel('Plot Items')
        label2 = qtw.QLabel('')
        
        #Intializes checkbox widgets and connects functions to them
        chk1 = qtw.QCheckBox('Efficient Frontier')
        chk2 = qtw.QCheckBox('All Portfolios')
        chk1.toggled.connect(lambda:self.graph_box_checked(chk1))
        chk2.toggled.connect(lambda:self.graph_box_checked(chk2))
        
        #Initializes button widgets and connects functions to them
        apply_button = qtw.QPushButton('Apply')
        report_button = qtw.QPushButton('Generate Report')
        report_button.clicked.connect(self.gen_report)
        apply_button.setObjectName(self.name)
        apply_button.clicked.connect(self.apply_plot_settings)
        
        #Initializes a toolbar for navigating the rendered figure
        graph_tools = NavigationToolbar(self.graphWidget,self)
        
        #Initializes Widget wid1 sets layouts and adds child widgets
        wid1 = qtw.QWidget()
        layout1.addWidget(self.graphWidget)
        layout1.addWidget(qtw.QLabel(''))
        layout1.addWidget(graph_tools)
        wid1.setLayout(layout1)
        
        #Initalizes Widget wid1a sets layout and adds child widgets
        wid1a = qtw.QWidget()
        layout1a.addWidget(wid1)
        wid1a.setLayout(layout1a)
        
        #Initializes Widget wid2 sets layout and adds child widgets
        wid2 = qtw.QWidget()
        layout2.addWidget(label,0,0,1,1)
        layout2.addWidget(label2,1,0,1,1)
        layout2.addWidget(chk1,2,0,1,1)
        layout2.addWidget(chk2,3,0,1,1)
        layout2.addWidget(report_button,3,2,1,1)
        layout2.addWidget(apply_button,2,2,1,1)
        wid2.setLayout(layout2)
        
        
        
        
        
        
        
        #Initializes the main layout 'layout' and adds
        #The previously intializeds widgets to it
        layout = qtw.QVBoxLayout()
        layout.addWidget(wid1a)
        layout.addWidget(wid2)
        
        return layout
          
    
    def keyPressEvent(self, event):
        """This function handles all key events in the GUI"""
        #Ends program event loop
        if event.key() == qtc.Qt.Key_Q:
            print("Killing")
            self.deleteLater()
            
        #Returns the parameters of data points within lasso selection 
        elif event.key() == qtc.Qt.Key_Return:
            lsso = self.graphWidget.CustomPlot.lsso
            print(lsso.xys[lsso.ind])
        
        event.accept()
        
        
        
if __name__ == '__main__':
    """this allows you to intialize the window, the keys are the names of the portfolios
    and the tickers will populate ticker lineedit widgets make sure to download the 
    historical data files from the main repository and place them in the same folder 
    to run the optimization process"""
    
    pd = {'Hello':'AIG,BA,CVX','22':'CVX,IBM'}
    app = qtw.QApplication(sys.argv)
    mw = Results_Window(pd,'C:/')
    sys.exit(app.exec())
