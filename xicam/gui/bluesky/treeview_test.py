# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/treeview_test.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from qtpy.QtGui import QStandardItemModel, QStandardItem

data = [
    ("Alice", [
        ("Keys", []),
        ("Purse", [
            ("Cellphone", [])
            ])
        ]),
    ("Bob", [
        ("Wallet", [
            ("Credit card", []),
            ("Money", [])
            ])
        ])
    ]


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(600, 371)
        self.horizontalLayout = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout.setObjectName("horizontalLayout")
        # self.treeWidget = QtWidgets.QTreeWidget(Form)
        # self.treeWidget.setObjectName("treeWidget")
        # item_0 = QtWidgets.QTreeWidgetItem(self.treeWidget)
        # item_1 = QtWidgets.QTreeWidgetItem(item_0)
        # item_2 = QtWidgets.QTreeWidgetItem(item_1)
        # item_2 = QtWidgets.QTreeWidgetItem(item_1)
        # item_1 = QtWidgets.QTreeWidgetItem(item_0)
        # item_2 = QtWidgets.QTreeWidgetItem(item_1)
        # item_2 = QtWidgets.QTreeWidgetItem(item_1)
        # item_0 = QtWidgets.QTreeWidgetItem(self.treeWidget)
        # item_1 = QtWidgets.QTreeWidgetItem(item_0)
        # item_1 = QtWidgets.QTreeWidgetItem(item_0)
        # item_2 = QtWidgets.QTreeWidgetItem(item_1)
        # item_2 = QtWidgets.QTreeWidgetItem(item_1)
        # item_0 = QtWidgets.QTreeWidgetItem(self.treeWidget)
        # self.horizontalLayout.addWidget(self.treeWidget)
        
        self.treeView = QtWidgets.QTreeView(Form)
        self.treeView.setObjectName("treeView")
        self.horizontalLayout.addWidget(self.treeView)

        self.model = QStandardItemModel()
        self.treeView.addItems(self.model, data)
        self.treeView.setModel(self.model)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        # self.treeWidget.headerItem().setText(0, _translate("Form", "Scan ID"))
        # self.treeWidget.headerItem().setText(1, _translate("Form", "Energy"))
        # self.treeWidget.headerItem().setText(2, _translate("Form", "Temp"))
        # self.treeWidget.headerItem().setText(3, _translate("Form", "Pressure"))
        # __sortingEnabled = self.treeWidget.isSortingEnabled()
        # self.treeWidget.setSortingEnabled(False)
        # self.treeWidget.topLevelItem(0).setText(0, _translate("Form", "Scan 1"))
        # self.treeWidget.topLevelItem(0).setText(1, _translate("Form", "12 keV"))
        # self.treeWidget.topLevelItem(0).setText(2, _translate("Form", "0K"))
        # self.treeWidget.topLevelItem(0).setText(3, _translate("Form", "1000bar"))
        # self.treeWidget.topLevelItem(0).child(0).setText(0, _translate("Form", "Analysis Settings"))
        # self.treeWidget.topLevelItem(0).child(0).setText(1, _translate("Form", "Calibrant"))
        # self.treeWidget.topLevelItem(0).child(0).setText(2, _translate("Form", "FIt Model"))
        # self.treeWidget.topLevelItem(0).child(0).child(0).setText(0, _translate("Form", "Setting 1.A"))
        # self.treeWidget.topLevelItem(0).child(0).child(1).setText(0, _translate("Form", "Setting 1.B"))
        # self.treeWidget.topLevelItem(0).child(1).setText(0, _translate("Form", "ROIs"))
        # self.treeWidget.topLevelItem(0).child(1).child(0).setText(0, _translate("Form", "ROI 1.1"))
        # self.treeWidget.topLevelItem(0).child(1).child(1).setText(0, _translate("Form", "ROI"))
        # self.treeWidget.topLevelItem(1).setText(0, _translate("Form", "Scan 2"))
        # self.treeWidget.topLevelItem(1).setText(1, _translate("Form", "11.9 keV"))
        # self.treeWidget.topLevelItem(1).setText(2, _translate("Form", "0K"))
        # self.treeWidget.topLevelItem(1).setText(3, _translate("Form", "1000bar"))
        # self.treeWidget.topLevelItem(1).child(0).setText(0, _translate("Form", "Analysis Settings"))
        # self.treeWidget.topLevelItem(1).child(1).setText(0, _translate("Form", "ROIs"))
        # self.treeWidget.topLevelItem(1).child(1).child(0).setText(0, _translate("Form", "ROI 2.1"))
        # self.treeWidget.topLevelItem(1).child(1).child(1).setText(0, _translate("Form", "ROI 2.2"))
        # self.treeWidget.topLevelItem(2).setText(0, _translate("Form", "Scan 3"))
        # self.treeWidget.setSortingEnabled(__sortingEnabled)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

