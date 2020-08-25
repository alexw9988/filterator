
import os
import json 
import math
import logging
import numpy as np

from PyQt5 import QtCore, QtGui, QtWidgets 
from PyQt5.uic import loadUiType
from pyqtgraph import ImageView, TextItem, InfiniteLine, SignalProxy

from tree.model import TreeModel
from tree.items import Item
from processing.manager import Manager 
from gui.widgets import ParametersWidget, PreProcessedTree, PostProcessedTree, ImagePropertiesView, FilteratorImageView

Ui_MainWindow, QMainWindow = loadUiType('gui/main.ui')


class FilteratorMainWindowSignals(QtCore.QObject):
    item_modified = QtCore.pyqtSignal(Item)
    items_moved = QtCore.pyqtSignal(list)

class FilteratorMainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self, app):

        #Initialisation
        super().__init__()
        self.setupUi(self)

        #Defaults
        self.app = app
        self.tree_model = app.tree_model
        self.filter_list_model = app.filter_list_model
        self.signals = FilteratorMainWindowSignals()
        self.display_image = None
        self.current_saved = True

        #Update Ui
        self.customUiSetup()
        self.updateUiState()

        #Connections
        self.pb_add_filter.clicked.connect(lambda: self.onAddItem(item_type='filter'))
        self.pb_add_group.clicked.connect(lambda: self.onAddItem(item_type='group'))
        self.pb_add_modifier.clicked.connect(lambda: self.onAddItem(item_type='modifier'))
        self.pb_delete.clicked.connect(self.onDeleteItem)
        self.pb_load_json.clicked.connect(self.onLoadJson)
        self.pb_save_json.clicked.connect(self.onSaveJson)
        self.pb_clear.clicked.connect(self.onClearAll)

        self.pb_load_image.clicked.connect(self.onLoadImage)
        self.pb_save_image.clicked.connect(self.onSaveImage)

        self.tree_pre.selectionModel().currentChanged[QtCore.QModelIndex, QtCore.QModelIndex].connect(self.onPreSelectionChanged)
        self.tree_post.selectionModel().currentChanged[QtCore.QModelIndex, QtCore.QModelIndex].connect(self.onPostSelectionChanged)

        self.tree_model.itemChanged.connect(self.onItemChange)

    def setupMainWindow(self, manager):
        self.manager = manager
        self.manager.signals.item_processed.connect(self.onItemProcessed)

    def onItemChange(self, item):
        self.current_saved = False

    def onSaveImage(self):
        if self.image_view.getImageItem() is None:
            return
        
        reply = QtWidgets.QFileDialog.getSaveFileName(self, caption="Save image",filter="PNG File (*.png)")
        full_path = reply[0]

        if not full_path: 
            return
        
        self.image_view.export(full_path)

    def onLoadImage(self):

        logging.debug("Getting input image path")
        path = QtWidgets.QFileDialog.getOpenFileName(self, 'Open Image', '', 'PNG (*.png);; All Files (*);; ')[0]
        
        if path != '':
            if self.tree_model.hasInputItem():
                logging.debug("Input item already exists. Replacing path.")
                input_item = self.tree_model.input_item
                input_item.updateParam('input_path',path)
                self.signals.item_modified.emit(self.tree_model.input_item)
            else:
                logging.debug("Input item does not exist. Clearing tree and inserting new input item.")
                if not self.onClearAll():
                    return
                input_item = Item.createInputItem(input_path=path)
                result = self.tree_model.insertItem(input_item)
                if result == self.tree_model.INSERT_FAILED:
                    logging.debug("Image loading aborted")
                    return 

            logging.info("Loaded image from path {}".format(path))
            self.tree_pre.selectionModel().clear()
            self.tree_pre.selectionModel().setCurrentIndex(input_item.index(), QtCore.QItemSelectionModel.SelectCurrent)
            self.displayParametersWidget(input_item)
            self.tree_pre.repaint()

            self.signals.item_modified.emit(input_item)

    def onAddItem(self, item_type):

        if item_type == 'filter':
            index = self.cb_add_filter.currentIndex()
            item = self.filter_list_model.item(index).clone()
        elif item_type == 'group':
            item = Item.createGroupItem()
        elif item_type == 'modifier':
            item = Item.createModifierItem()

        sel_model = self.tree_pre.selectionModel()
        insert_index = sel_model.currentIndex()
        insert_at = self.tree_model.itemFromIndex(insert_index)

        result = self.tree_model.insertItem(item, insert_at=insert_at)

        if result == self.tree_model.INSERT_SUCCESSFUL:
            self.tree_pre.selectionModel().clear()
            self.tree_pre.selectionModel().setCurrentIndex(item.index(), QtCore.QItemSelectionModel.SelectCurrent)
            self.displayParametersWidget(item)
            self.tree_pre.repaint()

            self.signals.item_modified.emit(item)

    def onDeleteItem(self):

        sel_model = self.tree_pre.selectionModel()
        tree_model = self.app.tree_model

        index = sel_model.currentIndex()
        item = tree_model.itemFromIndex(index)

        if not item: 
            return

        sel_item, exitcode = self.tree_model.removeItem(item)

        if exitcode == self.tree_model.REMOVE_SUCCESFUL:
            self.tree_pre.selectionModel().clear()
            if sel_item:
                sel_index = sel_item.index()
                self.tree_pre.selectionModel().setCurrentIndex(sel_index, QtCore.QItemSelectionModel.SelectCurrent)
            self.displayParametersWidget(sel_item)
            if sel_item:
                self.signals.item_modified.emit(sel_item)
            self.tree_pre.repaint()

    def onLoadJson(self):
        if self.tree_model.rowCount() > 0: 
            reply = QtWidgets.QMessageBox.question(self, 'Load JSON', 
                    'Do you really want to load an exisiting tree? This will overwrite the current tree!', 
                    QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No)
            if reply == QtWidgets.QMessageBox.No: return 
        
        reply = QtWidgets.QFileDialog.getOpenFileName(self, caption="Load tree from JSON",filter="JSON file (*.json)")
        full_path = reply[0]
        if not full_path: 
            return

        with open(full_path) as json_file:
            tree_list = json.load(json_file)

        result = self.tree_model.loadTree(tree_list)
        if result == self.tree_model.LOAD_SUCCESSFUL: 
            if self.tree_model.hasInputItem():
                self.signals.item_modified.emit(self.tree_model.input_item)
        elif result == self.tree_model.LOAD_FAILED or result == self.tree_model.LOAD_EXCEPTION:
            QtWidgets.QMessageBox.warning(self, 'Load JSON',
                    'An exception occured while loading the tree. Check log file.',
                    QtWidgets.QMessageBox.Ok)

        self.tree_pre.expandAll()
        self.tree_post.expandAll()

        self.current_saved = True
        
    def onSaveJson(self):
        if self.app.tree_model.rowCount() == 0: 
            return True
        reply = QtWidgets.QFileDialog.getSaveFileName(self, caption="Save tree to JSON",filter="JSON file (*.json)")
        full_path = reply[0]

        if not full_path: 
            return False
        if os.path.splitext(full_path)[1] != ".json":
            QtWidgets.QMessageBox.warning(self, "Invalid filename", "Invalid filename: Extension must be .json!",QtWidgets.QMessageBox.Ok)
            return False
        
        tree_list = self.app.tree_model.saveTree()
        with open(full_path, 'w') as outfile:
            json.dump(tree_list, outfile)

        self.current_saved = True
        return True
        
    def onClearAll(self):
        if self.app.tree_model.rowCount() == 0: 
            return True

        reply = QtWidgets.QMessageBox.question(self, 'Clear all', 
                 'Do you really want to clear all items?', QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            self.tree_model.clear()
            self.displayParametersWidget(None)
            return True
        else:
            return False

    @QtCore.pyqtSlot(QtCore.QModelIndex, QtCore.QModelIndex)
    def onPreSelectionChanged(self, current, previous):
        item = self.tree_model.itemFromIndex(current)
        self.displayParametersWidget(item)

    @QtCore.pyqtSlot(QtCore.QModelIndex, QtCore.QModelIndex)
    def onPostSelectionChanged(self, current, previous):
        item = self.tree_model.itemFromIndex(current)
        self.displayProcessedItem(item)

    @QtCore.pyqtSlot(Item)
    def onItemProcessed(self, item):
        curr_index = self.tree_post.currentIndex()
        sel_item = self.tree_model.itemFromIndex(curr_index)
        if sel_item is None:
            return
        
        item_rank = self.tree_model.getItemRank(item)
        sel_rank = self.tree_model.getItemRank(sel_item)

        if sel_rank < item_rank:
            self.displayProcessedItem(sel_item)
        elif sel_rank == item_rank:
            parent = sel_item.parent()
            if parent is None or parent.type() == Item.GROUP_TYPE:
                self.displayProcessedItem(sel_item)

    def displayParametersWidget(self, item):
        if self.widget_parameters.layout().count() > 0:
            child = self.widget_parameters.layout().takeAt(0)
            while child:
                del child
                child = self.widget_parameters.layout().takeAt(0)

        self.parameters_widget_obj = ParametersWidget(item)
        self.parameters_widget_obj.value_changed_signal.connect(lambda: self.signals.item_modified.emit(item))
        self.widget_parameters.layout().addWidget(self.parameters_widget_obj)
    
    def displayProcessedItem(self, item):
        if item is None:
            self.image_view.clear()
            self.image_view.setProcessed(status=True)
            self.view_item_info.clear()
        else:
            img = item.output
            self.display_image = img

            if img is None: 
                self.image_view.clear()
                self.view_image_properties.clear()

            else:
                image_item = self.image_view.getImageItem()
                auto_range = False if image_item else True

                if img.ndim == 2: 
                    self.image_view.setImage(img, axes = {'x':1, 'y':0}, autoRange=auto_range)
                elif img.ndim == 3:
                    self.image_view.setImage(img, axes = {'x':1, 'y':0, 'c':2}, autoRange=auto_range)
                else:
                    self.image_view.clear()
                
                self.view_image_properties.setImageProperties(minimum=np.amin(img),
                    maximum=np.amax(img), dtype=img.dtype, resolution=img.shape)

            self.image_view.setProcessed(status=item.is_processed)

            status_message = item.status_message
            self.view_item_info.setText(status_message)
    
    @QtCore.pyqtSlot(tuple)
    def onImageViewPosUpdate(self, coords):
        if self.display_image is None:
            self.lbl_x.setText("")
            self.lbl_y.setText("")
            self.lbl_value.setText("")

        x = int(coords[0])
        y = int(coords[1])
        
        if 0 <= x < self.display_image.shape[1] and 0 <= y < self.display_image.shape[0]:
            self.lbl_x.setText(str(x))
            self.lbl_y.setText(str(y))
            if self.display_image.ndim == 2:
                self.lbl_value.setText("{:.3f}".format(float(self.display_image[y, x])))
            else:
                self.lbl_value.setText(str(self.display_image[y, x]))
        
    def updateUiState(self, update_selection=None):
        pass

    def customUiSetup(self):

        #Setup views
        self.tree_pre = PreProcessedTree(self, parent=self.widget_pre)
        self.tree_pre.setModel(self.tree_model)
        self.lay_tree_pre.addWidget(self.tree_pre)

        self.tree_post = PostProcessedTree(self, parent=self.widget_post)
        self.tree_post.setModel(self.tree_model)
        self.lay_tree_post.addWidget(self.tree_post)

        #Setup image view
        self.image_view = FilteratorImageView(parent=self.widget_view)
        self.image_view.signals.mouse_pos_updated.connect(self.onImageViewPosUpdate)
        self.widget_view.layout().addWidget(self.image_view)

        #Setup image properties text view
        self.view_image_properties = ImagePropertiesView(self, parent=self.widget_post)
        self.widget_post.layout().addWidget(self.view_image_properties)

        #Setup filter combobox
        self.cb_add_filter.setModel(self.app.filter_list_model)

        #Set icons
        self.pb_load_image.setIcon(QtGui.QIcon('resources/input_new.png'))
        self.pb_add_group.setIcon(QtGui.QIcon('resources/folder_new.png'))
        self.pb_add_modifier.setIcon(QtGui.QIcon('resources/modifier_new.png'))
        self.pb_add_filter.setIcon(QtGui.QIcon('resources/filter_new.png'))
        self.pb_delete.setIcon(QtGui.QIcon('resources/delete.png'))

    def closeEvent(self, event):
        if self.current_saved: 
            event.accept()
        else:
            msgbox = QtWidgets.QMessageBox(self)
            msgbox.setWindowTitle('Unsaved Tree')
            msgbox.setIcon(QtWidgets.QMessageBox.Warning)
            msgbox.setText('Do you want to save the current tree before quitting?')
            msgbox.setStandardButtons(QtWidgets.QMessageBox.Discard|QtWidgets.QMessageBox.Save|QtWidgets.QMessageBox.Cancel)
            reply = msgbox.exec()
            
            if reply == QtWidgets.QMessageBox.Discard:
                event.accept()
            elif reply == QtWidgets.QMessageBox.Save:
                if self.onSaveJson(): 
                    event.accept()
                else:
                    event.ignore()
            elif reply == QtWidgets.QMessageBox.Cancel:
                event.ignore()
            else:
                event.accept()