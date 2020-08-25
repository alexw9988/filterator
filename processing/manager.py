
import logging

from PyQt5 import QtCore, QtGui, QtWidgets

from tree.items import Item


class ManagerSignals(QtCore.QObject):
    process_from = QtCore.pyqtSignal(Item, object)
    item_processed = QtCore.pyqtSignal(Item)


class Manager():
    
    def __init__(self, app):
        super().__init__()
        self.signals = ManagerSignals()
        self.app = app
        self.main_window = None

        self.tree_model = app.tree_model
        self.processor = None
        self.processor_busy = False
        
        self.lock = ManagerLock(self)

    def setupManager(self, main_window, processor):
        self.main_window = main_window
        self.main_window.signals.item_modified[Item].connect(self.handleItemChange)
        self.main_window.signals.items_moved[list].connect(self.handleItemMove)

        self.processor = processor
        self.processor.signals.item_processed[Item].connect(self.handleResult)

    def _findFirstUnprocessed(self):
        input_item = self.tree_model.input_item

        for item in self.tree_model.iterateTree(input_item, yield_none=True, exit_modifier=False):
            if not item:
                logging.info("No unprocessed item found.")
                return None
            if not item.is_processed:
                logging.debug("First unprocessed item is {} with id {}".format(item.full_name, item.id))
                return item
        
    def handleItemChange(self, item):
        logging.debug("Received change from item {} with id {}".format(item.full_name, item.id))
        curr_item = item

        for curr_item in self.tree_model.iterateTree(item, ignore_active_status=True):
            curr_item.is_processed = False
            curr_item.has_processing_error = False
            curr_item.status_message = "Not processed"
            curr_item.resetId()
            logging.debug("Reset item {} with new id {}".format(curr_item.full_name, curr_item.id))

        self.tryProcess()

    def handleItemMove(self, item_list):
        
        if item_list[1] is None:
            logging.debug("Received item moved signal with items {} and None".format(item_list[0].full_name))
            item_list.pop(1)
        else: 
            logging.debug("Received item moved signal with items {} and {}".format(item_list[0].full_name, item_list[1].full_name))
  
        for curr_item in item_list:
            
            is_first_item = True
            for curr_item in self.tree_model.iterateTree(curr_item, ignore_active_status=True):
                if curr_item.is_processed == False and not is_first_item:
                    is_first_item = False
                    break

                curr_item.is_processed = False
                curr_item.has_processing_error = False
                curr_item.status_message = "Not processed"
                curr_item.resetId()
                logging.debug("Reset item {} with new id {}".format(curr_item.full_name, curr_item.id))

        self.tryProcess()

    def tryProcess(self, item=None, input_item=None):
        
        if self.processor_busy:
            logging.debug("Processor busy, call aborted.")
            return
        
        if item is None:
            item = self._findFirstUnprocessed()
            if item is None:
                logging.debug("No unprocesssed item found. Tree done processing.")
                return
            else:
                logging.debug("Processing from first unprocessed item: {}".format(item.full_name))

        if input_item is None:
            input_item = self.tree_model.getPrev(item)

        self.processor_busy = True
        item_clone = item.clone(keep_id=True, keep_children_mode='first', keep_children_output=True)
        if input_item: 
            input_clone = input_item.clone(keep_id=True, keep_output=True, keep_children_mode='none')
            logging.debug("Calling processor with item {} (id: {}) and input item {} (id: {})".format(item_clone.full_name, item_clone.id, input_clone.full_name, input_clone.id))
        else:
            input_clone = None
            logging.debug("Calling processor with item {} (id: {}) and input item None".format(item_clone.full_name, item_clone.id))
            
        self.signals.process_from.emit(item_clone, input_clone)

    def handleResult(self, item): 
        
        logging.debug("Received item from processor {} (processed: {}, error: {}, message: {}, id: {})".format(item.full_name, item.is_processed, item.has_processing_error, item.status_message, item.id))
        self.processor_busy = False
        item_id = item.id

        for curr_item in self.tree_model.iterateTree(self.tree_model.input_item, yield_none=True, exit_modifier=False):
            if not curr_item:
                item_matched = False
                logging.debug("Item could not be matched to tree")
                break
            if curr_item.id == item_id:
                item_matched = True
                logging.debug("Item was matched to tree")
                break
        
        if item_matched:
            curr_item.output = item.output
            curr_item.is_processed = item.is_processed
            curr_item.has_processing_error = item.has_processing_error
            curr_item.status_message = item.status_message
            
            self.signals.item_processed.emit(curr_item)

            if item.has_processing_error:
                logging.debug("Item has processing error, stop processing")
                return 

            next_item, _ = self.tree_model.getNext(curr_item)
            if not next_item:
                logging.debug("No next item found, tree done processing.")
                return
            
            self.tryProcess(next_item)
        
        else:
            self.tryProcess()
            

class ManagerLock():
    def __init__(self, manager):
        self.manager = manager 
    
    def __enter__(self):
        logging.debug("ManagerLock acquired!")
        self.manager.main_window.signals.item_modified[Item].disconnect(self.manager.handleItemChange)
        self.manager.main_window.signals.items_moved[list].disconnect(self.manager.handleItemMove)

    def __exit__(self, type_, value, traceback):
        if type_ is None:
            logging.debug("ManagerLock released!")
            self.manager.main_window.signals.item_modified[Item].connect(self.manager.handleItemChange)
            self.manager.main_window.signals.items_moved[list].connect(self.manager.handleItemMove)

    def acquire(self): 
        logging.debug("ManagerLock acquired!")
        self.manager.main_window.signals.item_modified[Item].disconnect(self.manager.handleItemChange)
        self.manager.main_window.signals.items_moved[list].disconnect(self.manager.handleItemMove)

    def release(self):
        self.manager.main_window.signals.item_modified[Item].connect(self.manager.handleItemChange)
        self.manager.main_window.signals.items_moved[list].connect(self.manager.handleItemMove)
        logging.debug("ManagerLock released!")