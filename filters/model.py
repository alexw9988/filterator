
from PyQt5 import QtCore, QtGui, QtWidgets

from tree.items import Item


class FilterListModel(QtGui.QStandardItemModel):

    def __init__(self, filter_dict=None):
        super().__init__()

        if filter_dict: self.loadList(filter_dict)

    def loadList(self, filter_dict):
        
        for name, contents in filter_dict.items():
            full_name = contents['full_name']
            fn = contents['fn']
            try:
                description = contents['description']
            except KeyError:
                description = ""
            default_params = contents['default_params']

            item = Item.createFilterItem(name, full_name, description=description, fn=fn, params=default_params)

            self.appendRow(item)


            