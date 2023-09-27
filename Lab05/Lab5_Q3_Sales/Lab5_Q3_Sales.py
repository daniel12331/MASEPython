import pandas as pd
import matplotlib.pyplot as plt
from tabulate import tabulate
import time



def main():
    pd.options.display.float_format = '{:.2f}'.format
    print("Pandas Lab")
    local_file = "https://davmase.z6.web.core.windows.net/data/sales.csv"
    start = time.time()
    sales = pd.read_csv(local_file)
    end = time.time()
    print("Time taken to load data: {0:.5f} seconds".format(end-start))
    print(sales.info(verbose=True, memory_usage='deep',show_counts=True))
    printDF(sales, False)
    # CountProductLine(sales)
    sales = calculateSalesTaxes(sales)
    sales['Total'] = sales['Total'].apply(lambda x: round(x, 2))
    sales['Tax'] = sales['Tax'].apply(lambda x: round(x, 2))
    sales['Total Inc Tax'] = round(sales['Total Inc Tax'], 2)
    printDF(sales, False)
    salesByGender(sales)
    salesByBranch(sales)
    plotByMonth(sales)

def productTotals(dataF):
    prodTotals = dataF.groupby('Product line').agg({'Quantity':'sum', 'Total':'sum'}).reset_index()
    printDF(prodTotals, True)
    plt.figure(figsize=(12,12))
    plt.bar(prodTotals['Product line'], prodTotals['Total'], label='Total Sales')
    plt.xlabel('Product')
    plt.ylabel('Total Sales')
    plt.title('Quantity and Total Sales by Product')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def salesByGender(dataF):
    grouped = dataF.groupby('Gender')['Total'].sum().reset_index()
    printDF(grouped, True)

    plt.figure(figsize=(8,6))
    plt.pie(grouped['Total'], labels=grouped['Gender'], autopct='%1.1f%%',startangle=140)
    plt.title('Sales by Gender')
    plt.show()

def salesByBranch(dataF):
    grouped = dataF.groupby('Branch')['Total'].sum().reset_index()
    printDF(grouped,True)
    plt.figure(figsize=(8,6))
    plt.pie(grouped['Total'], labels=grouped['Branch'], autopct='%1.1f%%',startangle=140)
    plt.title('Sales by branch')
    plt.show()

def plotByMonth(dataF):
    month_names = {
        1:'January',2:'Feburary',3:'March',
        4: 'April',5:'May',6:'June',
        7: 'July',8:'August',9:'September',
        10: 'October',11:'November',12:'December',
    }

    dataF['Date'] = pd.to_datetime(dataF['Date'])
    dataF['Month'] = dataF['Date'].dt.month
    monthly_data = dataF.groupby('Month').agg({'Total' : 'sum'}).reset_index()

    monthly_data['Month'] = monthly_data['Month'].map(month_names)
    print(monthly_data)

    plt.figure(figsize=(8,6))
    plt.plot(monthly_data['Month'], monthly_data['Total'], label='Revenue Total by month', marker='o', linestyle='-')
    plt.xlabel('Month')
    plt.ylabel('Totals')
    plt.title('Total by month')
    plt.show()

def printDF(dataF, printOpt):
    if printOpt == True:
        print(tabulate(dataF, headers='keys',tablefmt='pretty',stralign='left',numalign='Right'))
    else:
        print(tabulate(dataF.head(), headers='keys', tablefmt='pretty', stralign='left', numalign='Right'))
        print(tabulate(dataF.tail(), headers='keys', tablefmt='pretty', stralign='left', numalign='Right'))


def CountProductLine(dataF):
    productLine = dataF['Product line'].value_counts().to_frame().reset_index()
    productLine = productLine.rename(columns={'count':'Prod Order Count'})
    printDF(productLine, True)

    plt.figure(figsize=(13,8))
    plt.bar(productLine['Product line'], productLine['Prod Order Count'], label='Instances of Order by Product')
    plt.xlabel('Product')
    plt.ylabel('Number of orders placed')
    plt.title('Number of order placed by product - NOT QUANTITY')
    plt.xticks(rotation=45)
    plt.tight_layout()
    #plt.savefig("Product.png")
    plt.show()

def calculateSalesTaxes(dataF):
    dataF['Total'] = dataF['Unit price'] * dataF['Quantity']
    dataF['Tax'] = dataF['Total'] * 0.5
    dataF['Total Inc Tax'] = dataF['Total'] + dataF['Tax']
    return dataF

if __name__ == '__main__':
    main()