from pytestqt import qtbot
from xicam.core.execution.workflow import Workflow
from xicam.plugins.operationplugin import OperationPlugin, output_names
from xicam.gui.widgets.linearworkfloweditor import WorkflowEditor


def test_linearworkfloweditor():
    from qtpy.QtWidgets import QApplication

    app = QApplication([])

    @OperationPlugin
    @output_names('square')
    def square(a: int = 3) -> int:
        return a ** 2

    @OperationPlugin
    @output_names('sum')
    def my_sum(square: int, b: int = 3) -> int:
        return square + b

    wf = Workflow()

    wf.add_operation(square)
    wf.add_operation(my_sum)
    wf.auto_connect_all()

    we = WorkflowEditor(wf)

    we.show()

    app.exec_()
    # qtbot.waitSignal(we.destroyed, timeout=None)
