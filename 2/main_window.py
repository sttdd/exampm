from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, \
    QPushButton, QLineEdit, QComboBox, QLabel, QFormLayout, QDialog
from PySide6.QtGui import QIcon
from sqlalchemy.orm import Session
from user_class import Employee, Position, Company

class MainWindow(QMainWindow):
    def __init__(self, session: Session):
        super().__init__()
        self.session = session
        self.setWindowTitle("Управление сотрудниками")
        self.setWindowIcon(QIcon('logo.png'))
        self.init_ui()
        self.populate_table()
        self.populate_f()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        self.table = QTableWidget()
        self.table.setColumnCount(9)
        self.table.setHorizontalHeaderLabels(["ID","ИМЯ","ФАМИЛИЯ","СЕРИЯ","НОМЕР","АДРЕС","ДАТА","ДОЛЖНОСТЬ","КОМПАНИЯ"])
        main_layout.addWidget(self.table)

        filter_layout = QHBoxLayout()
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Поиск по имени...")
        self.name_input.textChanged.connect(self.filter_table)

        self.surname_input = QLineEdit()
        self.surname_input.setPlaceholderText("Поиск по фамилии...")
        self.surname_input.textChanged.connect(self.filter_table)

        self.position_input = QComboBox()
        self.position_input.addItem("ВСЕ ДОЛЖНОСТИ")
        self.position_input.currentTextChanged.connect(self.filter_table)

        self.company_input = QComboBox()
        self.company_input.addItem("ВСЕ КОМПАНИИ")
        self.company_input.currentTextChanged.connect(self.filter_table)

        filter_layout.addWidget(QLabel("ПОИСК:"))
        filter_layout.addWidget(self.name_input)
        filter_layout.addWidget(QLabel("ПОИСК:"))
        filter_layout.addWidget(self.surname_input)
        filter_layout.addWidget(QLabel("ДОЛЖНОСТЬ:"))
        filter_layout.addWidget(self.position_input)
        filter_layout.addWidget(QLabel("КОМПАНИЯ:"))
        filter_layout.addWidget(self.company_input)
        main_layout.addLayout(filter_layout)

        button_layout = QHBoxLayout()
        add_button = QPushButton("Добавить сотрудника")
        delete_button = QPushButton("Удалить сотрудника")
        add_button.clicked.connect(self.open_add_dialog)
        delete_button.clicked.connect(self.delete_employee)
        button_layout.addWidget(add_button)
        button_layout.addWidget(delete_button)
        main_layout.addLayout(button_layout)

    def populate_table(self):
        employees = self.session.query(Employee).all()
        self.table.setRowCount(len(employees))
        for row, employee in enumerate(employees):
            self.table.setItem(row, 0, QTableWidgetItem(str(employee.id)))
            self.table.setItem(row, 1, QTableWidgetItem(employee.name))
            self.table.setItem(row, 2, QTableWidgetItem(employee.surname))
            self.table.setItem(row, 3, QTableWidgetItem(str(employee.s_pasport)))
            self.table.setItem(row, 4, QTableWidgetItem(str(employee.n_pasport)))
            self.table.setItem(row, 5, QTableWidgetItem(employee.adres))
            self.table.setItem(row, 6, QTableWidgetItem(str(employee.data_nach)))
            self.table.setItem(row, 7, QTableWidgetItem(employee.position.title))
            self.table.setItem(row, 8, QTableWidgetItem(employee.company.name))

    def filter_table(self):
        name_text = self.name_input.text().lower()
        surname_text = self.surname_input.text().lower()
        position_text = self.position_input.currentText()
        company_text = self.company_input.currentText()

        query = self.session.query(Employee)
        if name_text:
            query = query.filter(Employee.name.ilike(f"%{name_text}%"))
        if surname_text:
            query = query.filter(Employee.surname.ilike(f"%{surname_text}%"))
        if position_text != "ВСЕ ДОЛЖНОСТИ":
            query = query.join(Position).filter(Position.title == position_text)
        if company_text != "ВСЕ КОМПАНИИ":
            query = query.join(Company).filter(Company.name == company_text)

        employees = query.all()
        self.table.setRowCount(len(employees))
        for row, employee in enumerate(employees):
            self.table.setItem(row, 0, QTableWidgetItem(str(employee.id)))
            self.table.setItem(row, 1, QTableWidgetItem(employee.name))
            self.table.setItem(row, 2, QTableWidgetItem(employee.surname))
            self.table.setItem(row, 3, QTableWidgetItem(str(employee.s_pasport)))
            self.table.setItem(row, 4, QTableWidgetItem(str(employee.n_pasport)))
            self.table.setItem(row, 5, QTableWidgetItem(employee.adres))
            self.table.setItem(row, 6, QTableWidgetItem(str(employee.data_nach)))
            self.table.setItem(row, 7, QTableWidgetItem(employee.position.title))
            self.table.setItem(row, 8, QTableWidgetItem(employee.company.name))

    def populate_f(self):
        positions = self.session.query(Position).all()
        companies = self.session.query(Company).all()

        self.position_input.clear()
        self.company_input.clear()

        self.position_input.addItem("ВСЕ ДОЛЖНОСТИ")
        self.company_input.addItem("ВСЕ КОМПАНИИ")

        self.position_input.addItems([pos.title for pos in positions])
        self.company_input.addItems([comp.name for comp in companies])

    def delete_employee(self):
        selected = self.table.currentRow()
        if selected >= 0:
            employee_id = int(self.table.item(selected, 0).text())
            employee = self.session.query(Employee).filter_by(id=employee_id).first()
            if employee:
                self.session.delete(employee)
                self.session.commit()
                self.populate_table()

    def open_add_dialog(self):
        dialog = AddEmployee(self.session, self)
        if dialog.exec():
            self.populate_table()
            self.populate_f()

