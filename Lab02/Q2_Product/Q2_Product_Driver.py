from Product_Obj import Product


def main():
    print("Products")
    new_product = Product("Stanley 13 Ounce Wood Hammer", 12.99, 62)
    new_product.get_product_details()

    new_product = Product('National Hardware 3/4" Wire Nails', 12.99, 62)
    new_product.get_product_details()


if __name__ == '__main__':
    main()
