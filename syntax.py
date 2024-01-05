from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit

from PyQt5.QtGui import QTextCharFormat, QColor, QFont, QSyntaxHighlighter
from PyQt5.QtCore import Qt, QRegExp

import sys


class GoSyntaxHighlighter(QSyntaxHighlighter):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.highlighting_rules = []

        # Ключевые слова Golang
        keyword_format = QTextCharFormat()
        keyword_format.setForeground(Qt.cyan)
        keywords = ['break', 'default', 'func', 'interface', 'select',
                    'case', 'defer', 'go', 'map', 'struct',
                    'chan', 'else', 'goto', 'package', 'switch',
                    'const', 'fallthrough', 'if', 'range', 'type',
                    'continue', 'for', 'import', 'return', 'var']
        data_format = QTextCharFormat()
        data_format.setForeground(Qt.darkRed)

        datatypes = ['string', 'int', 'int64', 'bool', 'uint64',
                     'byte', 'rune', 'float32', 'float64',
                     'uint8', 'complex64', 'type', 'nil',
                     'err']

        for keyword in keywords:
            pattern = QRegExp(r'\b' + keyword + r'\b')
            rule = (pattern, keyword_format)
            self.highlighting_rules.append(rule)

        for data in datatypes:
            pattern = QRegExp(r'\b' + data + r'\b')
            rule = (pattern, data_format)
            self.highlighting_rules.append(rule)

        # Комментарии
        comment_format = QTextCharFormat()
        comment_format.setForeground(Qt.green)
        self.highlighting_rules.append((QRegExp(r'//.*'), comment_format))
        # vars

        var_format = QTextCharFormat()
        var_format.setForeground(Qt.magenta)
        self.highlighting_rules.append((QRegExp(r'var*'),var_format))

        func_format = QTextCharFormat()
        func_format.setForeground(Qt.yellow)
        self.highlighting_rules.append((QRegExp(r'func*'), func_format))

    def highlightBlock(self, text):
        for rule in self.highlighting_rules:
            pattern = rule[0]
            format = rule[1]
            expression = QRegExp(pattern)
            index = expression.indexIn(text)

            while index >= 0:
                length = expression.matchedLength()
                self.setFormat(index, length, format)
                index = expression.indexIn(text, index + length)

        self.setCurrentBlockState(0)

