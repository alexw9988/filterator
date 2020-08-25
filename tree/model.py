
import logging
import collections

from PyQt5 import QtCore, QtGui, QtWidgets

from tree.items import Item
from filters.defaults import DEFAULTS


class TreeModel(QtGui.QStandardItemModel): 
    INSERT_SUCCESSFUL = 0
    INSERT_FAILED = 1

    REMOVE_SUCCESFUL = INSERT_SUCCESSFUL
    REMOVE_FAILED = INSERT_FAILED

    LOAD_SUCCESSFUL = INSERT_SUCCESSFUL
    LOAD_EXCEPTION = 2 
    LOAD_FAILED = INSERT_FAILED
    
    def __init__(self, app, tree_dict=None):
        super().__init__()

        self.app = app
        if tree_dict: 
            self.loadTree(tree_dict)
        self.setItemPrototype(Item())

    @property
    def input_item(self):
        if self.invisibleRootItem().hasChildren():
            child = self.invisibleRootItem().child(0)
            if child.type() == Item.INPUT_TYPE:
                return child 
        
        return None

    @input_item.setter
    def input_item(self, value):
        if self.hasInputItem():
            self.invisibleRootItem().setChild(0, value)
        else: 
            self.insertRow(0, value)

    def hasInputItem(self):
        return (self.input_item is None) == False

    def loadTree(self, tree_list):
        logging.debug("Loading tree from list")

        self.clear()

        parent = self.invisibleRootItem()
        branch = tree_list
        had_exception = False

        try:
            had_exception = self._loadBranch(parent, branch, had_exception)
            if not self.hasInputItem():
                input_item = Item.createInputItem()
                self.insertRow(0, input_item)
                logging.warning("Imported JSON tree structure did not have input file. Input item was therefore added.")
                had_exception = True

        except Exception as e:
            logging.error("Error loading tree: {}".format(repr(e)))
            self.clear()
            return self.LOAD_FAILED

        else:
            if had_exception: 
                logging.warning("Loaded tree with at least one exception.")
                return self.LOAD_EXCEPTION
            else: 
                logging.info("Tree succesfully loaded")
                return self.LOAD_SUCCESSFUL

    def _loadBranch(self, parent, branch, had_exception):
        
        for item in branch:
            had_exception = self._loadItem(parent, item, had_exception)

        return had_exception 

    def _loadItem(self, parent, item, had_exception):

        try:
            if item['type'] == Item.FILTER_TYPE:
                name = item['name']
                full_name = DEFAULTS[name]['full_name']
                fn = DEFAULTS[name]['fn']
                description = DEFAULTS[name]['description']
                default_params = DEFAULTS[name]['default_params']
                new_item = Item.createFilterItem(name, full_name, description=description,fn=fn,params=default_params)
            elif item['type'] == Item.GROUP_TYPE:
                new_item = Item.createGroupItem()
            elif item['type'] == Item.MODIFIER_TYPE:
                new_item = Item.createModifierItem()
            elif item['type'] == Item.INPUT_TYPE:
                new_item = Item.createInputItem()

            new_item.setParamValueDict(item['param_values'])
            new_item.is_active = item['is_active']

        except Exception as e:
            logging.error("Unable to load an item: {}".format(repr(e)))
            had_exception = True
            
        else:
            logging.debug("Loaded item {}".format(new_item.full_name))
            parent.appendRow(new_item)

            if item['type'] == Item.GROUP_TYPE or item['type'] == Item.MODIFIER_TYPE:
                self._loadBranch(new_item, item['child_list'], had_exception)
        
        return had_exception

    def saveTree(self):
        branch = self.invisibleRootItem()
        tree_list = self._saveBranch(branch)

        logging.debug("Tree saved to dict")
        
        return tree_list

    def _saveBranch(self, branch): 
        branch_list = []
        child_count = branch.rowCount()

        for child_i in range(child_count):
            child = branch.child(child_i)
            branch_list.append(self._saveItem(child))
        
        return branch_list

    def _saveItem(self, item):
        data = {'type': item.type(),
                'name': item.name,
                'param_values': item.getParamValueDict(),
                'is_active': item.is_active}
                
        if item.type() == Item.FILTER_TYPE or item.type() == Item.INPUT_TYPE:
            return data
        elif item.type() == Item.GROUP_TYPE or item.type() == Item.MODIFIER_TYPE:
            data['child_list'] = self._saveBranch(item)
            return data
        else:
            return {}

    def getItemRank(self, item):
        rank = 0
        for item in self.iterateTree(item, exit_modifier=True):
            rank += 1 

        return rank

    def insertItem(self, item, insert_at=None):

        if item.type() == Item.INPUT_TYPE: 
            if self.hasInputItem(): 
                logging.debug("Can't insert input_item when there already is one.")
                return self.INSERT_FAILED
            else:
                logging.debug("Adding input_item as first item")
                self.appendRow(item)
                return self.INSERT_SUCCESSFUL
        else:
            if not self.hasInputItem():
                logging.debug("Can't insert item when there is no input item")
                return self.INSERT_FAILED

        if not insert_at:
            logging.debug("Adding item to end of tree")
            self.appendRow(item)
            return self.INSERT_SUCCESSFUL

        if insert_at.type() == Item.GROUP_TYPE or insert_at.type() == Item.MODIFIER_TYPE:
            logging.debug("Adding item to end of group/modifier")
            insert_at.appendRow(item)
        else:
            parent = insert_at.parent()
            if not parent:
                parent = self.invisibleRootItem()
            row = insert_at.row()
            logging.debug("Adding item after selected filter in row {}".format(row))
            parent.insertRow(row+1, item)
            
        return self.INSERT_SUCCESSFUL

    def removeItem(self, item, no_prompts=False):
        
        if item.type() == Item.INPUT_TYPE and self.rowCount() > 1: 
            if no_prompts:
                reply = QtWidgets.QMessageBox.Yes
            else:
                reply = QtWidgets.QMessageBox.question(self.app.main_window, 'Delete Item', 
                    'Deleting the input item will delete the entire tree. Continue?', QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No)
            if reply == QtWidgets.QMessageBox.No: 
                logging.debug("Input item was not removed along with entire tree")
                return (None, self.REMOVE_FAILED)
            else:
                self.clear()
                return (None, self.REMOVE_SUCCESFUL)

        if item.hasChildren():
            if no_prompts:
                reply = QtWidgets.QMessageBox.Yes
            else:
                reply = QtWidgets.QMessageBox.question(self.app.main_window, 'Delete Item', 
                        'Deleting this item will also delete all its children. Continue?', QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No)
            if reply == QtWidgets.QMessageBox.No: 
                logging.debug("Group/Modifier item was not removed along with all its children")
                return (None, self.REMOVE_FAILED)

        parent = item.parent()
        if not parent: 
            parent = self.invisibleRootItem() 
            parent_is_root = True  
        else:
            parent_is_root = False

        row = item.row()
        parent.removeRow(row)
        logging.debug("Removed item")
        
        sel_item = parent.child(row)
        if not sel_item: #item was last 
            sel_item = parent.child(row-1)
            if not sel_item: #item was also first (i.e. only item)
                if parent_is_root:
                    sel_item = None
                else:
                    sel_item = parent
        
        return (sel_item, self.REMOVE_SUCCESFUL)

    def iterateTree(self, item, exit_modifier=True, yield_none=False, ignore_active_status=False):
        
        if item is None: 
            return None
        
        while item: 
            yield item
            item, exit_modifier = self.getNext(item, exit_modifier=exit_modifier, 
                                    ignore_active_status=ignore_active_status)
        
        if yield_none:
            yield None

    def getNext(self, item, exit_modifier=False, ignore_active_status=False):

        if item is None:
            return (None, exit_modifier)
              
        row = item.row()

        parent = item.parent()
        parent_is_root = False
        if parent is None:
            parent = self.invisibleRootItem()
            parent_is_root = True
        elif exit_modifier and parent.type() == Item.MODIFIER_TYPE:
            exit_modifier = False
            return (parent, exit_modifier)

        if row == parent.rowCount()-1:
            if parent_is_root:
                return (None, exit_modifier)
            else:
                if parent.is_active:
                    return (parent, exit_modifier)
                else:
                    next_item, exit_modifier = self.getNext(parent, exit_modifier=exit_modifier)
                    return (next_item, exit_modifier)

        next_item = parent.child(row+1)
        while next_item.hasChildren():
            next_item = next_item.child(0)

        if next_item.is_active or ignore_active_status:
            return (next_item, exit_modifier)
        else:
            return self.getNext(next_item,exit_modifier=exit_modifier)
            
    def getPrev(self, item, ignore_active_status=False):
        
        if item is None: 
            return None

        it = item.type()
        if it == Item.INPUT_TYPE or it == Item.GROUP_TYPE or it == Item.MODIFIER_TYPE:
            return None

        curr_item = item
        parent = item.parent()
        while True:
            if parent is None or parent.type() == Item.GROUP_TYPE:
                row = curr_item.row()
                if row > 0:
                    break
            
            curr_item = parent
            parent = curr_item.parent()
            
        if parent is None: 
            parent = self.invisibleRootItem()

        prev_item = parent.child(row-1)
        if prev_item.is_active or ignore_active_status:
            return prev_item
        else:
            return self.getPrev(prev_item)
