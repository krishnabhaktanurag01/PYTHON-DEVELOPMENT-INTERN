import csv

class Employee:
    def __init__(self, name, position, salary):
        self.name = name
        self.position = position
        self.salary = salary

    def display_info(self):
        print(f"Name: {self.name}, Position: {self.position}, Salary: {self.salary}")

    def to_dict(self):
        return {'Name': self.name, 'Position': self.position, 'Salary': self.salary}


class EmployeeManagementSystem:
    def __init__(self, filename='employee_records.csv'):
        self.filename = filename
        self.employee_records = {}
        self.load_records()

    def load_records(self):
        try:
            with open(self.filename, mode='r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    employee = Employee(row['Name'], row['Position'], float(row['Salary']))
                    self.employee_records[employee.name] = employee
        except FileNotFoundError:
            # File doesn't exist, initialize an empty records dictionary
            self.employee_records = {}

    def save_records(self):
        with open(self.filename, mode='w', newline='') as file:
            fieldnames = ['Name', 'Position', 'Salary']
            writer = csv.DictWriter(file, fieldnames=fieldnames)

            writer.writeheader()
            for employee in self.employee_records.values():
                writer.writerow(employee.to_dict())

    def add_employee(self, employee):
        if not isinstance(employee, Employee):
            raise ValueError("Invalid employee object.")
        if employee.name in self.employee_records:
            print(f"Employee with name {employee.name} already exists.")
        else:
            self.employee_records[employee.name] = employee
            print(f"{employee.name} has been added to the records.")
            self.save_records()

    def remove_employee(self, name):
        if name in self.employee_records:
            del self.employee_records[name]
            print(f"{name} has been removed from the records.")
            self.save_records()
        else:
            print(f"Employee with name {name} not found.")

    def update_employee(self, name, new_position=None, new_salary=None):
        if name in self.employee_records:
            employee = self.employee_records[name]
            if new_position:
                employee.position = new_position
            if new_salary:
                employee.salary = new_salary
            print(f"{name}'s information has been updated.")
            self.save_records()
        else:
            print(f"Employee with name {name} not found.")

    def display_all_employees(self):
        if not self.employee_records:
            print("No employee records found.")
        else:
            print("Employee Records:")
            for employee in self.employee_records.values():
                employee.display_info()
                print("--------------------")



employee1 = Employee("John Doe", "Developer", 60000)
employee2 = Employee("Jane Smith", "Manager", 80000)

ems = EmployeeManagementSystem()
ems.add_employee(employee1)
ems.add_employee(employee2)

ems.display_all_employees()

ems.update_employee("John Doe", new_position="Senior Developer", new_salary=70000)

ems.display_all_employees()

ems.remove_employee("John Doe")

ems.display_all_employees()
