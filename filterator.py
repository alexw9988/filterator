
import sys
import logging
logging.basicConfig(filename="filterator.log",format="%(levelname)-8s - %(module)-12s: %(message)s",level=logging.DEBUG, filemode='w')

from PyQt5 import QtCore, QtWidgets, QtGui

from gui.main import FilteratorMainWindow
from tree.model import TreeModel
from filters.model import FilterListModel
from processing.processor import Processor
from processing.manager import Manager
from filters.defaults import DEFAULTS


class Filterator(QtWidgets.QApplication):

    def __init__(self, *args, **kwargs):

        #Initialization
        super().__init__(*args, **kwargs)
        self.tree_model = TreeModel(self)
        self.filter_list_model = FilterListModel(DEFAULTS)
        self.main_window = FilteratorMainWindow(self)
        self.manager = Manager(self)
        self.processor = Processor()

        self.main_window.setupMainWindow(self.manager)
        self.manager.setupManager(self.main_window, self.processor)
        self.processor.setupProcessor(self.manager)
        
        #Multithreading
        self.processor_thread = QtCore.QThread()
        self.processor.moveToThread(self.processor_thread)
        self.processor_thread.start()
        
    def __call__(self):
        
        #Show MainWindow
        self.main_window.showMaximized() 
        self.main_window.raise_()

        #Start event loop 
        self.exec_()


if __name__ == '__main__':
    
    logging.debug("Creating application")
    application = Filterator(sys.argv)

    # file = QtCore.QFile("resources/dark.qss")
    # file.open(QtCore.QFile.ReadOnly | QtCore.QFile.Text)
    # stream = QtCore.QTextStream(file)
    # application.setStyleSheet(stream.readAll())

    logging.debug("Launching application")
    application()

    logging.debug("Quitting application")

