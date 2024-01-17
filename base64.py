import base64
import sys
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QTextEdit,
    QVBoxLayout,
    QWidget,
    QLabel,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QFileDialog,
)
from PyQt5.QtGui import QPixmap, QPainter, QIcon
from PyQt5.QtPrintSupport import QPrinter
from PyQt5.QtCore import Qt

class Base64ImageWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Base64 图片解码器')
        self.setWindowIcon(QIcon(r'C:\Users\12625\Downloads\图片1.ico'))  # 设置窗口图标

        window_width = 800  # 设置窗口初始宽度
        window_height = 600  # 设置窗口初始高度

        layout = QVBoxLayout()

        self.text_edit = QTextEdit()
        self.text_edit.setPlaceholderText("在这里输入Base64编码字符串")
        layout.addWidget(self.text_edit)

        self.image_label = QLabel()
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(self.image_label)
        layout.addWidget(scroll_area)

        self.save_pdf_button = QPushButton("保存为PDF")
        self.save_pdf_button.clicked.connect(self.save_as_pdf)  # 连接按钮和保存为PDF的功能
        layout.addWidget(self.save_pdf_button)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.resize(window_width, window_height)  # 设置窗口大小

        self.text_edit.textChanged.connect(self.update_image)

        self.set_styles()  # 应用现代化样式

    def set_styles(self):
        style = """
            QMainWindow {
                background-color: #f0f0f0;
                border: 1px solid #d4d4d4;
            }
            QPushButton {
                background-color: #4CAF50;
                border: none;
                color: white;
                padding: 10px 20px;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                font-size: 16px;
                margin: 4px 2px;
                transition-duration: 0.4s;
                cursor: pointer;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QTextEdit {
                border: 1px solid #d4d4d4;
                padding: 10px;
                font-size: 14px;
            }
            QLabel {
                border: 1px solid #d4d4d4;
                padding: 10px;
            }
        """
        self.setStyleSheet(style)

    def update_image(self):
        base64_data = self.text_edit.toPlainText()
        try:
            img_data = base64.b64decode(base64_data)
            pixmap = QPixmap()
            pixmap.loadFromData(img_data)
            self.image_label.setPixmap(pixmap)
            self.image_label.adjustSize()
        except Exception as e:
            self.show_error_message("解码失败:", str(e))

    def save_as_pdf(self):
        try:
            file_dialog = QFileDialog()
            file_path, _ = file_dialog.getSaveFileName(self, "Save as PDF", filter="PDF Files (*.pdf)")
            if file_path:
                printer = QPrinter(QPrinter.HighResolution)
                printer.setOutputFormat(QPrinter.PdfFormat)
                printer.setOutputFileName(file_path)
                painter = QPainter(printer)
                painter.setRenderHint(QPainter.Antialiasing)
                pixmap = self.image_label.pixmap()
                if pixmap:
                    printer_page_size = printer.pageRect().size()
                    pixmap_scaled = pixmap.scaled(printer_page_size, aspectRatioMode=Qt.KeepAspectRatio)
                    painter.drawPixmap(int((printer_page_size.width() - pixmap_scaled.width()) / 2),
                                       int((printer_page_size.height() - pixmap_scaled.height()) / 2),
                                       pixmap_scaled)
                painter.end()
        except Exception as e:
            self.show_error_message("保存 PDF 时出错:", str(e))

    def show_error_message(self, message, details=""):
        error_dialog = QMessageBox()
        error_dialog.setIcon(QMessageBox.Critical)
        error_dialog.setWindowTitle("错误")
        error_dialog.setText(message)
        error_dialog.setDetailedText(details)
        error_dialog.exec_()

def main():
    app = QApplication(sys.argv)
    window = Base64ImageWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()