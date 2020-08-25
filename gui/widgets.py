
import numpy as np 

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.uic import loadUiType
from pyqtgraph import ImageView, TextItem, InfiniteLine, SignalProxy

from tree.items import Item
from tree.delegates import PreProcessedDelegate, PostProcessedDelegate

Ui_Form_Parameters, QWidget_parameters = loadUiType('gui/widget_parameters.ui')


class ParametersWidget(QWidget_parameters, Ui_Form_Parameters, QtCore.QObject):

    value_changed_signal = QtCore.pyqtSignal()

    def __init__(self, item):
        super().__init__()
        self.setupUi(self)
        self.layout = self.lay_parameters
        self.item = item
        if item: 
            params = item.params
            self.populateWidget(params)
            self.pb_reset.clicked.connect(self.reset)
        else: 
            self.pb_reset.setVisible(False)

    def populateWidget(self, params):
        self.input_elements = {}
        if not params: return

        for name, p in params.items():
            ie = _InputElement(name, p, self)
            ie.value_changed_signal[str, object].connect(lambda name, value: self.item.updateParam(name, value))
            ie.value_changed_signal.connect(lambda: self.value_changed_signal.emit())
            label, editor = ie.getInputElements()
            self.input_elements[name] = ie
            self.layout.addRow(label, editor)

    def reset(self):
        for ie in self.input_elements.values():
            ie.reset()


class _InputElement(QtCore.QObject): 

    value_changed_signal = QtCore.pyqtSignal(str,object)

    def __init__(self, name, param, parent):
        super().__init__()
        self.name = name
        self.parent = parent
        self.param = param 
        p = self.param

        #Create label
        self.label = QtWidgets.QLabel(p['full_name'], parent=self.parent)

        #Create appropriate editor
        if p['wtype'] == 'lineedit':
            editor = QtWidgets.QLineEdit(parent=self.parent)
            if p['dtype'] == float:
                validator = QtGui.QDoubleValidator(parent=editor)
            elif p['dtype'] == int:
                validator = QtGui.QIntValidator(parent=editor)
            else: 
                validator = None
            if validator: editor.setValidator(validator)
            editor.setText(str(p['value']))
            editor.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
            editor.editingFinished.connect(self.valueChanged)

        elif p['wtype'] == 'combobox':
            editor = QtWidgets.QComboBox(parent=self.parent)
            editor.addItems(p['options'])
            for i in range(len(p['options'])):
                editor.setItemData(i, p['options_description'][i], QtCore.Qt.ToolTipRole)
            editor.setCurrentIndex(editor.findText(p['value']))
            editor.currentTextChanged.connect(self.valueChanged)

        elif p['wtype'] == 'spinbox' or p['wtype'] == 'double_spinbox':
            if p['wtype'] == 'spinbox': 
                editor = QtWidgets.QSpinBox(parent=self.parent)
            elif p['wtype'] == 'double_spinbox':
                editor = QtWidgets.QDoubleSpinBox(parent=self.parent)
                if 'decimals' in p.keys(): editor.setDecimals(p['decimals'])
            if 'minimum' in p.keys(): editor.setMinimum(p['minimum'])
            if 'maximum' in p.keys(): editor.setMaximum(p['maximum'])
            if 'single_step' in p.keys(): editor.setSingleStep(p['single_step'])
            editor.setValue(p['value'])
            editor.valueChanged.connect(self.valueChanged)

        elif p['wtype'] == 'checkbox':
            editor = QtWidgets.QCheckBox(parent=self.parent)
            editor.setChecked(p['value'])
            editor.stateChanged.connect(self.valueChanged)

        editor.setToolTip(p['description'])
        self.editor = editor

    def valueChanged(self):
        p = self.param

        if p['wtype'] == 'lineedit':
            value = p['dtype'](self.editor.text())
        elif p['wtype'] == 'combobox':
            value = self.editor.currentText()
        elif p['wtype'] == 'spinbox' or p['wtype'] == 'double_spinbox':
            value = p['dtype'](self.editor.value())
        elif p['wtype'] == 'checkbox':
            value = self.editor.isChecked()

        self.value_changed_signal.emit(self.name, value)

    def getInputElements(self):
        return (self.label, self.editor)

    def reset(self):
        p = self.param

        if p['wtype'] == 'lineedit':
            self.editor.setText(str(p['default'])) 
        elif p['wtype'] == 'combobox':
            self.editor.setCurrentIndex(self.editor.findText(p['default']))    
        elif p['wtype'] == 'spinbox' or p['wtype'] == 'double_spinbox':
            self.editor.setValue(p['default'])
        elif p['wtype'] == 'checkbox':
            self.editor.setChecked(p['default'])
        
        self.valueChanged()
        self.editor.repaint()


