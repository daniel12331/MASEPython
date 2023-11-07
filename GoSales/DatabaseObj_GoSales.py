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
        self.host, self.user, self.password, self.port, self.database = connectInfo
        self.connectionProgress = ""
        self.tableInfo = None
        self.mydb = None
        # Create empty dataframes for each table and the merged dataframe
        self.go_daily_sales = None
        self.go_products = None
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
        print(self.connectionProgress)
        print("\n\nUsing Tables: \ngo_daily_sales\ngo_products")
        self.preformEDA('go_daily_sales')
        self.preformEDA('go_products')




    def preformEDA(self, tablenme):
        print("The performEDA function")
        query = "SELECT * FROM " + tablenme
        frame = pd.read_sql(query, self.mydb)
        print("\n\n\n ******************** {0} ***************".format(tablenme))

        print('\n\nPrint Dataframe Info for table {0}'.format(tablenme))
        print(frame.info())
        print('\n\nPrint Number of Unique Items in Each Column for table {0}'.format(tablenme))
        print(frame.apply(pd.unique))
        print("\n\nTable: {0}".format(tablenme))
        print(tabulate(frame.head(), headers='keys', tablefmt='pretty', showindex=True))
        print(tabulate(frame.tail(), headers='keys', tablefmt='pretty', showindex=True))

        if tablenme == "go_daily_sales" :
            self.go_daily_sales = frame.copy()
        else:
            self.go_products = frame.copy()
    def MergeDataFrame(self):
        print("\n\nMerged Dataframe")
        products = self.go_products[['Product number', 'Product', 'Unit cost']]
        self.merged_df = pd.merge(products, self.go_daily_sales[['Product number', 'Date', 'Quantity', 'Unit price', 'Unit sale price']],
                                  on='Product number', how='inner')
        self.merged_df['Total Sales'] = round(self.merged_df['Quantity'] * self.merged_df['Unit sale price'],2)
        self.merged_df['Total Profit'] = round(self.merged_df['Total Sales'] - (self.merged_df['Quantity'] * self.merged_df['Unit cost']),2)
        print(tabulate(self.merged_df.head(), headers='keys', tablefmt='pretty', showindex=True))
        print(tabulate(self.merged_df.tail(), headers='keys', tablefmt='pretty', showindex=True))



    def analyseTop10QuantitySales(self):
        print("The analyseTop10QuantitySales function")
        # Create a dataframe called product_sums that is an agg of merged_df based on the
        self.product_sums = self.merged_df.groupby('Product').agg({'Product number':'count', 'Unit price': 'first', 'Quantity':'sum', 'Total Sales' : 'sum', 'Total Profit':'sum'}).reset_index()
        # screenshot in the assessment sheet
        # Creae a resultset dataframe whic is the result of the 10 nlaregest where the columns are total sales
        # Order decending
        resultset = self.product_sums.nlargest(n=10, columns="Total Sales").sort_values('Total Sales', ascending=False)

        # Print this result using tabulate and rename the headers as per the screenshot
        print(tabulate(resultset, headers=['Product','No of Sales','Unit Price','Quantity Sold','Total Sales','Total Profit'], showindex=True))
        # Next create the plot but first

        wrapped_labels = [textwrap.fill(label, 10) for label in resultset['Product']]

        root = tk.Tk()
        root.title("GoSales")

        frame = ttk.Frame(root)
        frame.pack(expand=True, fill=tk.BOTH)

        fig,ax = plt.subplots(figsize=(5,4), dpi=100)
        ax.ticklabel_format(axis='y',style='plain')
        ax.set_xticks(range(len(wrapped_labels)))
        ax.set_xticklabels(wrapped_labels)

        ax.bar(resultset['Product'], resultset['Total Sales'], label='Total Sales',color='red')
        ax.bar(resultset['Product'], resultset['Total Profit'], label='Total Profit',color='blue', bottom=resultset['Total Sales'])
        ax.set_xlabel('Product')
        ax.set_ylabel('Amount in $')
        ax.set_title('Top 10 Products based on Sales and Profit')
        ax.legend()

        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)


        from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
        toolbar = NavigationToolbar2Tk(canvas,frame)
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        toolbar.update()

        root.mainloop()

    def analyseProductByID(self, prod_ID):
        print("The analyseProductByID function")
        resultset = self.merged_df[self.merged_df['Product number']==prod_ID]
        #Create a resultset form the merged_df based on the prodID
        print(tabulate(resultset,headers='keys' ,showindex=True))
        orders = resultset[['Date','Quantity','Unit sale price', 'Total Sales', 'Total Profit']]
        filtered = orders[orders['Unit sale price'] != 0]
        unitPrice = resultset['Unit Price'][0]
        unitCost = resultset['Unit cost'][0]
        total_sold = filtered['Quantity'].sum()
        total_sales = filtered['Total Sales'][0]
        total_profit = filtered['Total Profit'][0]
        total_orders = len(filtered)
        print('Unit Price: {0}'.format(unitPrice))
        print('Unit Cost: {0}'.format(unitCost))
        print('Orders: {0}'.format(total_orders))
        print('Sold: {0}'.format(total_sold))
        print('Sales : {0}'.format(round(total_sales,2)))
        print('Profit: {0}'.format(round(total_profit)),2)

        root = tk.Tk()
        root.title("Go Sales")

        frame = ttk.Frame(root)
        frame.pack(expand=True, fill=tk.BOTH)

        fig, ax = plt.subplots(figsize=(5, 4), dpi=100)
        ax.ticklabel_format(axis='y', style='plain')
        # ax.set_xticks(range(len(wrapped_labels)))
        # ax.set_xticklabels(wrapped_labels)

        ax.bar('Total Sales', total_sales, label='Total Sales', color='red')
        ax.bar('Total Profit', total_profit, label='Total Profit', color='blue')
        ax.set_xlabel('Sales')
        ax.set_ylabel('Amount in $')
        ax.set_title('Product by ID: {0}'.format(prod_ID))
        ax.legend()

        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
        toolbar = NavigationToolbar2Tk(canvas, frame)
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        toolbar.update()

        root.mainloop()
    def printDF(self, dataF):
        print('Print the dataF using tabulate')
        #Using tabulate print the head and tail of the dataF

    def disposeConnection(self):
        print("Close the connection")
        # Close the database connection
        self.mydb.dispose()

