from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Arcaea Search Interface")

        quit = QPushButton("Exit")
        quit.pressed.connect(self.close)

        self.setCentralWidget(quit)
        self.show()

app = QApplication([])
window = MainWindow()
app.exec()