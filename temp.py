def update(id, name=None, surname=None, age=None):
        params = [name, surname, age]
        if not any(item is not None for item in params):
            return None
        else:
            query  = "UPDATE employee SET "
            conditions = []
            query_params = []

            for param, value in zip(("name", "surname", "age"), params):
                if value:
                    conditions.append(f'{param} = ?')
                    query_params.append(value)
            query_params.append(id)
            query += ", ".join(conditions)
            query += ' WHERE id = ?'
            

            print(query, tuple(query_params))
        

print(update(1, name='gia', surname='asdad', age=34))





# UPDATE employee SET name = ?, surname = ?, age = ? WHERE id = ?, (self.name, self.surname, self.age, self.id)
# UPDATE employee SET name = ?, surname = ?, age = ? WHERE id = ? ('gia', 'asdad', 34, 1)