class PreProcessedTree(QtWidgets.QTreeView):
    def __init__(self, main_window, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.main_window = main_window
    
        self.setDragEnabled(True)
        self.setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)
        self.setDefaultDropAction(QtCore.Qt.MoveAction)
        self.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectItems)
        self.setHeaderHidden(True)

        #self.installEventFilter(_TreeEventFilter())
        #self.viewport().installEventFilter(_TreeEventFilter())

        self.setItemDelegate(PreProcessedDelegate())

    def dropEvent(self, event):
        drop_pos = self.dropIndicatorPosition()

        if drop_pos == QtWidgets.QAbstractItemView.OnViewport:
            return

        at_index = self.indexAt(event.pos())
        at_item = self.model().itemFromIndex(at_index)
        if not at_item:
            return
        
        if at_item.type() == Item.INPUT_TYPE and (drop_pos == self.AboveItem or drop_pos == self.OnItem):
            return

        sel_index = self.selectedIndexes()[0]
        sel_item = self.model().itemFromIndex(sel_index)
        
        next_item, _ = self.model().getNext(sel_item, exit_modifier=True)
        clone_item = sel_item.clone()

        if drop_pos == QtWidgets.QAbstractItemView.OnItem:
            if at_item.type() == Item.GROUP_TYPE or at_item.type() == Item.MODIFIER_TYPE:
                at_item.appendRow(clone_item)
            else:
                return 
        else:
            parent = at_item.parent()
            if not parent:
                parent = self.model().invisibleRootItem()
            at_row = at_item.row()

            if drop_pos == QtWidgets.QAbstractItemView.AboveItem:
                parent.insertRow(at_row, clone_item)
            elif drop_pos == QtWidgets.QAbstractItemView.BelowItem:
                parent.insertRow(at_row+1, clone_item)

        self.model().removeItem(sel_item, no_prompts=True)

        emit_items = [clone_item, next_item]
        self.main_window.signals.items_moved.emit(emit_items)
        
        return

    def eventFilter(self, source, event): 
        print("event filter called!")
        return super().eventFilter(source, event)

    # def eventFilter(self, source, event):
    #     if ((source is self.tree_pre and
    #          event.type() == QtCore.QEvent.KeyPress and
    #          event.key() == QtCore.Qt.Key_Escape and
    #          event.modifiers() == QtCore.Qt.NoModifier) or
    #         (source is self.tree_pre.viewport() and
    #          event.type() == QtCore.QEvent.MouseButtonPress and
    #          not self.tree_pre.indexAt(event.pos()).isValid())):
    #         self.tree_pre.selectionModel().clear()
    #         self.displayParametersWidget(None)
    #     return super().eventFilter(source, event)

class _TreeEventFilter(QtCore.QObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def eventFilter(self, source, event):
        print("source", source)
        
        return super().eventFilter(source, event)

class PostProcessedTree(QtWidgets.QTreeView):
    def __init__(self, main_window, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.main_window = main_window
        self.main_window.signals.items_moved.connect(self.repaint)
        
        self.setDragDropMode(QtWidgets.QAbstractItemView.NoDragDrop)
        self.setDefaultDropAction(QtCore.Qt.IgnoreAction)
        self.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.setHeaderHidden(True)
        self.setIndentation(20)
        self.setDragEnabled(False)

        self.setItemDelegate(PostProcessedDelegate())

    def selectionCommand(self, index, event):
        # if not index.data(Item.IS_PROCESSED):
        #     return QtCore.QItemSelectionModel.NoUpdate
        return super().selectionCommand(index, event)


class ImagePropertiesView(QtWidgets.QTextBrowser):
    def __init__(self, main_window, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.setMinimumHeight(78)
        self.setMaximumHeight(78)
    def setImageProperties(self, minimum=None, maximum=None, dtype=None, resolution=None):
        if minimum is None:
            minimum = ""
        else:
            if type(minimum) == np.uint8:
                minimum = "{}".format(minimum)
            elif type(minimum) == np.float64:
                minimum = "{:.3f}".format(minimum)
            else:
                minimum = str(minimum)
        
        if maximum is None:
            maximum = ""
        else:
            if type(maximum) == np.uint8:
                maximum = "{}".format(maximum)
            elif type(maximum) == np.float64:
                maximum = "{:.3f}".format(maximum)
            else:
                maximum = str(maximum)

        if dtype is None:
            dtype = ""
        else:
            dtype = str(dtype)
        
        if resolution is None:
            resolution = ""
        else:
            if type(resolution) == tuple:
                if len(resolution) == 2:
                    resolution = (resolution[1], resolution[0])
                elif len(resolution) == 3:
                    resolution = (resolution[1], resolution[0], resolution[2])
            
            resolution = str(resolution)

        self.setPlainText("Min value: {}\nMax value: {}\nDtype: {}\nResolution: {}".format(minimum, maximum, dtype, resolution))


class FilteratorImageViewSignals(QtCore.QObject):
    mouse_pos_updated = QtCore.pyqtSignal(tuple)


class FilteratorImageView(ImageView):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.ui.histogram.hide()
        self.ui.roiBtn.hide()
        self.ui.menuBtn.hide()

        self.image_view_text = TextItem(text="", color=(255,0,0), anchor=(0,0))
        self.getView().addItem(self.image_view_text)

        self.image_view_vline = InfiniteLine(angle=90, movable=False)
        self.image_view_hline = InfiniteLine(angle=0, movable=False)
        self.getView().addItem(self.image_view_vline, ignoreBounds=True)
        self.getView().addItem(self.image_view_hline, ignoreBounds=True)

        self.image_view_proxy = SignalProxy(self.getView().scene().sigMouseMoved, rateLimit=60, slot=self.onMouseMoved)

        self.signals = FilteratorImageViewSignals()

    def setProcessed(self, status=True):
        if status == True:
            self.image_view_text.setText("")
        else:
            self.image_view_text.setText("Not processed!",color=(255,0,0))

    def onMouseMoved(self, event):
        pos = event[0]
        item = self.getImageItem()
        viewbox = self.getView()

        if item.sceneBoundingRect().contains(pos):
            mouse_point = viewbox.mapSceneToView(pos)
            self.image_view_vline.setPos(mouse_point.x())
            self.image_view_hline.setPos(mouse_point.y())
            self.signals.mouse_pos_updated.emit((mouse_point.x(), mouse_point.y()))