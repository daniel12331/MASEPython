from FT_EmployeeOBJ import FullTimeEmployee
from PT_EmployeeOBJ import PartTimeEmployee


def main():
    new_ft_employee = FullTimeEmployee("Daniel", 1, 33000)
    new_ft_employee.display_info()

    new_pt_employee = PartTimeEmployee("Daniel", 2, 11.34, 10)
    new_pt_employee.display_info()

if __name__ == '__main__':
    main()