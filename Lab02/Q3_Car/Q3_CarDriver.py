from Car_Obj import CarObj

def main():
    car = CarObj("Ford", "Focus")
    car.display_details()
    print(car.get_make())

    car.set_make("VW")
    car.update_model("LM")

    car.display_details()


if __name__ == '__main__':
    main()
