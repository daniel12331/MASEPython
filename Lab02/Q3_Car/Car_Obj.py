class CarObj:
    def __init__(self, make, model):
        self._make = make
        self.__model = model

    # Public get make accessor
    def get_make(self):
        return self._make

    # Public set make accessor
    def set_make(self, make):
        self._make = make

    # Private get model accessor
    def __get_model(self):
        return self.__model

    # Private set model accessor
    def __set_model(self, __model):
        self.__model = __model

    # Public update set model func
    def update_model(self, model):
        self.__set_model(model)


    def display_details(self):
        print("-- Car Details -- \n Make:{0} \n Model:{1}".format(self.get_make(), self.__get_model()))
