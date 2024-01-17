import sys
import base64
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
from PyQt5.QtGui import QPixmap, QIcon, QImage
from PyQt5.QtCore import Qt
import fitz
from PIL import Image
from io import BytesIO

class Base64ConverterWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Base64 转换器')
        self.setWindowIcon(QIcon(r'C:\Users\12625\Documents\诸葛小戒工作夹\WorkSpace\test\adicon.ico'))  # 设置窗口图标

        window_width = 800  # 设置窗口初始宽度
        window_height = 600  # 设置窗口初始高度

        layout = QVBoxLayout()

        self.text_edit = QTextEdit()
        self.text_edit.setPlaceholderText("在这里输入Base64编码字符串")
        layout.addWidget(self.text_edit)

        self.content_label = QLabel()
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(self.content_label)
        layout.addWidget(scroll_area)

        self.save_button = QPushButton("保存")
        self.save_button.clicked.connect(self.save_file)  # 连接按钮和保存功能
        layout.addWidget(self.save_button)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.resize(window_width, window_height)  # 设置窗口大小

        self.text_edit.textChanged.connect(self.update_content)

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

    def update_content(self):
        base64_data = self.text_edit.toPlainText()
        try:
            data = base64.b64decode(base64_data)

            # Check if it's a valid image
            try:
                img = Image.open(BytesIO(data))
                img_format = img.format.lower()
                if img_format in ['jpeg', 'jpg', 'png']:
                    self.show_image(data)
                    self.save_button.setText("保存为 JPG")
                    return
            except Exception:
                pass

            # Check if it's a valid PDF
            try:
                doc = fitz.open(stream=data)
                self.show_pdf(data)
                self.save_button.setText("保存为 PDF")
                return
            except Exception as e:
                pass

            self.show_error_message("无法识别的格式:", "请输入有效的图片或 PDF 格式数据。")

        except Exception as e:
            self.show_error_message("解码失败:", str(e))

    def show_image(self, data):
        try:
            img = Image.open(BytesIO(data))
            pixmap = QPixmap()
            pixmap.loadFromData(data)
            self.content_label.setPixmap(pixmap)
            self.content_label.adjustSize()
        except Exception as e:
            self.show_error_message("图片显示失败:", str(e))

    def show_pdf(self, data):
        try:
            doc = fitz.open(stream=data)
            page = doc.load_page(0)
            pix = page.get_pixmap()
            img = QImage(pix.samples, pix.width, pix.height, pix.stride, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(img)
            self.content_label.setPixmap(pixmap)
            self.content_label.adjustSize()
        except Exception as e:
            self.show_error_message("PDF 显示失败:", str(e))

    def save_file(self):
        base64_data = self.text_edit.toPlainText()
        data = base64.b64decode(base64_data)

        try:
            # Check if it's a valid image
            try:
                img = Image.open(BytesIO(data))
                img_format = img.format.lower()
                if img_format in ['jpeg', 'jpg', 'png']:
                    img_path, _ = QFileDialog.getSaveFileName(self, "Save as Image", filter="Image Files (*.jpg *.jpeg *.png)")
                    if img_path:
                        img.save(img_path)
                        self.statusBar().showMessage("图片保存成功！", 3000)
                    return
            except Exception:
                pass

            # Check if it's a valid PDF
            try:
                doc = fitz.open(stream=data)
                pdf_path, _ = QFileDialog.getSaveFileName(self, "Save as PDF", filter="PDF Files (*.pdf)")
                if pdf_path:
                    with open(pdf_path, 'wb') as file:
                        file.write(data)
                    self.statusBar().showMessage("PDF 文件保存成功！", 3000)
                return
            except Exception as e:
                pass

            self.show_error_message("无法识别的格式:", "请输入有效的图片或 PDF 格式数据。")

        except Exception as e:
            self.show_error_message("保存失败:", str(e))

    def show_error_message(self, message, details=""):
        error_dialog = QMessageBox()
        error_dialog.setIcon(QMessageBox.Critical)
        error_dialog.setWindowTitle("错误")
        error_dialog.setText(message)
        error_dialog.setDetailedText(details)
        error_dialog.exec_()

def main():
    app = QApplication(sys.argv)
    window = Base64ConverterWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
