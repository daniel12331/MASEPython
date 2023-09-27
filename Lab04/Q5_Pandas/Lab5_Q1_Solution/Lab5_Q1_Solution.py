import pandas as pd
from tabulate import tabulate
import matplotlib.pyplot as plt

def main():
    data = {
        'Product': ['Book', 'Book', 'TShirt', 'TShirt', 'Book', 'Logo Set'],
        'Title': ['HP & the Philosophers Stone', 'HP & the Deathly Hallows', 'Gryffindor House', 'Hufflepuff House', 'The Hobbit', 'Hogwarts Astronomy Tower'],
        'Price':[9.99,15.99,25.50,49.99,25.99,59.99],
        'Quantity':[126,300,780,660,1100,1100]
    }

    df = pd.DataFrame(data)

    df['Total'] = df['Price'] * df['Quantity']

    pd.options.display.float_format = '{:.2f}'.format

    print(df)

    prodTotals = df.groupby('Product').agg({'Quantity' : 'sum', 'Total':'sum'}).reset_index()

    plt.figure(figsize=(8,6))
    plt.bar(prodTotals['Product'], prodTotals['Quantity'], label ='Quantity Sold', color='blue', bottom = prodTotals['Total'])
    plt.bar(prodTotals['Product'], prodTotals['Total'], label='Total Sales', color='red')

    plt.xlabel('Product')
    plt.ylabel('Amount')
    plt.title('Quantity and Total Sales by Product')
    plt.legend()

    plt.show()

    grouped = df.groupby('Product')['Quantity'].sum().reset_index()

    plt.figure(figsize=(8,6))
    plt.pie(grouped['Quantity'], labels=grouped['Product'], autopct='%1.1f%%', startangle=140)
    plt.title('Product Distribution by Category')
    plt.show()


if __name__ == '__main__':
    main()