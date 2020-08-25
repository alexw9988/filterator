
import logging
import numpy as np

from func_timeout import func_timeout, FunctionTimedOut
from PIL import Image
from PyQt5 import QtCore, QtGui, QtWidgets

from tree.items import Item


class ProcessorSignals(QtCore.QObject):
    item_processed = QtCore.pyqtSignal(Item)


class Processor(QtCore.QObject):

    TIMEOUT = 10

    def __init__(self):
        super().__init__()
        self.signals = ProcessorSignals()
        self.manager = None

    def setupProcessor(self, manager):
        self.manager = manager
        self.manager.signals.process_from[Item, object].connect(self.process)

    @QtCore.pyqtSlot(Item, Item)
    def process(self, item, input_item):

        logging.debug("Processor starting item {} with id {}".format(item.full_name, item.id))
        
        try:
            if item.type() == Item.INPUT_TYPE:
                params = item.getParamValueDict()
                path = params['input_path']

                output = np.array(Image.open(path))

            elif item.type() == Item.FILTER_TYPE:
                input_array = input_item.output
                params = item.getParamValueDict()
                fn = item.fn
                
                try:
                    output = func_timeout(self.TIMEOUT,fn,args=(input_array, params))
                except FunctionTimedOut:
                    raise ProcessingError("Filter timed out!")

            elif item.type() == Item.GROUP_TYPE:
                if not item.hasChildren():
                    raise ProcessingError("Group has no children!")
                
                children = [child for child in item.children()]
                child_count = item.rowCount()
                last_active_child = None
                pos = child_count - 1

                while pos >= 0:
                    child = children[pos]
                    if child.is_active:
                        last_active_child = child
                        break
                    pos -= 1

                if last_active_child is None:
                    raise ProcessingError("Group has no active children")        
                else:
                    output = np.copy(last_active_child.output)              

            elif item.type() == Item.MODIFIER_TYPE:
                if not item.hasChildren():
                    raise ProcessingError("Modifier has no children!")

                child_count = item.rowCount()
                
                mode = item.params['mode']['value']
                clip = item.params['clip']['value']
                img_list = []
                coeff_list = []
                for child in item.children():
                    if child.is_active:
                        img_list.append(child.output)
                        coeff_list.append(child.params['modifier_coefficient']['value'])
                
                if len(img_list) == 0:
                    raise ProcessingError("Modifier has no active children!")

                output = self._modifier(img_list, coeff_list, mode, clip)

        except Exception as e:
            logging.warning("Processor has error: {}".format(repr(e)))
            item.output = None
            item.is_processed = False
            item.has_processing_error = True
            item.status_message = repr(e)
        else:
            logging.debug("Processor was successful")
            item.output = output
            item.is_processed = True
            item.has_processing_error = False
            item.status_message = "Processing ok."
        finally:
            self.signals.item_processed.emit(item)
            logging.debug("Processor returning item")

    @staticmethod
    def _modifier(img_list, coeff_list, mode, clip):
        if len(img_list) != len(coeff_list):
            raise ValueError("img_list and coeff_list don't have same length in modifier!")
        
        #if None in img_list:
        #    raise ProcessingError("At least one modifier child is not processed!")

        output = img_list[0] * coeff_list[0]

        if mode == 'add':
            for i in range(1, len(img_list)):
                output = np.add(img_list[i]*coeff_list[i], output)
        elif mode == 'multiply':
            for i in range(1, len(img_list)):
                output = np.multiply(img_list[i]*coeff_list[i], output)
        else:
            raise ProcessingError("Invalid modifier mode!")

        if clip:
            if output.dtype == np.uint8:
                minimum = 0
                maximum = 255
            elif output.dtype == np.float64:
                minimum = 0.0
                maximum = 1.0
            elif output.dtype == np.bool:
                minimum = 0
                maximum = 1
            else:
                return output
            
            output = np.clip(output, minimum, maximum)
        else:
            minimum = np.amin(output)
            maximum = np.amax(output)
            
            if output.dtype == np.uint8:
                output = np.subtract(output, minimum)
                output = np.multiply(output, 255/maximum, dtype=np.uint8)
            elif output.dtype == np.float64:
                output = np.subtract(output, minimum)
                output = np.multiply(output, 1/maximum, dtype=np.float64)
            elif output.dtype == np.bool:
                output = np.subtract(output, minimum)
                output = np.multiply(output, 1/maximum, dtype=np.bool)
            else:
                return output

        return output


class ProcessingError(Exception):
    pass