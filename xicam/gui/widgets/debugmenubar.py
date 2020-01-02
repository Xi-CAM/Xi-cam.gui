import sys

from qtpy.QtWidgets import QMenuBar, QShortcut, QMenu, QPushButton, QApplication, QWidget, QAction
from qtpy.QtGui import QKeySequence, QMouseEvent
from qtpy.QtCore import Qt, QObject, QEvent

import pickle

# Hack to work around PySide being imported from nowhere:
import qtpy

if "PySide.QtCore" in sys.modules and qtpy.API != "pyside":
    del sys.modules["PySide.QtCore"]

# from qtconsole.rich_jupyter_widget import RichJupyterWidget
# from qtconsole.inprocess import QtInProcessKernelManager

class EventPickleProxy():
    def __init__(self, event):
        self.event = event

    def pickleable(self):
        return bool(self.__reduce__())

    def __reduce__(self):
        if isinstance(self.event, QMouseEvent):
            return self.event.__class__, (self.event.localPos(), self.event.button(), self.event.buttons(), self.event.modifiers())


class EventRecorder(QObject):
    def __init__(self):
        super(EventRecorder, self).__init__()
        self.journal = []
        self._recording = False

    def eventFilter(self, obj, event):
        if not self._recording: return super(EventRecorder, self).eventFilter(obj, event)

        if event.type() in [] or True:
            print(event.type())
            self.journal.append(event)  # note: this breaks sender(), since obj can't be re-referenced across sessions

        if event.type() == QEvent.KeyPress and event.key() == Qt.Key_Escape:
            self.stop()

        return super(EventRecorder, self).eventFilter(obj, event)

    def start(self):
        self.journal.clear()
        self._recording = True

    def stop(self):
        self._recording = False
        pickle_proxies = [EventPickleProxy(event) for event in self.journal]
        events_for_export = [event for event in pickle_proxies if event.pickleable()]

        print(pickle.dumps(events_for_export))
        self.journal.clear()


class DebuggableMenuBar(QMenuBar):
    def __init__(self, *args, **kwargs):
        super(DebuggableMenuBar, self).__init__(*args, **kwargs)

        self.debugshortcut = QShortcut(QKeySequence("Ctrl+Return"), self, self.showDebugMenu, context=Qt.ApplicationShortcut)

        self.recorder = EventRecorder()
        QApplication.instance().installEventFilter(self.recorder)

        self._debugmenu = QMenu("Debugging")
        self._debugmenu.addAction("Debug widget", self.startDebugging)
        self._debugmenu.addAction("Record macro (ESC to finish)", self.recorder.start)



        self.mousedebugger = MouseDebugger()

    def showDebugMenu(self):
        self.addMenu(self._debugmenu)

    def startDebugging(self):
        QApplication.instance().installEventFilter(self.mousedebugger)


class MouseDebugger(QObject):
    def eventFilter(self, obj, event):
        # print(event,obj)
        # print(self.sender())
        if event.type() == QEvent.MouseButtonPress:
            print(QApplication.instance().activeWindow().childAt(event.pos()))
            IPythonDebugger(QApplication.instance().activeWindow().childAt(event.pos())).show()
            QApplication.instance().removeEventFilter(self)
            return True
        return False


# class IPythonDebugger(RichJupyterWidget):
#     def __init__(self, widget: QWidget):
#         super(IPythonDebugger, self).__init__()
#
#         # Setup the kernel
#         self.kernel_manager = QtInProcessKernelManager()
#         self.kernel_manager.start_kernel()
#         kernel = self.kernel_manager.kernel
#         kernel.gui = "qt"
#
#         # Push QWidget to the console
#         kernel.shell.push({"widget": widget})
#
#         self.kernel_client = self.kernel_manager.client()
#         self.kernel_client.start_channels()
#
#         # Setup console widget
#         def stop():
#             self.kernel_client.stop_channels()
#             self.kernel_manager.shutdown_kernel()
#
#         self.exit_requested.connect(stop)


if __name__ == "__main__":
    from qtpy.QtWidgets import QApplication, QMainWindow, QLabel

    app = QApplication([])
    window = QMainWindow()
    window.setCentralWidget(QLabel("test"))
    db = DebuggableMenuBar()
    window.setMenuBar(db)
    window.show()

    app.exec_()
