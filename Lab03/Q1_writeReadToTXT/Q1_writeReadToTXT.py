
def updateDataTypes(data):

    updated_list = []
    for item in data:
        item = item.strip()
        try:
            converted_item = int(item)
        except ValueError:
            try:
                converted_item = float(item)

            except ValueError:

                converted_item = item

        updated_list.append(converted_item)

    return updated_list
def readFromTxtFile(name):

    with open (name, 'r') as file:
        data = file.read()

    my_list = data.split(',')
    my_list = [item.strip() for item in my_list]
    return my_list

def writeToTxtFile(data, name):
    data = ",".join(map(str, data))

    with open(name, 'w') as file:
       for item in data:
           file.write("{0}".format(item))
def main():
    listFileName = "ListData.txt"
    myListOut = [1,2,3,'a','b','c',True, False, 10.99, 9.99, 8.99]
    writeToTxtFile(myListOut, listFileName)

    myListIn = readFromTxtFile(listFileName)
    myListIn = updateDataTypes(myListIn)

    for item in myListIn:
        print(item, type(item))


if __name__ == '__main__':
    main()
