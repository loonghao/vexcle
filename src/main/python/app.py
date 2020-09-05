# Import built-in modules
import sys

# Import third-party modules
from fbs_runtime.application_context.PySide2 import ApplicationContext

# Import local modules
from vexcle import Controller
from vexcle import Model
from vexcle import View


class VexcleApplicationContext(ApplicationContext):

    def run(self):
        model = Model(self)
        ctrl = Controller(model, self._gui, self)
        ctrl.show()
        exit_code = self.app.exec_()
        sys.exit(exit_code)

    def __init__(self):
        super(VexcleApplicationContext, self).__init__()
        self._gui = View()


if __name__ == '__main__':
    app = VexcleApplicationContext()
    app.run()
