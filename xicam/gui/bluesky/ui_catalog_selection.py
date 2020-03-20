# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/catalog_selection.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_CatalogSelectionWidget(object):
    def setupUi(self, CatalogSelectionWidget):
        CatalogSelectionWidget.setObjectName("CatalogSelectionWidget")
        CatalogSelectionWidget.resize(225, 50)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(CatalogSelectionWidget)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.Catalog = QtWidgets.QLabel(CatalogSelectionWidget)
        self.Catalog.setObjectName("Catalog")
        self.horizontalLayout.addWidget(self.Catalog)
        self.catalog_list = QtWidgets.QComboBox(CatalogSelectionWidget)
        self.catalog_list.setObjectName("catalog_list")
        self.horizontalLayout.addWidget(self.catalog_list)
        self.horizontalLayout_2.addLayout(self.horizontalLayout)

        self.retranslateUi(CatalogSelectionWidget)
        QtCore.QMetaObject.connectSlotsByName(CatalogSelectionWidget)

    def retranslateUi(self, CatalogSelectionWidget):
        _translate = QtCore.QCoreApplication.translate
        CatalogSelectionWidget.setWindowTitle(_translate("CatalogSelectionWidget", "Form"))
        self.Catalog.setText(_translate("CatalogSelectionWidget", "Select Calalog:"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    CatalogSelectionWidget = QtWidgets.QWidget()
    ui = Ui_CatalogSelectionWidget()
    ui.setupUi(CatalogSelectionWidget)
    CatalogSelectionWidget.show()
    sys.exit(app.exec_())

