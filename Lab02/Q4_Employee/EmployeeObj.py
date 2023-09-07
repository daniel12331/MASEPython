class EmployeeOBJ:
    def __init__(self, name, employee_id):
        self.__name = name
        self.__employee_id = employee_id

    def display_info(self):
        print("-- Employee Details -- \n Name: {0} \n ID: {1}".format(self.__name, self.__employee_id))

    def get_employee_name(self):
        return self.__name

    def get_employee_id(self):
        return self.__employee_id