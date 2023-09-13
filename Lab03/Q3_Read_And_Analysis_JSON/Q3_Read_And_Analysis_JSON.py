import json
import tabulate

def printListOfDict(data):
    header = data[0].keys()
    rows = [x.values() for x in data]
    print(tabulate.tabulate(rows, header))
def readFromJson(name):

    with open(name, 'r') as json_file:
        grades = json.load(json_file)

    print("\n Working with a list of dictionaries loaded from JSON file")
    printListOfDict(grades)

    sum_ages = sum([float(row["Age"]) for row in grades])
    sum_grades = sum([float(row["Grade"]) for row in grades])
    count_students = len(grades)
    average_grade = sum_grades/count_students
    average_age = sum_ages/count_students

    print("\n ************ Quick Analysis ************")
    print("Total number of students: {0}".format(count_students))
    print("Average Grade: {0:.2f}%".format(average_grade))
    print("Average student age: {0:.2f}".format(average_age))


def main():
    jsonFileName = "Grades.json"
    readFromJson(jsonFileName)


if __name__ == '__main__':
    main()




