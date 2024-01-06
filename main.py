import sys
from PyQt5 import QtWidgets
from PyQt5.QtCore import QFile, QTextStream
from PyQt5.QtWidgets import QFileDialog
import design
from PyQt5.QtCore import QTextCodec
import syntax
import subprocess

path = ""

class ExampleApp(QtWidgets.QMainWindow, design.Ui_MainWindow):

    def __init__(self):

        super().__init__()

        self.setupUi(self)
        self.action.triggered.connect(self.save_file)
        self.action_2.triggered.connect(self.open_file)
        self.action_3.triggered.connect(self.examples)
        self.action_4.triggered.connect(self.run_script)

        highlighter = syntax.GoSyntaxHighlighter(self.textEdit)



    def new_file(self):
        self.textEdit.clear()
    def open_file(self):
        file, _ = QFileDialog.getOpenFileName(self, self.tr("Open File"), "",
                                                       "Go Files (*.go)")
        path = file
        path = path.replace("/","\\")
        print(path)
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
        path = fileName
        path = path.replace("/", "\\")
        if fileName:
            with open(fileName, 'w') as file:
                file.write(self.textEdit.toPlainText())

    def examples(self):

        file, _ = QFileDialog.getOpenFileName(self, self.tr("Open File"), "examples",
                                              "Go Files (*.go)")
        path = file
        path = path.replace("/", "\\")
        if file:
            in_file = QFile(file)
            if in_file.open(QFile.ReadOnly | QFile.Text):
                stream = QTextStream(in_file)
                self.textEdit.setPlainText(stream.readAll())


    def run_script(self):
        command = "go run D:/programming/go/netMg/netMg/cmd/server.go"
        print(command)

        process = subprocess.Popen(
            command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE
        )

        output, error = process.communicate()

        if error:
            print(output.decode('cp866'))
            self.lineEdit.setText("Ошибка сборки плагина")
        else:
            self.lineEdit.setText("Успешная сборка плагина!\n"+output.decode('cp866'))


def main():

    app = QtWidgets.QApplication(sys.argv)
    window = ExampleApp()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
