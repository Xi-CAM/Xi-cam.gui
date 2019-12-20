from qtpy.QtCore import Signal, QPropertyAnimation, Qt, QParallelAnimationGroup, QAbstractAnimation
from qtpy.QtWidgets import QSplitter, QToolBar, QWidget, QFrame, QScrollArea, QToolButton, QGridLayout, QSizePolicy, \
    QLabel, QVBoxLayout, QFormLayout


# TODO: this could be more generic, defining a collapsible interface/mixin type class
class CollapsibleWidget(QWidget):
    """
    Creates a widget that can be collapsed when a button is clicked.
    """

    toggled = Signal(bool)

    def __init__(self, widget: QWidget, buttonText: str, parent=None):
        """
        Constructs a widget that lets the passed ``widget`` keep an internal collapsed state that can be triggered when
        a button is clicked.

        Internally, when the button is clicked, a toggled signal is emitted, indicating what the collapse state has
        been toggled to. Additionally, this signal is connected to the collapse() slot, which will collapse the passed
        widget if another widget has been added via addWidget(). The widget added via addWidget() is not collapsible.

        Parameters
        ----------
        widget
            The widget to make collapsible.
        buttonText
            The text of the button that will be used to collapse.
        parent
            The parent widget.
        """
        super(CollapsibleWidget, self).__init__(parent)
        self.widget = widget
        self.buttonText = buttonText
        self.collapsed = False

        toolBar = QToolBar()
        action = toolBar.addAction(self.buttonText, self.toggle)
        action.setIconText("&" + action.text())
        self.collapseButton = toolBar.widgetForAction(action)
        self.collapseButton.setCheckable(True)
        self.collapseButton.setChecked(not self.collapsed)

        self.splitter = QSplitter(Qt.Horizontal)
        self.splitter.addWidget(self.widget)
        self.splitter.setCollapsible(0, self.collapsed)
        # Keep track of the collapsed widget's size to restore properly when un-collapsed
        self.widgetSize = self.splitter.sizes()[0]

        layout = QGridLayout()
        layout.addWidget(self.splitter, 0, 0)
        layout.addWidget(toolBar, 1, 0)

        self.setLayout(layout)

        self.toggled.connect(self.collapse)

    def addWidget(self, widget):
        """
        Adds a non-collapsible widget to the internal splitter.

        Parameters
        ----------
        widget
            Non-collapsible widget to add.
        """
        # TODO -- what happens when more than one widget is added?
        self.splitter.addWidget(widget)
        self.splitter.setCollapsible(1, False)

    def toggle(self):
        self.collapsed = not self.collapsed
        self.toggled.emit(self.collapsed)

    def collapse(self, collapsed):
        self.collapseButton.setChecked(not collapsed)
        self.splitter.setCollapsible(0, collapsed)
        # Only do something for now if there is more than one widget added.
        if len(self.splitter.sizes()) > 1:
            if collapsed:
                self.widgetSize = self.splitter.sizes()[0]
                sizes = [0, self.splitter.sizes()[1]]
                self.splitter.setSizes(sizes)
            else:
                sizes = [self.widgetSize, self.splitter.sizes()[1] - self.widgetSize]
                self.splitter.setSizes(sizes)


class CollapsiblePanel(QWidget):
    def __init__(self, parent=None, title='', layout=None, animationDuration=100):
        """
        References:
            # Adapted from c++ version
            http://stackoverflow.com/questions/32476006/how-to-make-an-expandable-collapsable-section-widget-in-qt
        """
        super(CollapsiblePanel, self).__init__(parent=parent)

        self.animationDuration = animationDuration
        self.toggleAnimation = QParallelAnimationGroup()
        self.contentArea = QWidget()
        self.headerLine = QFrame()
        self.toggleButton = QToolButton()
        self.mainLayout = QGridLayout()

        toggleButton = self.toggleButton
        toggleButton.setStyleSheet("QToolButton { border: none; }")
        toggleButton.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        toggleButton.setArrowType(Qt.RightArrow)
        toggleButton.setText(str(title))
        toggleButton.setCheckable(True)
        toggleButton.setChecked(False)

        headerLine = self.headerLine
        headerLine.setFrameShape(QFrame.HLine)
        headerLine.setFrameShadow(QFrame.Sunken)
        headerLine.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)

        # self.contentArea.setStyleSheet("QScrollArea { background-color: white; border: none; }")
        self.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Fixed)
        self.contentArea.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Preferred)
        # start out collapsed
        self.contentArea.setMaximumHeight(0)
        self.contentArea.setMinimumHeight(0)
        # let the entire widget grow and shrink with its content
        toggleAnimation = self.toggleAnimation
        toggleAnimation.addAnimation(QPropertyAnimation(self, b"minimumHeight"))
        toggleAnimation.addAnimation(QPropertyAnimation(self, b"maximumHeight"))
        toggleAnimation.addAnimation(QPropertyAnimation(self.contentArea, b"minimumHeight"))
        toggleAnimation.addAnimation(QPropertyAnimation(self.contentArea, b"maximumHeight"))
        # don't waste space
        mainLayout = self.mainLayout
        mainLayout.setVerticalSpacing(0)
        mainLayout.setContentsMargins(0, 0, 0, 0)
        mainLayout.addWidget(self.toggleButton, 0, 0, 1, 1, Qt.AlignLeft)
        mainLayout.addWidget(self.headerLine, 0, 2, 1, 1, Qt.AlignVCenter)
        mainLayout.addWidget(self.contentArea, 1, 0, 1, 3)
        self.setLayout(self.mainLayout)

        # Initialize contentLayout
        self.content_layout = None
        self.setContentLayout(layout if layout is not None else QVBoxLayout())

        def start_animation(checked):
            collapsedHeight = self.sizeHint().height() - self.contentArea.maximumHeight()
            contentHeight = self.content_layout.sizeHint().height()
            for i in [0, 1]:
                spoilerAnimation = self.toggleAnimation.animationAt(i)
                spoilerAnimation.setDuration(self.animationDuration)
                spoilerAnimation.setStartValue(collapsedHeight)
                spoilerAnimation.setEndValue(collapsedHeight + contentHeight)
            for i in [2, 3]:
                contentAnimation = self.toggleAnimation.animationAt(i)
                contentAnimation.setDuration(self.animationDuration)
                contentAnimation.setStartValue(0)
                contentAnimation.setEndValue(contentHeight)

            arrow_type = Qt.DownArrow if checked else Qt.RightArrow
            direction = QAbstractAnimation.Forward if checked else QAbstractAnimation.Backward
            toggleButton.setArrowType(arrow_type)
            self.toggleAnimation.setDirection(direction)
            self.toggleAnimation.start()

        self.toggleButton.toggled.connect(start_animation)

    def setContentLayout(self, contentLayout):
        # Not sure if this is equivalent to self.contentArea.destroy()
        # self.contentArea.destroy()
        self.content_layout = contentLayout
        self.contentArea.setLayout(contentLayout)

    def addWidget(self, widget):
        self.content_layout.addWidget(widget)

    def addRow(self, *args, **kwargs):
        if not isinstance(self.contentArea.layout(), QFormLayout):
            raise AttributeError('The assigned layout is not QFormLayout, however .addRow was used')
        else:
            self.content_layout.addRow(*args, **kwargs)
