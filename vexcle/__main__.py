# Import built-in modules
import sys

# Import third-party modules
from PySide6.QtWidgets import QApplication

# Import local modules
from vexcle import Controller
from vexcle import Model
from vexcle import View
from vexcle import context


if __name__ == "__main__":
    app = QApplication(sys.argv)
    context = context.Context(app)
    gui = View()
    model = Model(context)
    ctrl = Controller(model, gui, context)
    ctrl.show()
    sys.exit(app.exec())
