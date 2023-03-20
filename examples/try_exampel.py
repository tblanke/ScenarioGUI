from PySide6 import QtCore, QtGui, QtWidgets

class Widget(QtWidgets.QLineEdit):
    def __init__(self, parent=None):
        super(Widget, self).__init__(parent)
        lay = QtWidgets.QVBoxLayout(self)
        for i in range(5):
            btn = QtWidgets.QPushButton(
                'button {}'.format(i),
                clicked=self.on_clicked
            )
            lay.addWidget(btn)

    #@QtCore.Qt.pyqtSlot()
    def on_clicked(self):
        btn = self.sender()
        ix = self.layout().indexOf(btn)
        new_btn = QtWidgets.QPushButton(
            "button {}".format(self.layout().count()),
            clicked=self.on_clicked
        )
        self.layout().insertWidget(ix+1, new_btn)

if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication.instance()
    if app is None:
        app = QtWidgets.QApplication(sys.argv)
    w = Widget()
    w.show()
    sys.exit(app.exec())