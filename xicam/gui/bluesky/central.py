"""
Provides a central widget that contains much of what the blueskybrowser.
Might go away eventually, but needed to prevent the CentralWdiget from
trying to setup a menu.
"""

import time

from .search import SearchWidget, SearchState
from xicam.gui.bluesky.summary import SummaryWidget

from qtpy.QtCore import QDateTime, Qt
from qtpy.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QSplitter)


class CentralWidget(QWidget):
    """
    Encapsulates all widgets and models. Connect signals on __init__.
    """
    def __init__(self, *args,
                 catalog, menuBar,
                 zmq_address=None, **kwargs):
        super().__init__(*args, **kwargs)

        # Define models.
        search_state = SearchState(
            catalog=catalog)
        self.search_model = search_state.search_results_model
        # Define widgets.
        self.search_widget = SearchWidget()
        self.summary_widget = SummaryWidget()

        left_pane = QSplitter(Qt.Vertical)
        left_pane.addWidget(self.search_widget)
        left_pane.addWidget(self.summary_widget)

        layout = QHBoxLayout()
        splitter = QSplitter(Qt.Horizontal)
        layout.addWidget(splitter)
        splitter.addWidget(left_pane)

        self.setLayout(layout)

        def show_double_clicked_entry(index):
            search_state.search_results_model.emit_open_entries(None, [index])

        # Set models, connect signals, and set initial values.
        now = time.time()
        ONE_HOUR = 60 * 60
        TODAY = ONE_HOUR * 24
        ONE_WEEK = TODAY * 7
        ONE_MONTH = TODAY * 30 #used for 30 days QRadioButton

        def set_timerange(timerange):
            search_state.search_results_model.on_select_range(timerange)
            self.search_widget.search_input_widget.since_widget.setDateTime(
            QDateTime.fromSecsSinceEpoch(now - timerange))
            self.search_widget.search_input_widget.until_widget.setDateTime(
            QDateTime.fromSecsSinceEpoch(now))

        def on_select_today():
            set_timerange(TODAY)

        def on_select_lasthour():
            set_timerange(ONE_HOUR)

        def on_select_30days():
            set_timerange(ONE_MONTH)

        def on_select_all():
            search_state.search_results_model.on_select_all()
            self.search_widget.search_input_widget.since_widget.setDateTime(
            QDateTime.fromSecsSinceEpoch(0))
            self.search_widget.search_input_widget.until_widget.setDateTime(
            QDateTime.fromSecsSinceEpoch(now))

        # connect QRadioButtons and change date dropdowns (since/until widgets) accordingly
        self.search_widget.search_input_widget.today_widget.clicked.connect(
            on_select_today)
        self.search_widget.search_input_widget.hour_widget.clicked.connect(
            on_select_lasthour)
        self.search_widget.search_input_widget.days_widget.clicked.connect(
            on_select_30days)
        self.search_widget.search_input_widget.all_widget.clicked.connect(
            on_select_all)
        # connect input since/until widgets
        self.search_widget.search_input_widget.until_widget.dateTimeChanged.connect(
            search_state.search_results_model.on_until_time_changed)
        self.search_widget.search_input_widget.until_widget.setDateTime(
            QDateTime.fromSecsSinceEpoch(now))
        self.search_widget.search_input_widget.since_widget.dateTimeChanged.connect(
            search_state.search_results_model.on_since_time_changed)
        self.search_widget.search_input_widget.since_widget.setDateTime(
            QDateTime.fromSecsSinceEpoch(now - ONE_WEEK))
        # connect catalog_list dropdown
        self.search_widget.catalog_selection_widget.catalog_list.setModel(
            search_state.catalog_selection_model)
        self.search_widget.catalog_selection_widget.catalog_list.currentIndexChanged.connect(
            search_state.set_selected_catalog)

        self.search_widget.search_input_widget.search_bar.textChanged.connect(
            search_state.search_results_model.on_search_text_changed)
            
        self.search_widget.search_results_widget.setModel(
            search_state.search_results_model)
        self.search_widget.search_results_widget.selectionModel().selectionChanged.connect(
            search_state.search_results_model.emit_selected_result)
        self.search_widget.search_results_widget.doubleClicked.connect(
            show_double_clicked_entry)
        search_state.search_results_model.selected_result.connect(
            self.summary_widget.set_entries)
        search_state.search_results_model.valid_custom_query.connect(
            self.search_widget.search_input_widget.mark_custom_query)
        search_state.sig_update_header.connect(
            self.search_widget.search_results_widget.hide_hidden_columns)
        search_state.enabled = True
        search_state.search()



