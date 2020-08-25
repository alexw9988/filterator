
import logging

from PyQt5 import QtCore, QtGui, QtWidgets

from tree.items import Item


class PreProcessedDelegate(QtWidgets.QStyledItemDelegate):

    def __init__(self):
        super().__init__()

    def initStyleOption(self, option, index):
        super().initStyleOption(option, index)
        if index.data(Item.TYPE) == Item.INPUT_TYPE:
            option.features &= ~QtWidgets.QStyleOptionViewItem.HasCheckIndicator


class PostProcessedDelegate(QtWidgets.QStyledItemDelegate):

    def __init__(self):
        super().__init__()

    def initStyleOption(self, option, index):
        super().initStyleOption(option, index)
        if index.data(Item.IS_PROCESSED):
            option.font.setItalic(False)
        else:
            option.font.setItalic(True)
        
        if index.data(Item.HAS_PROCESSING_ERROR):
            option.palette.setBrush(QtGui.QPalette.Text, QtGui.QColor(255, 0, 0))

        option.features &= ~QtWidgets.QStyleOptionViewItem.HasCheckIndicator
    
    