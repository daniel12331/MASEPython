import random
import matplotlib.pyplot as plt

def countDistinct(unique, data):

    plotdata = []
    count = []

    for item in unique:
        plotdata.append(item)
        count.append(data.count(item))
        print("{0} -> {1}".format(item, data.count(item)))

    fig,ax = plt.subplots()
    ax.bar(plotdata, count)
    ax.set_ylabel("Occurrences")
    ax.set_xlabel("Unique Values")
    ax.set_title("Set Items")
    plt.xticks(plotdata)
    plt.show()

def generate_random_list(size):
    random_list = []
    for i in range(1,size +1):
        random_num = random.randint(1,10)
        random_list.append(random_num)

    return random_list

def main():
    list_size = 30

    random_list = generate_random_list(list_size)

    list_set = set(dict.fromkeys(random_list))

    print(random_list)
    print(list_set)
    countDistinct(list_set, random_list)





if __name__ == '__main__':

    main()

