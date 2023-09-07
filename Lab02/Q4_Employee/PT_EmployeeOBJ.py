from EmployeeObj import EmployeeOBJ


class PartTimeEmployee(EmployeeOBJ):
    def __init__(self, name, employee_id, hourly_rate, hours_worked):
        super().__init__(name, employee_id)
        self.hourly_rate = hourly_rate
        self.hours_worked = hours_worked

    def calculate_pay(self):
        return round(self.hourly_rate * self.hours_worked)

    def display_info(self):
        super().display_info()
        print("Hours Worked: {0}hrs".format(self.hours_worked))
        print("Hourly Rate: ${0}".format(self.hourly_rate))
        print("Salary: ${0:.2f}".format(self.calculate_pay()))
