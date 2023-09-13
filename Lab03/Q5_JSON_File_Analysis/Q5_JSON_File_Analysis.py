import json
import tabulate

def readFromJson(name):
    with open(name, 'r') as json_file:
        Heros = json.load(json_file)

    printListOfDict(Heros)


    total_heroes = len(Heros)

    total_height = sum(float(row["Height"]) for row in Heros)
    avg_height = total_height / total_heroes

    total_weight = sum(float(row["Weight"]) for row in Heros)
    avg_weight = total_weight / total_heroes

    print("\n ****** Quick Analysis ********")
    print(" Total number of heros: {0}".format(total_heroes))
    print(" Average Height of heros: {0}".format(avg_height))
    print(" Average Weight of heros: {0}".format(avg_weight))

    total_females = 0
    total_males = 0
    for person in Heros:
        if person["Gender"] == "Female":
            total_females += 1
        else:
            total_males += 1

    print("\n Heros by gender")
    print(" Female -> {0}".format(total_females))
    print(" Male -> {0}".format(total_males))

    eye_yellow = 0
    eye_blue = 0
    eye_red = 0
    eye_green = 0
    eye_black = 0

    for hero in Heros:
        if hero["Eye color"] == "Yellow":
            eye_yellow += 1
        elif hero["Eye color"] == "Blue":
            eye_blue += 1
        elif hero["Eye color"] == "Red":
            eye_red += 1
        elif hero["Eye color"] == "Green":
            eye_green += 1
        else:
            eye_black += 1

    print("\n Heros with eye colour of: ")
    print(" Yellow -> {0}".format(eye_yellow))
    print(" Blue -> {0}".format(eye_blue))
    print(" Red -> {0}".format(eye_red))
    print(" Green -> {0}".format(eye_green))
    print(" Black -> {0}".format(eye_black))

    no_hair = 0
    black_hair = 0
    blue_hair = 0

    for hero in Heros:
        if hero["Hair color"] == "No Hair":
            no_hair += 1
        elif hero["Hair color"] == "Black":
            black_hair +=1
        else:
            blue_hair += 1

    print("\n Heros with hair colour of: ")
    print(" No Hair -> {0}".format(no_hair))
    print(" Blue -> {0}".format(blue_hair))
    print(" Black -> {0}".format(black_hair))

    grey_skin = 0
    blue_skin = 0
    white_skin = 0
    red_skin = 0
    green_skin = 0

    for hero in Heros:
        if hero["Skin color"] == "Grey":
            grey_skin += 1
        elif hero["Skin color"] == "Blue":
            blue_skin += 1
        elif hero["Skin color"] == "White":
            white_skin += 1
        elif hero["Skin color"] == "Red":
            red_skin += 1
        else:
            green_skin += 1

    print("\n Heros with skin colour of: ")
    print(" Grey -> {0}".format(grey_skin))
    print(" Blue -> {0}".format(blue_skin))
    print(" White -> {0}".format(white_skin))
    print(" Red -> {0}".format(red_skin))
    print(" Green -> {0}".format(green_skin))

    alignment_good = 0
    alignment_bad = 0

    for hero in Heros:
        if hero["Alignment"] == "Bad":
            alignment_bad += 1
        else:
            alignment_good += 1

    print("\n Heros with alignment of: ")
    print(" Good -> {0}".format(alignment_good))
    print(" Bad -> {0}".format(alignment_bad))


    marvel_publish = 0
    dc_publish = 0
    darkhorse_publish = 0

    for hero in Heros:
        if hero["Publisher"] == "Marvel Comics":
            marvel_publish += 1
        elif hero["Publisher"] == "DC Comics":
            dc_publish +=1
        else:
            darkhorse_publish += 1


    print("\n Heros with alignment of: ")
    print(" Marvel Comics -> {0}".format(marvel_publish))
    print(" DC Comics -> {0}".format(dc_publish))
    print(" Dark Horse Comics -> {0}".format(darkhorse_publish))





def printListOfDict(data):
    header = data[0].keys()
    rows = [x.values() for x in data]

    print(tabulate.tabulate(rows, header))
def main():
    jsonFileName = "Heroes.json"
    readFromJson(jsonFileName)


if __name__ == '__main__':
    main()
