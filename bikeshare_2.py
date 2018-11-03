import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

THIS_YEAR = 2018

def int_to_month(num):
    # function that simplifies printing month integers to the console
    if num == 1:
        return 'January'
    elif num == 2:
        return 'February'
    elif num == 3:
        return 'March'
    elif num == 4:
        return 'April'
    elif num == 5:
        return 'May'
    elif num == 6:
        return 'June'
    elif num == 7:
        return 'July'
    elif num == 8:
        return 'August'
    elif num == 9:
        return 'September'
    elif num == 10:
        return 'October'
    elif num == 11:
        return 'November'
    elif num == 12:
        return 'December'
    else:
        return num

def get_filters():
    print('Hello! Let\'s explore some US bikeshare data!')
    print('We have data for Chicago, New York City, and Washington.')
    print('Please type one of these cities.')

    while True:
        city = input().lower()
        if city == 'chicago' or city == 'new york city' or city == 'washington':
            print("You selected ", city.title())
            break
        else:
            print("We didn't fully understand what you typed: ", city)
            print("Please type 'Chicago, New York City, and Washington.'")
            continue

    print("Please type your desired month by name or number (ex: 'January' or '1') or 'all'")
    print("Note: Data is only available between January and June")
    while True:
        month = input().lower()
        # if this were C++ or Java, I'd vote for a switch statement.
        if month.lower() == 'january' or month == '1':
            month = 'January'
        elif month.lower() == 'february' or month == '2':
            month = 'February'
        elif month.lower() == 'march' or month == '3':
            month = 'March'
        elif month.lower() == 'april' or month == '4':
            month = 'April'
        elif month.lower() == 'may' or month == '5':
            month = 'May'
        elif month.lower() == 'june' or month == '6':
            month = 'June'
        elif month.lower() == 'july' or month == '7':
            month = 'July'
        elif month.lower() == 'august' or month == '8':
            month = 'August'
        elif month.lower() == 'september' or month == '9':
            month = 'September'
        elif month.lower() == 'october' or month == '10':
            month = 'October'
        elif month.lower() == 'november' or month == '11':
            month = 'November'
        elif month.lower() == 'december' or month == '12':
            month = 'December'
        elif month.lower() == 'all':
            month = 'all'
        else:
            print("It appears you picked a month outside our calendar range: ", month)
            print("Please type a valid month or number between 1 and 12.")
            continue

        print("You selected: ", month)
        break

    print("Please enter a number for your desired day of the week")
    print("Choose from the following: Su / 1, M / 2, Tu / 3, W / 4, Th / 5, F / 6, Sa / 7, or All")
    while True:
        day = input().lower()
        if day == 'su' or day == '1':
            day = 'Sunday'
        elif day == 'm' or day == '2':
            day = 'Monday'
        elif day == 'tu' or day == '3':
            day = 'Tuesday'
        elif day == 'w' or day == '4':
            day = 'Wednesday'
        elif day == 'th' or day == '5':
            day = 'Thursday'
        elif day == 'f' or day == '6':
            day = 'Friday'
        elif day == 'sa' or day == '7':
            day = 'Saturday'
        elif day == 'all':
            day = 'all'
        else:
            print("It appears you picked a day outside our weekly range: ", day)
            print("Please choose from the following: Su, M, Tu, W, Th, F, Sa, or All")
            continue
        print("You selected day: ", day)
        break

    print("Input is valid, you provided: ", city, " | ", month, " | ", day)
    print('-'*40)
    return city, month, day

def load_data(city, month, day):

    df = pd.read_csv(CITY_DATA[city]) #start by reading the correct csv

    # now we convert our Start Time column strings into Pandas DateTime objects
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # now we create a month column from the start-time column
    # this might create a negligible  inconsistency with our midnight riders on
    # the last day of the month
    df['month'] = df['Start Time'].dt.month

    # now we create a day_of_week column
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # refine the dataframe by selected month
    if month != 'all':  #this should leave the dataframe unfiltered by month
        # deconflicting the string month to np integer month
        months = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
        'August', 'September', 'October', 'November', 'December']
        num_month = months.index(month) + 1

        df = df[df['month'] == num_month]

    # Now we also filter by weekday_name
    if day != 'all': # don't filter anything if 'any' was selected
        df = df[df['day_of_week'] == day.title()]

    #data frame is complete and ready for further queries
    return df

