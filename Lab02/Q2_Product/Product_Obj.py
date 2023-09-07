class Product:
    def __init__(self, name, price, discount_percent):
        self.name = name
        self.price = price
        self.discount_percent = discount_percent

    def get_discount_amount(self):
        return self.discount_percent

    def get_discount_price(self):
        discount_price = self.price * self.discount_percent / 100
        return format(self.price - discount_price, ".2f")

    def get_product_details(self):
        print(
            "Product Name: {0} \n Product Discount: {1}% \n Product Price: ${2} \n Product Price with discount: ${3}".format(self.name, self.discount_percent, self.price, Product.get_discount_price(self)))
