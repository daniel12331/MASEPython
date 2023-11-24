import pandas as pd



# Get drivers ID
def get_driver_id(driver_name, connection):
    query_drivers_names = "SELECT * FROM drivers WHERE CONCAT(forename, ' ', surname) = '{0}'".format(driver_name)
    df_mysql = pd.read_sql(query_drivers_names, con=connection)
    driver_id = df_mysql['driverId'][0]
    return driver_id

def get_driver_constructor_points(connection, driver_name):
    pd.set_option('display.max_rows', None)
    driver_id = get_driver_id(driver_name, connection)
    #
    query_driver_average_pitstop = "Select constructor_standings.points as 'constructor_points', driver_standings.points as 'driver_points' from driver_standings Inner join constructor_standings on driver_standings.raceId = constructor_standings.raceId where driverId = {0}".format(
        driver_id)
    df_mysql = pd.read_sql(query_driver_average_pitstop, con=connection)

    # Change data to numeric
    df_mysql['constructor_points'] = pd.to_numeric(df_mysql['constructor_points'], errors='coerce')
    df_mysql['driver_points'] = pd.to_numeric(df_mysql['driver_points'], errors='coerce')

    # Drop any rows with NaNs
    df_mysql.dropna(inplace=True)

    return df_mysql


def get_driver_constructor_wins(connection, driver_name):
    pd.set_option('display.max_rows', None)
    driver_id = get_driver_id(driver_name, connection)
    #
    query_driver_average_pitstop = "select constructor_standings.wins as 'constructor_wins', driver_standings.wins as 'driver_wins' from driver_standings Inner join constructor_standings on driver_standings.raceId = constructor_standings.raceId where driverId = {0}".format(
        driver_id)
    df_mysql = pd.read_sql(query_driver_average_pitstop, con=connection)

    # Change data to numeric
    df_mysql['constructor_wins'] = pd.to_numeric(df_mysql['constructor_wins'], errors='coerce')
    df_mysql['driver_wins'] = pd.to_numeric(df_mysql['driver_wins'], errors='coerce')
    # Drop any rows with NaNs
    df_mysql.dropna(inplace=True)

    df_top_fifteen_wins_constructor = df_mysql.sort_values(by=['constructor_wins'], ascending=False).head(15)

    return df_top_fifteen_wins_constructor

def get_driver_status_races(connection, driver_name):
    pd.set_option('display.max_columns', None)
    driver_id = get_driver_id(driver_name, connection)
    #
    query_driver_status = "select raceId,status from results Inner join status on results.statusId = status.statusId where driverId ={0}".format(
        driver_id)
    df_mysql = pd.read_sql(query_driver_status, con=connection)
    # No need to format the dataframe as the dtype is object already
    # Drop any rows with NaNs
    df_mysql.dropna(inplace=True)
    # Group the total status counts and sort the aesceding order, name the column "count"
    df_status_grouped_sorted = df_mysql.groupby('status')['raceId'].nunique().sort_values(ascending=True).reset_index(name="count")
    df_status_grouped_sorted['count'] = pd.to_numeric(df_status_grouped_sorted['count'], errors='coerce')
    return df_status_grouped_sorted

def get_driver_fastestlap_count(connection, driver_name):
    pd.set_option('display.max_columns', None)
    driver_id = get_driver_id(driver_name, connection)
    #
    query_driver_status = "select fastestLap from results where driverId = {0}".format(
        driver_id)
    df_mysql = pd.read_sql(query_driver_status, con=connection)
    # Change from object to int type
    df_mysql['fastestLap'] = pd.to_numeric(df_mysql['fastestLap'], errors='coerce')
    # Drop any NaNs
    df_mysql.dropna(inplace=True)

    return df_mysql
