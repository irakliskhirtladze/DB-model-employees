from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem
from PyQt5.uic import loadUi
from modules.employee import Employee
from modules.db import conn


class DbApp(QMainWindow):
    """GUI class responsible for connecting GUI elements with database functionality
    and handling the app behaviour"""
    def __init__(self) -> None:
        """Initialize UI and connect buttons with methods"""
        super().__init__()
        self.ui = loadUi("ui/employee.ui", self)

        self.ui.pushButton.clicked.connect(self.add_employee)
        self.ui.pushButton_2.clicked.connect(self.search_employee)
        self.ui.pushButton_3.clicked.connect(self.update_employee)
        self.ui.pushButton_4.clicked.connect(self.delete_employee)

    def add_employee(self):
        """Add a new employee to the database"""
        name = self.ui.lineEdit.text()
        surname = self.ui.lineEdit_2.text()
        age_raw = self.ui.lineEdit_3.text()

        if age_raw.isdigit() and "" not in (name, surname):
            age = int(age_raw)
            employee = Employee(name, surname, age)
            employee.save()
            conn.commit()
            self.ui.label_4.setStyleSheet("color: green")
            self.ui.label_4.setText(f"An employee was created successfully. ID = {employee.id}")

        elif "" in (name, surname):
            self.ui.label_4.setStyleSheet("color: red")
            self.ui.label_4.setText("Both Name and Surname are required")

        elif age_raw == "":
            self.ui.label_4.setStyleSheet("color: red")
            self.ui.label_4.setText("Please enter valid age")

    def search_employee(self):
        """Search employee in the database based on the provided parameters
        and display the results in a table"""
        name = self.ui.lineEdit_5.text()
        surname = self.ui.lineEdit_6.text()
        age_raw = self.ui.lineEdit_7.text()
        age = int(age_raw) if age_raw.isdigit() else None
        id_raw = self.ui.lineEdit_8.text()
        id_num = int(id_raw) if id_raw.isdigit() else None

        employee_list = Employee.get_list(name=name, surname=surname, age=age, id_num=id_num)
        # Column names to be set on the app table
        column_names = ['ID', 'Name', 'Surname', 'Age']
        # Setting the table rows and columns
        self.ui.tableWidget.setRowCount(len(employee_list))
        self.ui.tableWidget.setColumnCount(len(column_names))
        self.ui.tableWidget.setHorizontalHeaderLabels(column_names)
        # Populating the table with employee data
        for row_idx, employee in enumerate(employee_list):
            for col_idx, value in enumerate([employee.name, employee.surname, employee.age, employee.id]):
                item = QTableWidgetItem(str(value))
                self.ui.tableWidget.setItem(row_idx, col_idx, item)

    def update_employee(self):
        """Update an employee in the database based on the provided parameters"""
        self.ui.label_16.setText('')
        # Read input to use them as search parameters
        name = self.ui.lineEdit_4.text()
        surname = self.ui.lineEdit_10.text()
        age = self.ui.lineEdit_11.text()
        id_num = self.ui.lineEdit_9.text()
        # Handle input errors and update employee in the database
        if id_num.isdigit() and any(item != '' for item in (name, surname, age)):
            id_num = int(id_num)
            if age != '':
                if age.isdigit():
                    age = int(age)
                else:
                    self.ui.label_16.setStyleSheet("color: red")
                    self.ui.label_16.setText('Age must be a number')
                    return None
                
            employee = Employee(name, surname, age, id_num)
            # Check if record with provided ID exists
            if employee.get_one(id_num):
                employee.save()
                conn.commit()
                self.ui.label_16.setStyleSheet("color: green")
                self.ui.label_16.setText('Successfully updated')
            else:
                self.ui.label_16.setStyleSheet("color: red")
                self.ui.label_16.setText('No such ID found in database')

        elif id == '' or not id_num.isdigit():
            self.ui.label_16.setStyleSheet("color: red")
            self.ui.label_16.setText('ID must be a number')

        elif all(item == '' for item in (name, surname, age)):
            self.ui.label_16.setStyleSheet("color: red")
            self.ui.label_16.setText('Enter at least one parameter to update')

        else:
            self.ui.label_16.setStyleSheet("color: red")
            self.ui.label_16.setText('An error occurred')

    def delete_employee(self):
        """Delete an employee from the database"""
        id_num = self.ui.lineEdit_9.text()
        # Handle input errors and delete employee from the database
        if id_num.isdigit():
            id_num = int(id_num)
            employee = Employee.get_one(id_num)
            if employee:  # Check if record with provided ID exists
                employee.delete()
                conn.commit()
                self.ui.label_16.setStyleSheet("color: green")
                self.ui.label_16.setText(f'Employee with ID = {id_num} was deleted')
            else:
                self.ui.label_16.setStyleSheet("color: red")
                self.ui.label_16.setText('No such ID found in database')

        else:
            self.ui.label_16.setStyleSheet("color: red")
            self.ui.label_16.setText('ID must be an integer to delete')
