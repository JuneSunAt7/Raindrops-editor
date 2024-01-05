import sys
from PyQt5 import QtWidgets
from pathlib import Path
from PyQt5.QtCore import QFile, QTextStream
from PyQt5.QtWidgets import QFileDialog
import design
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QTextCodec
import syntax


class ExampleApp(QtWidgets.QMainWindow, design.Ui_MainWindow):

    def __init__(self):

        super().__init__()

        self.setupUi(self)
        self.action.triggered.connect(self.save_file)
        self.action_2.triggered.connect(self.open_file)
        self.action_3.triggered.connect(self.examples)

        highlighter = syntax.GoSyntaxHighlighter(self.textEdit)
        codec = QTextCodec.codecForName("Windows-1251")

        QTextCodec.setCodecForLocale(codec)


    def new_file(self):
        self.textEdit.clear()
    def open_file(self):
        file, _ = QFileDialog.getOpenFileName(self, self.tr("Open File"), "",
                                                       "Go Files (*.go)")

        if file:
            in_file = QFile(file)
            if in_file.open(QFile.ReadOnly | QFile.Text):
                stream = QTextStream(in_file)
                self.textEdit.setPlainText(stream.readAll())

    def save_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self, "Save File", "", "Go Files (*.go);",
                                                  options=options)
        if fileName:
            with open(fileName, 'w') as file:
                file.write(self.textEdit.toPlainText())

    def examples(self):

        file, _ = QFileDialog.getOpenFileName(self, self.tr("Open File"), "examples",
                                              "Go Files (*.go)")

        if file:
            in_file = QFile(file)
            if in_file.open(QFile.ReadOnly | QFile.Text):
                stream = QTextStream(in_file)
                self.textEdit.setPlainText(stream.readAll())

def main():

    app = QtWidgets.QApplication(sys.argv)
    window = ExampleApp()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
