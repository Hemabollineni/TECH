class Employee:

    def __init__(self, name, salary):
        self.name = name
        self.salary = salary

    def display(self):
        print("Employee Name:", self.name)
        print("Employee Salary:", self.salary)


# Creating an employee object
emp1 = Employee("Hema", 30000)

# Calling the display method
emp1.display()