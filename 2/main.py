from PySide6.QtWidgets import QApplication
from user_class import Connect
from main_window import MainWindow


app = QApplication([])
session = Connect.create_connection()
window = MainWindow(session)
window.show()
app.exec()
