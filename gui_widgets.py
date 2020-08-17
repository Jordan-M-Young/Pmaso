from PyQt5 import QtCore as qtc
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg



class CustomComboBox(qtw.QComboBox):
    """Custom ComboBox widget class
    
    Initializes a custom combobox widget for the GUI,
    takes one box_type string as an argument
    """
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
            
            
            
            
            
            
            
        
