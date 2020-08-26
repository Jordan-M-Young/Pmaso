from matplotlib.figure import Figure
from matplotlib.widgets import LassoSelector
from matplotlib.path import Path
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import numpy as np
from PyQt5 import QtCore as qtc
from PyQt5 import QtWidgets as qtw



class CustomComboBox(qtw.QComboBox):
    
    def __init__(self,box_type='Freq'):
        qtw.QComboBox.__init__(self)
        
        self.box_type = box_type
        
        self.get_box_choices()
        
        for choice in self.box_choices:
            self.addItem(choice)
            
    
    def get_box_choices(self):
            
        if self.box_type == 'Freq':
            self.box_choices = ['Daily','Weekly','Monthly']
        
        elif self.box_type == 'MaxW':
            #Choices are 50 - 100 in increments of 5
            self.box_choices = [str(50 + (5*i)) for i in range(11)]
        
        elif self.box_type == 'MinW':
            #Choices are 0 - 20 in increments of five
            self.box_choices = [str(5*i) for i in range(5)]
        else:
            self.box_choices = ['100','500','1000','5000','10000','50000']
            
        
    

class SelectFromCollection(object):
    """Select indices from a matplotlib collection using `LassoSelector`.

    Selected indices are saved in the `ind` attribute. This tool fades out the
    points that are not part of the selection (i.e., reduces their alpha
    values). If your collection has alpha < 1, this tool will permanently
    alter the alpha values.

    Note that this tool selects collection objects based on their *origins*
    (i.e., `offsets`).

    Parameters
    ----------
    ax : :class:`~matplotlib.axes.Axes`
        Axes to interact with.

    collection : :class:`matplotlib.collections.Collection` subclass
        Collection you want to select from.

    alpha_other : 0 <= float <= 1
        To highlight a selection, this tool sets all selected points to an
        alpha value of 1 and non-selected points to `alpha_other`.
    """

    def __init__(self, ax, collection, alpha_other=0.3):
        self.canvas = ax.figure.canvas
        self.collection = collection
        self.alpha_other = alpha_other

        self.xys = collection.get_offsets()
        self.Npts = len(self.xys)

        # Ensure that we have separate colors for each object
        self.fc = collection.get_facecolors()
        if len(self.fc) == 0:
            raise ValueError('Collection must have a facecolor')
        elif len(self.fc) == 1:
            self.fc = np.tile(self.fc, (self.Npts, 1))
        
        lineprops = {'color': 'red'}            
        self.lasso = LassoSelector(ax, 
                                   onselect=self.onselect, 
                                   lineprops=lineprops)
        self.ind = []

    def onselect(self, verts):
        path = Path(verts)
        self.ind = np.nonzero(path.contains_points(self.xys))[0]
        self.fc[:, -1] = self.alpha_other
        self.fc[self.ind, -1] = 1
        self.collection.set_facecolors(self.fc)
        self.canvas.draw_idle()

    
    def onPress(self,event):
    	print('Mouse pressed')
    
    def onRelease(self,event):
    	print('Mouse released')
        
        
    


class CustomPlot():
    
    def __init__(self,fig,ax,pts):
        
        
        self.fig = fig
        self.ax = ax
        self.pts = pts
        
        self.lineprops = {'color': 'red', 'linewidth': 4, 'alpha': 0.8}
        self.lsso = SelectFromCollection(self.ax, self.pts)
        
        self.fig.canvas.mpl_connect('button_press_event', self.lsso.onPress)
        self.fig.canvas.mpl_connect('button_release_event', self.lsso.onRelease)
        
        
        
        

    def ret_lasso(self):
        print(self.lsso)




class CustomCanvas(CustomPlot,FigureCanvas):

    def __init__(self,opt_params,p_items=['All Portfolios']):
        
        
        self.fig = Figure(figsize=(7,6), dpi=100)
        self.ax1 = self.fig.add_subplot(111)
        
        
        self.opt_params = opt_params    
        
        
        #These two lines are why actual best values are not plotting!!!!
        
        p_r = np.array(self.opt_params['Portfolio_Space_Stds'])
        p_s = np.array(self.opt_params['Portfolio_Space_Returns'])
        
        
        
        
        
        e_f = self.opt_params['Frontier_Vals'].T
        
        
        if p_items:
            if 'All Portfolios' in p_items and 'Efficient Frontier' in p_items:
                self.pts = self.ax1.scatter(p_r,p_s)
                self.ax1.plot(e_f[:,0],e_f[:,1],color='r')
            
            elif 'All Portfolios' in p_items:
                self.pts = self.ax1.scatter(p_r,p_s)
            elif 'Efficient Frontier' in p_items:
                self.ax1.plot(e_f[:,0],e_f[:,1],color='r')
                self.pts = self.ax1.scatter(np.min(e_f[:,0]),np.min(e_f[:,1]),color='w')
            else:
                self.pts = self.ax1.scatter(np.array([0]),np.array([0]),color='w')
        else:
            self.pts = self.ax1.scatter(np.array([0]),np.array([0]),color='w')
        
        
        # ax1 settings
        self.ax1.set_xlabel('Expected Returns (%)')
        self.ax1.set_ylabel('Standard Deviation')
     
        

        FigureCanvas.__init__(self, self.fig)
        self.CustomPlot = CustomPlot(self.fig,self.ax1,self.pts)
        
        
        
class TableModel(qtc.QAbstractTableModel):
    def __init__(self,dat=None,tickers=None):
        super().__init__()
        if dat == None:
            self._data = [[None,None,None,None,None],
                          [None,None,None,None,None],
                          [None,None,None,None,None]]
        else:
            self._data = dat
            
        self._headers =['Std Deviation','Returns','Sharpe Ratio',
                        'Alpha','Beta']    
        if tickers:
            for i in reversed(range(len(tickers))):
                self._headers.insert(6,tickers[i])
      
        
    def rowCount(self,parent):
        return len(self._data)
    
    def columnCount(self,parent):
        return len(self._headers)
    
    def data(self,index,role):
        if role == qtc.Qt.DisplayRole:
            return self._data[index.row()][index.column()]
    
    def headerData(self,section,orientation,role):
        
        if (
            orientation == qtc.Qt.Horizontal and
            role == qtc.Qt.DisplayRole
            ):
            return self._headers[section]
        else:
            return super().headerData(section, orientation, role)
    
    def sort(self, column, order):
        self.layoutAboutToBeChanged.emit()
        self._data.sort(key=lambda x: x[column])
        if order == qtc.Qt.DescendingOrder:
            self._data.reverse()
        self.layoutChanged.emit()
            
            
            
        
