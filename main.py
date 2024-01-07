import sys
from PyQt5 import QtWidgets
from PyQt5.QtCore import QFile, QTextStream
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtGui import QColor, QPalette
import design
from PyQt5.QtCore import QTextCodec
import syntax
import subprocess


class ExampleApp(QtWidgets.QMainWindow, design.Ui_MainWindow):

    def __init__(self):

        super().__init__()

        self.setupUi(self)
        self.action.triggered.connect(self.save_file)
        self.action_2.triggered.connect(self.open_file)
        self.action_3.triggered.connect(self.examples)
        self.action_4.triggered.connect(self.run_script)

        highlighter = syntax.GoSyntaxHighlighter(self.textEdit)
        self.file_path = None


    def new_file(self):
        self.save_file()
        self.textEdit.clear()
    def open_file(self):
        file, _ = QFileDialog.getOpenFileName(self, self.tr("Open File"), "",
                                                       "Go Files (*.go)")

        self.file_path = file.replace("/","\\")

        if file:
            in_file = QFile(file)
            if in_file.open(QFile.ReadOnly | QFile.Text):
                stream = QTextStream(in_file)
                stream.setCodec("UTF-8")
                self.textEdit.setPlainText(stream.readAll())

    def save_file(self):


        fileName, _ = QFileDialog.getSaveFileName(self, "Save File", "", "Go Files (*.go);",
                                                  )
        self.file_path = fileName.replace("/", "\\")
        if fileName:
            with open(fileName, 'w', encoding="utf-8") as file:
                file.write(self.textEdit.toPlainText())

    def examples(self):

        file, _ = QFileDialog.getOpenFileName(self, self.tr("Open File"), "examples",
                                              "Go Files (*.go)")
        self.file_path = file.replace("/","\\")
        if file:
            in_file = QFile(file)
            if in_file.open(QFile.ReadOnly | QFile.Text):
                stream = QTextStream(in_file)
                self.textEdit.setPlainText(stream.readAll())


    def run_script(self):
        self.save_file()
        command = "go build " + self.file_path
        print(command)

        process = subprocess.Popen(
            command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE
        )

        output, error = process.communicate()

        if error:
            print(error)
            palette = QPalette()
            palette.setColor(QPalette.Text, QColor(255, 179, 179))
            self.lineEdit.setPalette(palette)
            self.lineEdit.setText(error.decode())
        else:
            palette = QPalette()
            palette.setColor(QPalette.Text, QColor(179, 255, 179))
            self.lineEdit.setPalette(palette)
            self.lineEdit.setText("Успешная сборка плагина!\n"+output.decode('cp866'))


def main():

    app = QtWidgets.QApplication(sys.argv)
    window = ExampleApp()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
