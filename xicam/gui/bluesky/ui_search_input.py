# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_search_input.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_SearchInputWidget(object):
    def setupUi(self, SearchInputWidget):
        SearchInputWidget.setObjectName("SearchInputWidget")
        SearchInputWidget.resize(389, 368)
        self.gridLayout_4 = QtWidgets.QGridLayout(SearchInputWidget)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.search_input_layout = QtWidgets.QVBoxLayout()
        self.search_input_layout.setObjectName("search_input_layout")
        self.default_period_layout = QtWidgets.QGridLayout()
        self.default_period_layout.setObjectName("default_period_layout")
        self.all_widget = QtWidgets.QRadioButton(SearchInputWidget)
        self.all_widget.setObjectName("all_widget")
        self.default_period_layout.addWidget(self.all_widget, 0, 0, 1, 1)
        self.days_widget = QtWidgets.QRadioButton(SearchInputWidget)
        self.days_widget.setObjectName("days_widget")
        self.default_period_layout.addWidget(self.days_widget, 0, 1, 1, 1)
        self.today_widget = QtWidgets.QRadioButton(SearchInputWidget)
        self.today_widget.setObjectName("today_widget")
        self.default_period_layout.addWidget(self.today_widget, 1, 0, 1, 1)
        self.hour_widget = QtWidgets.QRadioButton(SearchInputWidget)
        self.hour_widget.setObjectName("hour_widget")
        self.default_period_layout.addWidget(self.hour_widget, 1, 1, 1, 1)
        self.search_input_layout.addLayout(self.default_period_layout)
        self.since_until_layout = QtWidgets.QGridLayout()
        self.since_until_layout.setObjectName("since_until_layout")
        self.since_label = QtWidgets.QLabel(SearchInputWidget)
        self.since_label.setObjectName("since_label")
        self.since_until_layout.addWidget(self.since_label, 0, 0, 1, 1)
        self.since_widget = QtWidgets.QDateTimeEdit(SearchInputWidget)
        self.since_widget.setMinimumDateTime(QtCore.QDateTime(QtCore.QDate(1752, 9, 14), QtCore.QTime(0, 0, 0)))
        self.since_widget.setCalendarPopup(True)
        self.since_widget.setObjectName("since_widget")
        self.since_until_layout.addWidget(self.since_widget, 0, 1, 1, 1)
        self.until_label = QtWidgets.QLabel(SearchInputWidget)
        self.until_label.setObjectName("until_label")
        self.since_until_layout.addWidget(self.until_label, 1, 0, 1, 1)
        self.until_widget = QtWidgets.QDateTimeEdit(SearchInputWidget)
        self.until_widget.setCalendarPopup(True)
        self.until_widget.setObjectName("until_widget")
        self.since_until_layout.addWidget(self.until_widget, 1, 1, 1, 1)
        self.search_input_layout.addLayout(self.since_until_layout)
        self.search_bar_layout = QtWidgets.QHBoxLayout()
        self.search_bar_layout.setObjectName("search_bar_layout")
        self.custom_query_label = QtWidgets.QLabel(SearchInputWidget)
        self.custom_query_label.setObjectName("custom_query_label")
        self.search_bar_layout.addWidget(self.custom_query_label)
        self.search_bar = QtWidgets.QLineEdit(SearchInputWidget)
        self.search_bar.setObjectName("search_bar")
        self.search_bar_layout.addWidget(self.search_bar)
        self.mongo_query_help_button = QtWidgets.QPushButton(SearchInputWidget)
        self.mongo_query_help_button.setObjectName("mongo_query_help_button")
        self.search_bar_layout.addWidget(self.mongo_query_help_button)
        self.search_input_layout.addLayout(self.search_bar_layout)
        self.gridLayout_4.addLayout(self.search_input_layout, 0, 0, 1, 1)

        self.retranslateUi(SearchInputWidget)
        QtCore.QMetaObject.connectSlotsByName(SearchInputWidget)

    def retranslateUi(self, SearchInputWidget):
        _translate = QtCore.QCoreApplication.translate
        SearchInputWidget.setWindowTitle(_translate("SearchInputWidget", "Form"))
        self.all_widget.setText(_translate("SearchInputWidget", "All"))
        self.days_widget.setText(_translate("SearchInputWidget", "30 Days"))
        self.today_widget.setText(_translate("SearchInputWidget", "Today"))
        self.hour_widget.setText(_translate("SearchInputWidget", "Last Hour"))
        self.since_label.setText(_translate("SearchInputWidget", "Since:"))
        self.until_label.setText(_translate("SearchInputWidget", "Until:"))
        self.custom_query_label.setText(_translate("SearchInputWidget", "Custom Query:"))
        self.mongo_query_help_button.setText(_translate("SearchInputWidget", "?"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    SearchInputWidget = QtWidgets.QWidget()
    ui = Ui_SearchInputWidget()
    ui.setupUi(SearchInputWidget)
    SearchInputWidget.show()
    sys.exit(app.exec_())

