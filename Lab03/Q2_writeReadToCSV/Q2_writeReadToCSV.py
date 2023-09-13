import csv

def readFromCSVFile(filename):
    file = open(filename, 'r')

    data = list(csv.reader(file, delimiter=","))

    printCSVContents(data)
    print([row[2] for row in data])
    print([float(row[2]) for row in data[1:]])

    sum_ages = sum([float(row[2]) for row in data[1:]])
    sum_grades = sum([float(row[3]) for row in data[1:]])
    count_students = len(data) - 1
    average_grade = sum_grades /count_students
    average_age = sum_ages/count_students

    print("\n ************ Quick Analysis ************")
    print("Total number of students: {0}".format(count_students))
    print("Average Grade: {0:.2f}%".format(average_grade))
    print("Average student age: {0:.2f}".format(average_age))


def printCSVContents(data):
    for row in data:
        print(row)
def writeToCSVFile(header, data, name):
    with open(name, 'w', encoding='UTF8', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerows(data)
def main():

    csvFileName = 'Students.csv'

    header = ["ID", "Name", "Age", "Grade"]

    data = [[1 , "Harmonie", 18, 97],
            [2,"Harry",17,75],
            [3, "Ron", 19, 70],
            [4, "Luna", 16, 81],
            [5, "Emily", 15, 85]]

    writeToCSVFile(header, data, csvFileName)
    readFromCSVFile(csvFileName)

if __name__ == '__main__':
    main()