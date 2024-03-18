from modules.db import curs


class Employee(object):
    """CRUD operations for an employee"""

    def __init__(self, name, surname, age, primary_key=None):
        self.name = name
        self.surname = surname
        self.age = age
        self.id = primary_key

    @classmethod
    def get_one(cls, id_num):
        """Obtains one employee from the database based on ID"""
        result = curs.execute("SELECT * FROM employee WHERE id = ?", (id_num,))
        values = result.fetchone()
        if values is None:
            return None
        employee = Employee(values["name"], values["surname"], values["age"], values["id"])
        return employee

    @classmethod
    def get_list(cls, name=None, surname=None, age=None, id_num=None):
        """Obtains a list of employees from the database based on parameters"""
        params = [name, surname, age, id_num]
        if not any(item is not None for item in params):
            return None
        else:
            # Building a custom query depending op provided parameters
            query = 'SELECT * FROM employee WHERE '
            conditions = []  # Stores the conditions for the query
            query_params = []  # Stores the parameters for the query

            # Iterating on conditions and parameters to check which are not None and add them to the query
            for param, value in zip(("name", "surname", "age", "id"), params):
                if value:
                    conditions.append(f'{param} = ?')
                    query_params.append(value)

            query += " AND ".join(conditions)
            result = curs.execute(query, tuple(query_params))

            # Building a list of employees obtained from the database
            employees = []
            for row in result:
                employees.append(Employee(row['Id'], row['Name'], row['Surname'], row['Age']))

            return employees

    def __repr__(self):
        return f'[{self.name}, {self.surname}, {self.age}, {self.id}]'

    def __eq__(self, other):
        if self == other:
            return True
        return False

    def create(self):
        """Create a new employee in the database"""
        curs.execute("INSERT INTO employee (name, surname, age) VALUES (?, ?, ?)", (self.name, self.surname, self.age))
        self.id = curs.lastrowid

    @staticmethod
    def update(id_num, name=None, surname=None, age=None):
        """Update an employee in the database"""
        params = [name, surname, age]
        if not any(item is not None for item in params):
            return
        else:
            # Building a custom query depending on the provided parameters
            query = 'UPDATE employee SET '
            conditions = []
            query_params = []

            # Iterating on conditions and parameters to check which are not None and add them to the query
            for param, value in zip(("name", "surname", "age"), params):
                if value:
                    conditions.append(f'{param} = ?')
                    query_params.append(value)
            # Adding the ID to the query
            query_params.append(id_num)
            # Building the query
            query += ', '.join(conditions) + ' WHERE id = ?'

            curs.execute(query, tuple(query_params))

    def delete(self):
        """Delete an employee from the database"""
        if self.id:
            curs.execute("DELETE FROM employee WHERE id = ?", (self.id,))
            return self

    def save(self):
        """Saves an employee to the database or updates it if it already exists"""
        if not self.id:
            self.create()
        else:
            self.update(self.id, name=self.name, surname=self.surname, age=self.age)
        return self
