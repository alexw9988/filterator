
import copy
import time 
import logging
import collections

from PyQt5 import QtCore, QtGui, QtWidgets


class Item(QtGui.QStandardItem):

    #TYPE constants: use Item.type() to return item type
    FILTER_TYPE = QtGui.QStandardItem.UserType + 1
    MODIFIER_TYPE = QtGui.QStandardItem.UserType + 2
    GROUP_TYPE = QtGui.QStandardItem.UserType + 3
    INPUT_TYPE = QtGui.QStandardItem.UserType + 10

    #DATA ROLE constants: use with Item.setData(value, role) or Item.data(role)
    TYPE = QtCore.Qt.UserRole + 100
    NAME = QtCore.Qt.UserRole + 200
    IS_PROCESSED = QtCore.Qt.UserRole + 500
    HAS_PROCESSING_ERROR = QtCore.Qt.UserRole + 501
    STATUS_MESSAGE = QtCore.Qt.UserRole + 502
    OUTPUT = QtCore.Qt.UserRole + 600
    FN = QtCore.Qt.UserRole + 700
    PARAMS = QtCore.Qt.UserRole + 900
    ID = QtCore.Qt.UserRole + 1000

    def __init__(self):
        super().__init__()

        self.name = ""
        self.full_name = ""
        self.description = ""

        self.fn = None
        self.params = None

        self.is_active = True
        self.is_processed = False
        self.has_processing_error = False
        self.status_message = "Not processed"
        self.output = None

        self.id = str(time.time()) #Item id is the current time, converted to string. This ensures uniqueness

    def __getattribute__(self, name):
        if name == 'name':
            return self.data(self.NAME)
        elif name == 'full_name':
            return self.data(QtCore.Qt.DisplayRole)
        elif name == 'description':
            return self.data(QtCore.Qt.ToolTipRole)
        elif name == 'fn':
            return self.data(self.FN)
        elif name == 'params':
            return self.data(self.PARAMS)
        elif name == 'is_active':
            value = self.data(QtCore.Qt.CheckStateRole)
            return True if value == QtCore.Qt.Checked else False
        elif name == 'is_processed':
            return self.data(self.IS_PROCESSED)
        elif name == 'has_processing_error':
            return self.data(self.HAS_PROCESSING_ERROR)
        elif name == 'status_message':
            return self.data(self.STATUS_MESSAGE)
        elif name == 'output':
            return self.data(self.OUTPUT)
        elif name == 'id':
            return self.data(self.ID)
        elif name == 'icon':
            return Item._getIcon(self)
        else:
            return super().__getattribute__(name)

    def __setattr__(self, name, value):
        if name == 'name':
            self.setData(value, self.NAME)
        elif name == 'full_name':
            self.setData(value, QtCore.Qt.DisplayRole)
            self.setData(value, QtCore.Qt.EditRole)
        elif name == 'description':
            self.setData(value, QtCore.Qt.ToolTipRole)
        elif name == 'fn':
            self.setData(value, self.FN)
        elif name == 'params': 
            self.setData(value, self.PARAMS)
        elif name == 'is_active':
            if type(value) == bool:
                value = QtCore.Qt.Checked if value else QtCore.Qt.Unchecked
            self.setData(value, QtCore.Qt.CheckStateRole)
        elif name == 'is_processed':
            self.setData(value, self.IS_PROCESSED)
        elif name == 'has_processing_error':
            self.setData(value, self.HAS_PROCESSING_ERROR)
        elif name == 'status_message':
            self.setData(value, self.STATUS_MESSAGE)
        elif name == 'output':
            self.setData(value, self.OUTPUT)
        elif name == 'id':
            self.setData(value, self.ID)
        else:
            super().__setattr__(name, value)  

    def updateParam(self, name, value):
        params = self.params
        params[name]['value'] = value
        self.params = params

    def resetId(self):
        self.id = str(time.time())

    def clone(self, keep_id=False, keep_output=False, keep_children_mode='all', keep_children_output=False):
        
        item = Item()
        item.name = self.name
        item.full_name = self.full_name
        item.description = self.description
        
        item.fn = self.fn
        item.params = copy.deepcopy(self.params)
        
        item.is_active = self.is_active

        item.setData(self.type(), self.TYPE)
        item.setData(Item._getIcon(item), QtCore.Qt.DecorationRole)
        item.setFlags(Item._getFlags(item))

        if keep_id:
            item.id = self.id

        if keep_output:
            item.output = self.output
    
        if keep_children_mode.lower() == 'all':
            for child in self.children():
                child_clone = child.clone(keep_id=keep_id, 
                keep_output=keep_children_output, keep_children_mode='all')
                item.appendRow(child_clone)

        elif keep_children_mode.lower() == 'first':
            for child in self.children():
                child_clone = child.clone(keep_id=keep_id, 
                keep_output=keep_children_output, keep_children_mode='none')
                item.appendRow(child_clone)
        
        else:
            pass

        logging.debug("Cloned item {} (keep_id={}, keep_output={}, keep_children_mode={}, keep_children_output={})".format(item.full_name, keep_id, keep_output, keep_children_mode, keep_children_output))
        
        return item

    def setParamValueDict(self, params): 
        for name, value in params.items():
            self.updateParam(name, value)

    def getParamValueDict(self):
        params = collections.OrderedDict()
        for name, param in self.params.items():
            params[name] = param['value']
        return params

    def children(self):
        child_count = self.rowCount()
        if self.hasChildren():
            for child_i in range(child_count):
                yield self.child(child_i)

    def type(self):
        return self.data(self.TYPE)

    @staticmethod
    def createFilterItem(name, full_name, description="", fn=None, params=collections.OrderedDict()):
        
        item = Item()

        item.name = name
        item.full_name = full_name
        item.description = description
        
        item.fn = fn
        if params: 
            try: 
                item.params = Item._initializeFilterParams(params)
            except ParameterError as e:
                print("Parameter error in item {}: ".format(name), e)
                item.params = collections.OrderedDict()
        else:
            item.params = collections.OrderedDict()

        item.params['modifier_coefficient'] = {
            'full_name': 'Modifier Coefficient',
            'wtype':'double_spinbox',
            'dtype': float,
            'description': 'Coefficient to use for this item if it is contained within a modifier',
            'optional': True,
            'value': 1.0,
            'default': 1.0,
            'minimum': -9999.0,
            'maximum': 9999.0,
            'single_step': 0.1,
            'decimals': 2}

        item.setData(Item.FILTER_TYPE, Item.TYPE)
        item.setData(Item._getIcon(item), QtCore.Qt.DecorationRole)
        item.setFlags(Item._getFlags(item))
        
        return item

    @staticmethod
    def createGroupItem():

        item = Item()

        item.name = 'group'
        item.full_name = 'Group'
        item.description = "Processes multiple items in sequence"

        item.params = collections.OrderedDict()

        item.params['modifier_coefficient'] = {
            'full_name': 'Modifier Coefficient',
            'wtype':'double_spinbox',
            'dtype': float,
            'description': 'Coefficient to use for this item if it is contained within a modifier',
            'optional': True,
            'value': 1.0,
            'default': 1.0,
            'minimum': -9999.0,
            'maximum': 9999.0,
            'single_step': 0.1,
            'decimals': 2}

        item.setData(Item.GROUP_TYPE, Item.TYPE)
        item.setData(Item._getIcon(item), QtCore.Qt.DecorationRole)
        item.setFlags(Item._getFlags(item))

        return item

    @staticmethod
    def createModifierItem():
        
        item = Item()

        item.name = 'modifier'
        item.full_name = 'Modifier'
        item.description = 'Processes multiple items individually and then combines their results'

        item.params = collections.OrderedDict({
            'mode': {
                'full_name': 'Modifier Mode',
                'wtype': 'combobox',
                'dtype': str,
                'description': "Determines whether children of modifier are added or multiplied",
                'optional': False,
                'value': 'add',
                'default': 'add',
                'options': ['add', 'multiply'],
                'options_description': ['Add components', 'Multiply components']},
            'clip': {
                'full_name': 'clip',
                'wtype': 'checkbox',
                'dtype': bool, 
                'description': "Clip result to maximum for given dtype, else range will be stretched to dtype range", 
                'optional': False,
                'default': True,
                'value': True},
            'modifier_coefficient': {
                'full_name': 'Modifier Coefficient',
                'wtype': 'double_spinbox',
                'dtype': float,
                'description': 'Coefficient to use for this item if it is contained within a modifier',
                'optional': True,
                'value': 1.0,
                'default': 1.0,
                'minimum': -9999.0,
                'maximum': 9999.0,
                'single_step': 0.1,
                'decimals': 2}})

        item.setData(Item.MODIFIER_TYPE, Item.TYPE) 
        item.setData(Item._getIcon(item), QtCore.Qt.DecorationRole)
        item.setFlags(Item._getFlags(item))

        return item

    @staticmethod
    def createInputItem(input_path=None):

        item = Item()
        
        item.name = 'input_item'
        item.full_name = 'Input Image'
        item.description = "The tree's input image. Cannot be moved!"

        item.params = collections.OrderedDict(
            {'input_path': {
                'full_name': 'Input Path',
                'wtype':'lineedit',
                'dtype': str,
                'description': "Path of the input image",
                'optional': False,
                'value': "",
                'default': "",
            },
            'modifier_coefficient': {
                'full_name': 'Modifier Coefficient',
                'wtype':'double_spinbox',
                'dtype': float,
                'description': 'Coefficient to use for this item if it is contained within a modifier',
                'optional': True,
                'value': 1.0,
                'default': 1.0,
                'minimum': -9999.0,
                'maximum': 9999.0,
                'single_step': 0.1,
                'decimals': 2}})

        item.setData(Item.INPUT_TYPE, Item.TYPE) 
        item.setData(Item._getIcon(item), QtCore.Qt.DecorationRole)
        item.setFlags(Item._getFlags(item))

        if input_path:
            item.updateParam('input_path',input_path)

        return item

    @staticmethod
    def _initializeFilterParams(params):
        
        if not params: 
            return collections.OrderedDict()
        else:
            params = collections.OrderedDict(params)

        for name, p in params.items():
            if not 'full_name' in p.keys(): p['full_name'] = name
            if not 'optional' in p.keys(): p['options'] = False
            if not 'description' in p.keys(): p['description'] = ""

            if not 'dtype' in p.keys(): raise ParameterError("No dtype provided for parameter {}".format(name))
            if not p['dtype'] in [float, int, str, bool]: raise ParameterError("Invalid dtype for paramter {}".format(name))

            if not 'wtype' in p.keys(): raise ParameterError("No wtype provided for parameter {}".format(name))
            if not p['wtype'] in ['lineedit', 'combobox', 'spinbox', 'double_spinbox', 'checkbox']: raise AttributeError("Invalid wtype for parameter {}".format(name))
        
            if p['wtype'] == 'spinbox':
                if p['dtype'] != int: raise ParameterError("dtype for wtype=spinbox must be int in parameter {}".format(name))
            elif p['wtype'] == 'double_spinbox':
                if p['dtype'] != float: raise ParameterError("dtype for wtype=double_spinbox must be float in parameter {}".format(name))

            if not 'default' in p.keys():
                if p['dtype'] == float:
                    p['default'] = 0.0
                elif p['dtype'] == int: 
                    p['default'] = 0
                elif p['dtype'] == str:
                    p['default'] = ""
                elif p['dtype'] == bool:
                    p['default'] = False
                
            if not type(p['default']) == p['dtype']: raise ParameterError("Type of default value doesn't match dtype in parameter {}".format(name))
            
            if p['wtype'] == 'spinbox' or p['wtype'] == 'double_spinbox':
                if 'minimum' in p.keys(): 
                    if type(p['minimum']) != p['dtype']: raise ParameterError("Type of spinbox minimum value doesn't match dtype in parameter {}".format(name))
                if 'maximum' in p.keys(): 
                    if type(p['maximum']) != p['dtype']: raise ParameterError("Type of spinbox maximum value doesn't match dtype in parameter {}".format(name))
                if 'single_step' in p.keys(): 
                    if type(p['single_step']) != p['dtype']: raise ParameterError("Type of spinbox single step value doesn't match dtype in parameter {}".format(name))
            
            if p['wtype'] == 'double_spinbox':
                if not 'decimals' in p.keys():
                    p['decimals'] = 2

            if p['wtype'] == 'combobox':
                if not 'options' in p.keys(): raise ParameterError("No options provided for wtype=combobox in parameter {}".format(name))
                if 'options_description' in p.keys():
                    if len(p['options']) != len(p['options_description']):
                        raise ParameterError("Length of options list doesn't match length of options_description in parameter {}".format(name))
            
            if not 'value' in p.keys(): 
                p['value'] = p['default']

        return params
    
    @staticmethod
    def _getIcon(item):

        if item.type() == item.FILTER_TYPE:
            return QtGui.QIcon('resources/filter.png')
        elif item.type() == item.MODIFIER_TYPE:
            return QtGui.QIcon('resources/modifier.png')
        elif item.type() == item.GROUP_TYPE:
            return QtGui.QIcon('resources/folder.png')
        elif item.type() == item.INPUT_TYPE:
            return QtGui.QIcon('resources/input.png')
        else:
            return QtGui.QIcon()

    @staticmethod
    def _getFlags(item):
        
        flags = QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled
        if item.type() == item.FILTER_TYPE:
            flags = flags|QtCore.Qt.ItemNeverHasChildren
        elif item.type() == item.GROUP_TYPE:
            flags = flags|QtCore.Qt.ItemIsDropEnabled|QtCore.Qt.ItemIsEditable
        elif item.type() == item.MODIFIER_TYPE:
            flags = flags|QtCore.Qt.ItemIsDropEnabled
        elif item.type() == item.INPUT_TYPE:
            flags &= ~(QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsUserCheckable)
        else: 
            return super().flags()

        return flags 


class ParameterError(Exception):
    pass
       