class AddEmployee(QDialog):
    def __init__(self, session: Session, parent=None):
        super().__init__(parent)
        self.session = session
        self.setWindowTitle("Добавление сотрудника")
        self.s_ui()

    def s_ui(self):
        layout = QFormLayout(self)
        self.name_input = QLineEdit()
        self.surname_input = QLineEdit()
        self.n_pasport = QLineEdit()
        self.s_pasport = QLineEdit()
        self.adres = QLineEdit()
        self.data_nach = QLineEdit()
        self.position_combo = QComboBox()
        self.company_combo = QComboBox()

        positions = self.session.query(Position).all()
        companies = self.session.query(Company).all()
        self.position_combo.addItems([pos.title for pos in positions])
        self.company_combo.addItems([comp.name for comp in companies])

        layout.addRow("имя",self.name_input)
        layout.addRow("фам", self.surname_input)
        layout.addRow("номер", self.n_pasport)
        layout.addRow("серия", self.s_pasport)
        layout.addRow("адрес", self.adres)
        layout.addRow("дата начала", self.data_nach)
        layout.addRow("Должность", self.position_combo)
        layout.addRow("Компания", self.company_combo)

        buttons = QHBoxLayout()
        add_button = QPushButton("ДОБАВИТЬ")
        cancel_button = QPushButton("ОТМЕНА")
        add_button.clicked.connect(self.add_employee)
        cancel_button.clicked.connect(self.reject)
        buttons.addWidget(add_button)
        buttons.addWidget(cancel_button)
        layout.addRow(buttons)

    def add_employee(self):
        name = self.name_input.text()
        surname = self.surname_input.text()
        n_pasport = self.n_pasport.text()
        s_pasport = self.s_pasport.text()
        adres = self.adres.text()
        data_nach = self.data_nach.text()
        position_title = self.position_combo.currentText()
        company_name = self.company_combo.currentText()

        if not all([name, surname, n_pasport, s_pasport, adres, data_nach, position_title, company_name]):
            print("Заполните все поля!")
            return

        position = self.session.query(Position).filter_by(title=position_title).first()
        company = self.session.query(Company).filter_by(name=company_name).first()

        if position and company:
            employee = Employee(
                name=name,
                surname=surname,
                n_pasport=int(n_pasport),
                s_pasport=int(s_pasport),
                adres=adres,
                data_nach=data_nach,
                position=position,
                company=company
            )
            self.session.add(employee)
            self.session.commit()
            self.accept()