def time_stats(df):

    start_time = time.time()
    print('\nCalculating The Most Frequent Times of Travel...\n')

    # display the most common month, if we only queried one month, this is not very significant
    num_months = len(df['month'].unique())
    popular_month = df['month'].mode()[0] #shows month with the highest count
    # not very significant if we only queried one day
    num_days = len(df['day_of_week'].unique())
    popular_day = df['day_of_week'].mode()[0]
    popular_start_hour = df['Start Time'].mode()[0].hour

    print("Total months in data: \n{}\n".format(num_months))
    print("Most popular month: \n{}\n".format(int_to_month(popular_month)))
    print("Total days in data: \n{}\n".format(num_days))
    print("Most popular day: \n{}\n".format(popular_day))
    print("Most popular starting hour: \n{}\n".format(popular_start_hour))

    print("\nThis query took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    start = (df['Start Station'].mode()[0])
    end = (df['End Station'].mode()[0])

    # add a column to track start-stop combinations
    # Since this is already wrangled we should have the same String values to combine
    df['Route'] = df['Start Station'] + ' -to- ' + df['End Station']
    pop_route = df['Route'].mode()[0]
    #TODO: add the count in its own column instead of using a mislabeled one



    print("The most commonly used start location is: \n{}\n".format(start))
    print("The most commonly used end location is: \n{}\n".format(end))
    print("The most popular route is: \n{}\n".format(pop_route))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    # """Displays statistics on the total and average trip duration."""
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    sum_travel_time_sec = df['Trip Duration'].sum()
    mean_travel_time_sec = df['Trip Duration'].mean()
    max_travel_time_sec = df['Trip Duration'].max()
    min_travel_time_sec = df['Trip Duration'].min()

    print("Total time traveled (all riders): \t{} hours".format(int(sum_travel_time_sec/3600)))
    print("Average time traveled for all riders: \t{} minutes {} seconds".format(
    int(mean_travel_time_sec/60), int(mean_travel_time_sec%60)))
    print("Longest ride: \t\t\t\t{} hours, {} minutes, {} seconds".format(
    int(max_travel_time_sec/3600), int(max_travel_time_sec/60), int(max_travel_time_sec%60)))
    print("Shortest ride: \t\t\t\t{} seconds".format(int(min_travel_time_sec)))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    # Displays statistics on bikeshare users
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    # This is outside the try block since we know this data exists
    user_type_cnt = df['User Type'].value_counts()
    print("User type summary: \n{}\n".format(user_type_cnt))

    # Per 1st submission feedback, the ideal solution for missing data
    # is a try-except block
    try:
        user_gender_cnt = df['Gender'].value_counts()
        # Display earliest, most recent, and most common year of birth
        oldest_rider = df['Birth Year'].min()
        youngest_rider = df['Birth Year'].max()
        most_common_rider_age = df['Birth Year'].mean()
        print("User gender summary: \n{}\n".format(user_gender_cnt))
        print("Oldest rider / earliest year of birth): \n{} / {}\n".format(
        int(THIS_YEAR - oldest_rider), int(oldest_rider)))
        print("Youngest rider / most recent year of birth): \n{} / {}\n".format(
        int(THIS_YEAR - youngest_rider), int(youngest_rider)))
        print("Average rider age / most common year of birth): \n{} / {}\n".format(
        int(THIS_YEAR - most_common_rider_age), int(most_common_rider_age)))
    except KeyError:
        print("It appears that this user query has no additional data")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

# Lets the user hit one key to got through the data 5 entries at a time
def step_through_data(df):
    cnt = 0
    print(df.head())
    while True:
        cnt = cnt + 5
        # indices = [cnt, cnt+1, cnt+2, cnt+3, cnt+4]
        print("Press 'y' for the next 5 entries:")
        next_five = input()
        if next_five.lower() == 'y':
            print(df.iloc[cnt:cnt+5])
            continue
        else:
            break

def main():
    welcome_str ="""
         ____  _ __           ____        __
        / __ )(_) /_____     / __ \____ _/ /_____ _
       / __  / / //_/ _ \   / / / / __ `/ __/ __ `/
      / /_/ / / ,< /  __/  / /_/ / /_/ / /_/ /_/ /
     /_____/_/_/|_|\___/  /_____/\__,_/\__/\__,_/

         ____               _           __
        / __ \_________    (_)__  _____/ /_
       / /_/ / ___/ __ \  / / _ \/ ___/ __/
      / ____/ /  / /_/ / / /  __/ /__/ /_
     /_/   /_/   \____/_/ /\___/\___/\__/
                     /___/
    """
    print(welcome_str)
    while True:
        # We'll handle input control in a 2nd loop within the get_filters() function
        city, month, day = get_filters()
        # create a filtered Pandas dataframe with a string, string, string parameters
        df = load_data(city, month, day)
        print("Data successfully queried.")
        instructions ="""
Please select what operation comes next:
1.) Show time stats
2.) Show Sation Stats
3.) Show Trip Duration Breakout
4.) Show User Stats
5.) Step through all data (increments of 5)
6.) See all data (will be truncated due to size of data)
type 'q' to quit
"""
        while True:
            print(instructions)
            selection = input()
            if selection.lower() == 'q':
                break
            elif selection == '1':
                time_stats(df)
                continue
            elif selection == '2':
                station_stats(df)
                continue
            elif selection == '3':
                trip_duration_stats(df)
                continue
            elif selection == '4':
                user_stats(df)
                continue
            elif selection == '5':
                step_through_data(df)
                continue
            elif selection == '6':
                print(df)
                continue
            else:
                print("It looks like we received an unexpected input: ", selection)
                print("Please re-enter your number selection or htt q to quit")
                continue

        restart = input('\nWould you like to query new data? Enter yes or no.\n')
        if restart.lower() != 'yes':
            goodbye= """
            GOODBYE!!!!
░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
░░░░░░░▄▄▀▀▀▀▀▀▀▀▀▀▄▄█▄░░░░▄░░░░█░░░░░░░
░░░░░░█▀░░░░░░░░░░░░░▀▀█▄░░░▀░░░░░░░░░▄░
░░░░▄▀░░░░░░░░░░░░░░░░░▀██░░░▄▀▀▀▄▄░░▀░░
░░▄█▀▄█▀▀▀▀▄░░░░░░▄▀▀█▄░▀█▄░░█▄░░░▀█░░░░
░▄█░▄▀░░▄▄▄░█░░░▄▀▄█▄░▀█░░█▄░░▀█░░░░█░░░
▄█░░█░░░▀▀▀░█░░▄█░▀▀▀░░█░░░█▄░░█░░░░█░░░
██░░░▀▄░░░▄█▀░░░▀▄▄▄▄▄█▀░░░▀█░░█▄░░░█░░░
██░░░░░▀▀▀░░░░░░░░░░░░░░░░░░█░▄█░░░░█░░░
██░░░░░░░░░░░░░░░░░░░░░█░░░░██▀░░░░█▄░░░
██░░░░░░░░░░░░░░░░░░░░░█░░░░█░░░░░░░▀▀█▄
██░░░░░░░░░░░░░░░░░░░░█░░░░░█░░░░░░░▄▄██
░██░░░░░░░░░░░░░░░░░░▄▀░░░░░█░░░░░░░▀▀█▄
░▀█░░░░░░█░░░░░░░░░▄█▀░░░░░░█░░░░░░░▄▄██
░▄██▄░░░░░▀▀▀▄▄▄▄▀▀░░░░░░░░░█░░░░░░░▀▀█▄
░░▀▀▀▀░░░░░░░░░░░░░░░░░░░░░░█▄▄▄▄▄▄▄▄▄██
░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
            """
            print(goodbye)
            break

if __name__ == "__main__":
	main()
