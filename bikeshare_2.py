import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }


#TODO: comeback and make this data input a little more versatile and human readable
def get_filters():
    print('Hello! Let\'s explore some US bikeshare data!')
    print('We have data for Chicago, New York City, and Washington.')
    print('Please type one of these cities.')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input().lower()
        if city == 'chicago' or city == 'new york city' or city == 'washington':
            print("You selected ", city.title())
            break
        else:
            print("We didn't fully understand what you typed: ", city)
            print("Please type 'Chicago, New York City, and Washington.'")
            continue

    print("Please type your desired month by name or number (ex: 'January' or '1')")
    while True:
        month = input()
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
    print("Choose from the following: Su, M, Tu, W, Th, F, Sa, or Any")
    while True:
        day = input()
        if day.lower() == 'su' or day == '1':
            day = 'Sunday'
        elif day.lower() == 'm' or day == '2':
            day = 'Monday'
        elif day.lower() == 'tu' or day == '3':
            day = 'Tuesday'
        elif day.lower() == 'w' or day == '4':
            day = 'Wednesday'
        elif day.lower() == 'th' or day == '5':
            day = 'Thursday'
        elif day.lower() == 'f' or day == '6':
            day = 'Friday'
        elif day.lower() == 'sa' or day == '7':
            day = 'Saturday'
        elif day.lower() == 'any':
            day = 'any'
        else:
            print("It appears you picked a day outside our weekly range: ", day)
            print("Please choose from the following: Su, M, Tu, W, Th, F, Sa, or Any")
            continue
        print("You selected day: ", day)
        break

#     good_str = """
# ┌┌┌┌┌┌┌┌┌┌┌┌┌┌┌┌┌┌┌┌┌┌┌┌┌┌┌┌┌┌┌┌┌┌┌┌┌┌┌┌
# ┌┌┌┌┌┌┌┌┌┌┌█████┌┌┌┌┌┌┌┌┌┌┌┌┌┌┌┌┌┌┌┌┌┌┌┌
# ┌┌┌┌┌┌┌┌┌┌███████┌┌┌┌┌┌┌┌┌┌┌┌┌┌┌┌┌┌┌┌┌┌┌
# ┌┌┌┌┌┌┌┌┌███┌┌┌██┌┌┌┌┌┌┌┌┌┌┌┌┌┌┌┌┌┌┌┌┌┌┌
# ┌┌┌┌┌┌┌┌┌██┌┌┌┌██┌┌┌┌┌┌┌┌┌┌┌┌┌┌┌┌┌┌┌┌┌┌┌
# ┌┌┌┌┌┌┌┌███┌┌┌┌███┌┌┌┌┌┌┌┌┌┌┌┌┌┌┌┌┌┌┌┌┌┌
# ┌┌┌┌┌┌┌┌███┌┌┌┌███┌┌┌┌┌┌┌┌┌┌┌┌┌┌┌┌┌┌┌┌┌┌
# ┌┌┌┌┌┌┌┌┌██┌┌┌┌┌███┌┌┌┌┌┌┌┌┌┌┌┌┌┌┌┌┌┌┌┌┌
# ┌┌┌┌┌┌┌┌┌███┌┌┌┌┌███┌┌┌┌┌┌┌┌┌┌┌┌┌┌┌┌┌┌┌┌
# ┌┌┌┌┌┌┌┌┌┌███┌┌┌┌┌████┌┌┌┌┌┌┌┌┌┌┌┌┌┌┌┌┌┌
# ┌┌┌┌┌┌┌┌┌┌┌██┌┌┌┌┌┌████┌┌┌┌┌┌┌┌┌┌┌┌┌┌┌┌┌
# ┌┌┌┌┌┌┌┌┌┌┌███┌┌┌┌┌┌┌███┌┌┌┌┌┌┌┌┌┌┌┌┌┌┌┌
# ┌┌┌┌┌┌┌┌┌┌┌┌███┌┌┌┌┌┌┌███┌┌┌┌┌┌┌┌┌┌┌┌┌┌┌
# ┌┌┌┌┌┌┌┌┌┌┌┌███┌┌┌┌┌┌┌┌███┌┌┌┌┌┌┌┌┌┌┌┌┌┌
# ┌┌┌┌┌┌┌┌┌┌┌┌┌██┌┌┌┌┌┌┌┌┌┌███┌┌┌┌┌┌┌┌┌┌┌┌
# ┌┌┌┌┌┌┌┌┌███┌███┌┌┌┌┌┌┌┌┌┌██┌┌┌┌┌┌┌┌┌┌┌┌
# ┌┌┌┌████████████┌┌┌┌┌┌┌┌┌┌┌███┌┌┌┌┌┌┌┌┌┌
# ┌┌████████┌┌┌┌┌┌┌┌┌┌┌┌┌┌┌┌┌┌███┌┌┌┌┌┌┌┌┌
# ┌███┌┌┌┌┌┌┌┌┌┌┌┌┌┌┌┌┌┌┌┌┌┌┌┌┌█████████┌┌
# ███┌┌┌┌█████████┌┌┌┌┌┌┌┌┌┌┌┌┌┌┌┌┌┌█████┌
# ██┌┌┌███████┌████┌┌┌┌┌┌┌┌┌┌┌┌┌┌┌┌┌┌┌███┌
# ██┌┌┌┌███┌┌┌┌┌┌┌███┌┌┌┌┌┌┌┌┌┌┌┌┌┌┌┌┌┌██┌
# ███┌┌┌┌┌┌┌┌┌┌┌█████┌┌┌┌┌┌┌┌┌┌┌┌┌┌┌┌┌┌██┌
# ┌███┌┌┌┌┌┌┌████████┌┌┌┌┌┌┌┌┌┌┌┌┌┌┌┌┌┌██┌
# ┌┌████████████┌┌┌████┌┌┌┌┌┌┌┌┌┌┌┌┌┌┌┌██┌
# ┌███┌██████┌┌┌┌┌┌┌████┌┌┌┌┌┌┌┌┌┌┌┌┌┌┌██┌
# ┌███┌┌┌┌┌┌┌┌┌┌┌██████┌┌┌┌┌┌┌┌┌┌┌┌┌┌┌┌██┌
# ┌┌████┌████┌██████████┌┌┌┌┌┌┌┌┌┌┌┌┌┌┌██┌
# ┌┌┌████████████┌┌┌┌┌███┌┌┌┌┌┌┌┌┌┌┌┌┌███┌
# ┌┌┌┌██┌┌┌┌┌┌┌┌┌┌┌███████┌┌┌┌┌┌┌███████┌┌
# ┌┌┌┌████┌┌┌┌┌┌████████┌┌┌┌┌┌┌┌████████┌┌
# ┌┌┌┌┌████████████┌┌┌███┌┌┌┌┌███┌┌┌┌┌┌┌┌┌
# ┌┌┌┌┌┌┌┌███┌█┌█┌┌┌┌┌┌███┌┌┌███┌┌┌┌┌┌┌┌┌┌
# ┌┌┌┌┌┌┌┌███┌┌┌┌┌┌█████┌┌█████┌┌┌┌┌┌┌┌┌┌┌
# ┌┌┌┌┌┌┌┌┌██████████████████┌┌┌┌┌┌┌┌┌┌┌┌┌
# ┌┌┌┌┌┌┌┌┌┌██████████████┌┌┌┌┌┌┌┌┌┌┌┌┌┌┌┌
# ┌┌┌┌┌┌┌┌┌┌┌┌┌┌┌┌┌┌┌┌┌┌┌┌┌┌┌┌┌┌┌┌┌┌┌┌┌┌┌┌
#     """
    # print(good_str)
    print("You provided: ", city, " | ", month, " | ", day)
    print('-'*40)
    return city, month, day

