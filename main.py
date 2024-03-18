import sys
from modules.gui import DbApp
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DbApp()

    window.setWindowTitle("TBC Academy")
    window.setWindowIcon(QIcon("assets/tbcicon.png"))
    window.show()

    sys.exit(app.exec_())
