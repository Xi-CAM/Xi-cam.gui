from qtpy.QtCore import Signal, QPropertyAnimation, Qt, QParallelAnimationGroup, QAbstractAnimation
from qtpy.QtWidgets import QSplitter, QToolBar, QWidget, QFrame, QScrollArea, QToolButton, QGridLayout, QSizePolicy, \
    QLabel, QVBoxLayout, QFormLayout

class CollapsibleWidget(QWidget):

    toggled = Signal(bool)

    def __init__(self, widget: QWidget, name: str, parent=None):
        super(CollapsibleWidget, self).__init__(parent)
        layout = QVBoxLayout()
        self.widget = widget
        self.name = name
        layout.addWidget(QLabel(self.name))
        layout.addWidget(self.widget)
        self.collapsed = False
        self.setLayout(layout)

    def toggle(self):
        self.collapsed = not self.collapsed
        if self.collapsed:
            self.hide()
        else:
            self.show()
        self.toggled.emit(self.collapsed)


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
