import pandas as pd



# Get drivers ID
def get_driver_id(driver_name, connection):
    query_drivers_names = "SELECT * FROM drivers WHERE CONCAT(forename, ' ', surname) = '{0}'".format(driver_name)
    df_mysql = pd.read_sql(query_drivers_names, con=connection)
    driver_id = df_mysql['driverId'][0]
    return driver_id


# Get the first five fastests the driver has made
def get_driver_fastests_laps(connection, driver_name):
    pd.set_option('display.max_columns', None)

    driver_id = get_driver_id(driver_name, connection)
    # Joining three tables results, races, circuits and select fastestLapTime, fastestLapSpeed, circuits.name, circuits.country
    query_drivers_results = "SELECT fastestLapTime, fastestLapSpeed, circuits.name, circuits.country, year FROM results INNER JOIN races on results.raceId = races.raceId INNER JOIN circuits on races.circuitId = circuits.circuitId WHERE driverId = {0}".format(
        driver_id)
    df_mysql = pd.read_sql(query_drivers_results, con=connection)

    # Sort by the top five fastests laps and convert the track time into total seconds
    df_first_five_laps = df_mysql.sort_values(by=['fastestLapTime']).head(5)
    df_first_five_laps['racetracks'] = df_first_five_laps['name'] + "-" + df_first_five_laps['country'] + " (" + \
                                       df_first_five_laps['fastestLapTime'] + ")"

    # Using regex to format the lap times into total seconds
    d = {'^(\d+\.\d+)$': r'00:00:\1', '^(\d+:\d+\.\d+)$': r'00:\1'}
    df_first_five_laps['fastestLapTime'] = df_first_five_laps['fastestLapTime'].replace(d, regex=True).apply(
        pd.to_timedelta).dt.total_seconds()

    return df_first_five_laps


def get_driver_wins_losses(connection, driver_name):
    pd.set_option('display.max_columns', None)
    driver_id = get_driver_id(driver_name, connection)
    #
    query_drivers_wins_loses = "SELECT wins FROM driver_standings WHERE driverId = {0}".format(driver_id)
    df_mysql = pd.read_sql(query_drivers_wins_loses, con=connection)
    total_wins = ((df_mysql['wins']).sum())
    total_loses = ((df_mysql['wins'] == 0).sum())
    return total_wins, total_loses


def get_driver_average_pitstop_lap(connection, driver_name):
    pd.set_option('display.max_columns', None)
    driver_id = get_driver_id(driver_name, connection)
    #
    query_driver_average_pitstop = "SELECT results.raceId, duration FROM results INNER JOIN pit_stops on results.raceId = pit_stops.raceId WHERE results.driverId = {0}".format(
        driver_id)
    df_mysql = pd.read_sql(query_driver_average_pitstop, con=connection)
    # Changing the duration column to numeric and changing unfitting values to Nan
    df_mysql['duration'] = pd.to_numeric(df_mysql['duration'], errors='coerce')
    # Drop NaN values
    cleaned_df_average_pit_stop = df_mysql.dropna()
    # Group by raceid and get average pit stop duration per race
    cleaned_df_average_pit_stop = cleaned_df_average_pit_stop.groupby(['raceId']).mean().reset_index()
    return cleaned_df_average_pit_stop


def get_driver_top_speed(connection, driver_name):
    pd.set_option('display.max_rows', None)
    driver_id = get_driver_id(driver_name, connection)
    #
    query_driver_average_pitstop = "SELECT circuits.name, fastestLapSpeed FROM results INNER JOIN races on results.raceId = races.raceId JOIN circuits on races.circuitId = circuits.circuitId WHERE results.driverId = {0}".format(
        driver_id)
    df_mysql = pd.read_sql(query_driver_average_pitstop, con=connection)
    # format and turn \N values into NaN
    df_mysql['fastestLapSpeed'] = pd.to_numeric(df_mysql['fastestLapSpeed'], errors='coerce')
    # drop the NA values
    df_mysql.dropna(inplace=True)
    # group by name and get the highest fastestLapTime for each circuit(name)
    cleaned_top_speed = df_mysql.loc[df_mysql.groupby(['name'])['fastestLapSpeed'].idxmax()]
    # get top 5 fastests speeds
    top_per_circuit = cleaned_top_speed.sort_values(by=['fastestLapSpeed'], ascending=False).head(5)

    return top_per_circuit

