import pandas as pd
from tabulate import tabulate
from sqlalchemy import create_engine, inspect
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import textwrap

class DBConnection:
    def __init__(self, connectInfo):
        print("Inside the Constructor")
        self.host, self.user, self.password, self.port, self.database = connectInfo
        self.connectionProgress = ""
        self.tableInfo = None
        self.mydb = None
        # Create empty dataframes for each table and the merged dataframe
        self.orderdetails = None
        self.orders = None
        self.products = None
        self.merged_df = None
        self.product_sums = None
        self.db_config = {
            'host': self.host,
            'user': self.user,
            'password': self.password,
            'port': self.port,
            'database': self.database
        }
        # Once configured then call the ConnectNow, getConnectionProgress and
        # MergeDataFrame functions
        self.ConnectNow()
        self.getConnectionProgress()
        self.MergeDataFrame()

    def ConnectNow(self):
        print("The ConnectNow function")
        # Print the connection data to the user so they can see what was entered
        print("New connection using: "
              "\nHost: {0}"
              "\nUser: {1}"
              "\nPassword: {2}"
              "\nPort: {3}"
              "\nDatabase: {4}\n\n".format(self.host,self.user,self.password,self.port, self.database)
              )

        # Establish a connection
        try:
            # Create a SQLAlchemy engine to connect to the database
            self.mydb = create_engine(
                f"mysql://{self.db_config['user']}:{self.db_config['password']}@{self.db_config['host']}:{self.db_config['port']}/{self.db_config['database']}"
            )
            # Create an Inspector object to inspect the database
            inspector = inspect(self.mydb)

            # Get the list of table names in the database
            table_names = inspector.get_table_names()

            # Print the list of table names
            self.connectionProgress += "Tables in the database:"
            for table_name in table_names:
                self.connectionProgress += "\n" + table_name


        # Handle the exception if the connection fails or any other error occurs
        except Exception as error:
            print("Error: Unable to connect to the MySQL database")
            print(f"Error Details: {error}")

    def getConnectionProgress(self):
        # Print the connection pr◘ogress
        print(self.connectionProgress)
        print("\nThe getConnectionProgress function")
        # Print to the console what tables are being used
        print("\n\nUsing Tables: \norderdetails\nproducts\norders")
        # Call the preformEDA functions for each table
        self.preformEDA('products')
        self.preformEDA('orders')
        self.preformEDA('orderdetails')



    def preformEDA(self, tablenme):
        print("The performEDA function")
        query = "SELECT * FROM " + tablenme
        frame = pd.read_sql(query, self.mydb)
        print("\n\n\n ******************** {0} ********************".format(tablenme))

        print('\n\nPrint Dataframe Info for table {0}'.format(tablenme))
        print(frame.info())
        print('\n\nPrint Number of Unique Items in Each Column for table {0}'.format(tablenme))
        print(frame.apply(pd.unique))
        print("\n\nTable: {0}".format(tablenme))
        print(tabulate(frame.head(), headers='keys', tablefmt='pretty', showindex=True))
        print(tabulate(frame.tail(), headers='keys', tablefmt='pretty', showindex=True))

        if tablenme == "orderdetails" :
            self.orderdetails = frame.copy()
        elif tablenme == "orders":
            self.orders = frame.copy()
        else:
            self.products = frame.copy()

    def MergeDataFrame(self):
        print("\n\nMerged Dataframe")
        orders = self.orders[['orderNumber', 'orderDate', 'requiredDate', 'shippedDate']]
        self.merged_df = pd.merge(orders, self.orderdetails[['orderNumber','productCode', 'quantityOrdered', 'priceEach']],
                                  on='orderNumber', how='inner')
        self.merged_df = pd.merge(self.merged_df, self.products[['productCode','productName','productLine','quantityInStock', 'buyPrice', 'MSRP']],
                                  on='productCode', how='inner')
        self.merged_df['discountPerUnit'] = round(self.merged_df['MSRP'] - self.merged_df['priceEach'], 2)
        self.merged_df['orderTotal'] = round(self.merged_df['quantityOrdered'] * self.merged_df['priceEach'], 2)
        self.merged_df['customerSavings'] = round((self.merged_df['MSRP'] * self.merged_df['quantityOrdered']) - self.merged_df['orderTotal'], 2)
        self.merged_df['profit'] = round(self.merged_df['orderTotal'] - (self.merged_df['buyPrice'] * self.merged_df['quantityOrdered']),2)
        print(tabulate(self.merged_df.head(15), headers='keys', tablefmt='pretty', showindex=True))

    def analyseTop10QuantitySales(self):
        print("The analyseTop10QuantitySales function")
        # Create a dataframe called product_sums that is an agg of merged_df based on the

        self.product_sums = self.merged_df.groupby('productName').agg({'productLine':'first','productCode':'count','quantityOrdered':'sum', 'orderTotal' : 'sum', 'profit':'sum'}).reset_index()
        # screenshot in the assessment sheet
        # Creae a resultset dataframe whic is the result of the 10 nlaregest where the columns are total sales
        # Order decending
        resultset = self.product_sums.nlargest(n=10, columns="orderTotal").sort_values('orderTotal', ascending=False)
        # Print this result using tabulate and rename the headers as per the screenshot
        print(tabulate(resultset, tablefmt='pretty',headers=['Name','Line','Number of Orders','Total Ordered','Total Sales','Total Profit'], showindex=True))
        # Next create the plot but first

        wrapped_labels = [textwrap.fill(label, 10) for label in resultset['productName']]


        fig,ax = plt.subplots(figsize=(5,4), dpi=100)
        ax.ticklabel_format(axis='y',style='plain')
        ax.set_xticks(range(len(wrapped_labels)))
        ax.set_xticklabels(wrapped_labels)

        ax.bar(resultset['productName'], resultset['orderTotal'], label='Total Sales',color='red')
        ax.bar(resultset['productName'], resultset['profit'], label='Total Profit',color='blue', bottom=resultset['orderTotal'])
        ax.set_xlabel('Product')
        ax.set_ylabel('Amount in $')
        ax.set_title('Top 10 Products based on Sales and Profit')
        ax.legend()
        plt.show()
    def analyseProductByID(self, prod_ID):
        print("The analyseProductByID function")
        resultset = self.merged_df[self.merged_df['productCode'] == prod_ID]
        # Create a resultset form the merged_df based on the prodID
        orders = resultset[['orderDate', 'requiredDate', 'shippedDate', 'quantityOrdered', 'priceEach', 'discountPerUnit', 'orderTotal', 'customerSavings', 'profit']]
        productName = resultset['productName'].iat[0]
        productLine = resultset['productLine'].iat[0]
        QuantityStock = resultset['quantityInStock'].iat[0]
        unitPrice = resultset['buyPrice'].iat[0]
        MSRP = resultset['MSRP'].iat[0]
        Orders = resultset['quantityOrdered'].iat[1]
        Sold = resultset['quantityOrdered'].sum()
        Sales = resultset['orderTotal'].sum()
        Profit = resultset['profit'].sum()

        print('Product Name: {0}'.format(productName))
        print('Product Line: {0}'.format(productLine))
        print('Quantity in stock: {0}'.format(QuantityStock))
        print('Unit Price: ${0}'.format(unitPrice))
        print('MSRP: ${0}'.format(MSRP))
        print('Orders : {0}'.format(round(Orders, 2)))
        print('Sold: {0}'.format(round(Sold, 2)))
        print('Sales: ${0}'.format(round(Sales, 2)))
        print('Profit: ${0}'.format(round(Profit, 2)))
        print(tabulate(resultset.head(15), tablefmt='pretty', headers='keys', showindex=True))

        fig, ax = plt.subplots(figsize=(5, 4), dpi=100)
        ax.ticklabel_format(axis='y', style='plain')
        # ax.set_xticks(range(len(wrapped_labels)))
        # ax.set_xticklabels(wrapped_labels)

        ax.bar('Total Sales', Sales, label='Total Sales', color='red')
        ax.bar('Total Profit', Profit, label='Total Profit', color='blue')
        ax.set_xlabel('Sales')
        ax.set_ylabel('Amount in $')
        ax.set_title('Product by ID: {0}'.format(prod_ID))
        ax.legend()
        plt.show()

        plt.plot(resultset['orderDate'], resultset['quantityOrdered'])
        plt.title('Total Order per month')
        plt.xlabel('Month')
        plt.ylabel('Total Orders')
        plt.show()
    
    def productLineSummary(self):
        print('Product Line Summary')

        line = self.products['productLine'].value_counts()
        print(line)
        plt.pie(self.products['productLine'].value_counts().values, labels=self.products['productLine'].value_counts().index)
        plt.show()
    def printDF(self, dataF):
        print('Print the dataF using tabulate')
        #Using tabulate print the head and tail of the dataF

    def disposeConnection(self):
        print("Close the connection")
        # Close the database connection

