import pandas as pd
from tabulate import tabulate
import matplotlib.pyplot as plt


def main():
    data = {
        "Day" :['Mon','Tue','Wed','Thur','Fri','Sat','Sun'],
        "Category":['Run','Run','Walk','Run','Rest','Run','Walk'],
        "Distance":[10,12,5.6,10,"Rest",32.2,5],
        "Time":[53,102,72,55,"Rest",187,58],
        "Calories":[769,967,387,788,"Rest",2559,340]
    }
    df = pd.DataFrame(data)
    print(df)
    df = cleanRestDays(df)
    print(df)
    df = calculateSpped(df)
    print(df)
    calorieTotals(df)
    caloriesBurned(df, 500)
    distanceQuery(df, 10,12)
    runTimeQuery(df, 55)
    calculateRunTotals(df)



def cleanRestDays(dataF):
    dataF[['Distance','Time','Calories']] = dataF[['Distance','Time','Calories']].apply(pd.to_numeric, errors='coerce')
    return dataF
def calculateSpped(dataF):
    print('Calculateing Speed')
    for i,(d,t) in enumerate(zip(dataF['Distance'], dataF['Time'])):
        try:
            dataF.loc[i,'Speed'] = round(d/(t/60),2)
        except ZeroDivisonError:
            dataF.loc[i,'Speed'] = np.nan
    return dataF

def calorieTotals(dataF):
    activityCalorieSum = dataF.groupby('Category')['Calories'].sum().to_frame()

    activityCalorieSum.plot(kind="pie", autopct='%.2f%%', subplots=True)
    plt.title("Total Calories Burned")
    plt.show()

def caloriesBurned(dataF, calories):
    print("\n\nQuery Results: Activites where < {0} calories were burned".format(calories))
    condition = dataF['Calories'] < calories
    filtered_df = dataF.loc[condition]
    print(filtered_df)

def distanceQuery(dataF, low, high):
    print("\n\nQuery results: Activities between {0}klm - {1}klm".format(low,high))
    query1 = dataF.query('Distance >= @low and Distance <= @high')
    query1.plot(kind="bar", x="Day", y="Distance")
    plt.title("Activites between {0}klm - {1}klm".format(low,high))
    plt.xticks(rotation=0)
    plt.show()

def runTimeQuery(dataF, time):
    print("\n\nQuery Results: Running activites more than {0} minutes".format(time))
    query1 = dataF.query('`Category` == "Run" and Time > @time')
    print(query1)

def calculateRunTotals(dataF):
    runQuery = dataF.query('`Category` == "Run"')
    totalTime = runQuery['Time'].sum()
    totalRuns = len(runQuery.index)
    totalDistance = runQuery['Distance'].sum()
    totalCalories = runQuery['Calories'].sum()
    averageSpeed = runQuery['Speed'].mean()

    print("\nAnalysis for the runs during the week"
          "\nNumber of Runs: \t\t\t\t {0}"
          "\nTotal Distance: \t\t\t\t {1:.2f}km"
          "\nTotal Calories Burned: \t\t\t\t {2:.2f}"
          "\nTotal Running Time: \t\t\t\t {3:.0f} minutes"
          "\nAverage Speed: \t\t\t\t {4:.2f} klm/hour"
          .format(totalRuns, totalDistance, totalCalories, totalTime, averageSpeed))

if __name__ == '__main__':
    main()