# I borrowed a bit from Exercise 3 of the class material here
def load_data(city, month, day):
    # """
    # Loads data for the specified city and filters by month and day if applicable.
    #
    # Args:
    #     (str) city - name of the city to analyze
    #     (str) month - name of the month to filter by, or "all" to apply no month filter
    #     (str) day - name of the day of week to filter by, or "all" to apply no day filter
    # Returns:
    #     df - Pandas DataFrame containing city data filtered by month and day
    # """

    #start by reading the correct csv
    df = pd.read_csv(CITY_DATA[city])

    # now we'll need to convert our Start Time column strings into Pandas DateTime objects
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # now we'll create a month column from the start-time column
    # this might create a negligible  inconsistency with our midnight riders on
    # the last day of the month
    df['month'] = df['Start Time'].dt.month

    # now we'll create a day_of_week column
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # we need some way of deconflicting the string month to np integer month
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
        'August', 'September', 'October', 'November', 'December']
    num_month = months.index(month) + 1

    # Now we'll refine the dataframe by selected month
    if month != 'all':  #this should leave the dataframe unfiltered by month
        df = df[df['month'] == num_month]

    # Now we'll filter by weekday_name
    if day != 'any': # don't filter anything if 'any' was selected
        df = df[df['day_of_week'] == day.title()]

    return df


# def time_stats(df):
    # """Displays statistics on the most frequent times of travel."""
    #
    # print('\nCalculating The Most Frequent Times of Travel...\n')
    # start_time = time.time()
    #
    # # display the most common month
    #
    #
    # # display the most common day of week
    #
    #
    # # display the most common start hour
    #
    #
    # print("\nThis took %s seconds." % (time.time() - start_time))
    # print('-'*40)


# def station_stats(df):
    # """Displays statistics on the most popular stations and trip."""
    #
    # print('\nCalculating The Most Popular Stations and Trip...\n')
    # start_time = time.time()

    # display most commonly used start station


    # display most commonly used end station


    # display most frequent combination of start station and end station trip

    #
    # print("\nThis took %s seconds." % (time.time() - start_time))
    # print('-'*40)


# def trip_duration_stats(df):
    # """Displays statistics on the total and average trip duration."""
    #
    # print('\nCalculating Trip Duration...\n')
    # start_time = time.time()
    #
    # # display total travel time
    #
    #
    # # display mean travel time
    #
    #
    # print("\nThis took %s seconds." % (time.time() - start_time))
    # print('-'*40)


# def user_stats(df):
    # """Displays statistics on bikeshare users."""
    #
    # print('\nCalculating User Stats...\n')
    # start_time = time.time()
    #
    # # Display counts of user types
    #
    #
    # # Display counts of gender
    #
    #
    # # Display earliest, most recent, and most common year of birth
    #
    #
    # print("\nThis took %s seconds." % (time.time() - start_time))
    # print('-'*40)
    #

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

        #TODO: ask user for
        #1) Most popular route
        #2) Rider Age breakout
        #3) Trip duration breakout
        #4) User Stats: Type | Gender | Oldest, youngest, and most common age | Time to execute

        # time_stats(df)
        # station_stats(df)
        # trip_duration_stats(df)
        # user_stats(df)
        print(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
