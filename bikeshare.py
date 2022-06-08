import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}


def check_input(input_str, input_type):
    """
    Check the validity of user input

    Args:
        input_str(str): is the input of the user
        input_type(int): is the type of input: 1 = city, 2 = month, 3 = day
    Returns:
        input_read
    >>> check_input("Which Month (all, january, ... june)?", 2)
    may
    """
    while True:
        input_read = input(input_str).lower()
        try:
            if input_read in ['chicago', 'new york city', 'washington'] and input_type == 1:
                break
            elif input_read in ['january', 'february', 'march', 'april', 'may', 'june', 'all'] and input_type == 2:
                break
            elif input_read in ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'all'] and input_type == 3:
                break
            else:
                if input_type == 1:
                    print(
                        "Sorry, your input should be: chicago new york city or washington")
                if input_type == 2:
                    print(
                        "Sorry, your input should be: january, february, march, april, may, june or all")
                if input_type == 3:
                    print(
                        "Sorry, your input should be: sunday, ... friday, saturday or all")
        except ValueError:
            print("Sorry, your input is wrong")
    return input_read


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = check_input(
        "Would you like to see the data for chicago, new york city or washington?", 1)

    # TO DO: get user input for month (all, january, february, ... , june)
    month = check_input("Which Month (all, january, ... june)?", 2)

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    day = check_input("Which day? (all, monday, tuesday, ... sunday)", 3)

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    #  Load data file into a DataFrame
    df = pd.read_csv(CITY_DATA[city])

    # Convert the Start Time column into datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month, day of week, hour from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month  # Mobth
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        # Get number of month using index
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        # Convert day_name to title to math day's column
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = df['month'].mode()[0]

    print(f'Most Popular Month:{popular_month}')

    # display the most common day of week
    popular_day_of_week = df['day_of_week'].mode()[0]

    print(f'Most Day Of Week:{popular_day_of_week}')

    # display the most common start hour
    popular_common_start_hour = df['hour'].mode()[0]

    print(f'Most Common Start Hour:{popular_common_start_hour}')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]

    print(f'Most Start Station:\n\t\t{popular_start_station}')

    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]

    print(f'Most End Station:\n\t\t{popular_end_station}\n')

    # display most frequent combination of start station and end station trip
    group_field = df.groupby(['Start Station', 'End Station'])
    popular_combination_station = group_field.size().sort_values(ascending=False).head(1)
    print(
        f'Most frequent combination of Start Station and End Station trip:\n\n{popular_combination_station}')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()

    print(f'Total Travel Time: {total_travel_time}')

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()

    print(f'Mean Travel Time: {mean_travel_time}')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('User Type Stats:')
    print(f"{df['User Type'].value_counts()}")
    if city != 'washington':
        # Display counts of gender
        print('\nGender Stats:')
        print(f"{df['Gender'].value_counts()}\n")
        # Display earliest, most recent, and most common year of birth
        print('Birth Year Stats:')
        most_common_year = df['Birth Year'].mode()[0]
        print(f'Most Common Year: {int(most_common_year)}')
        most_recent_year = df['Birth Year'].max()
        print(f'Most Recent Year: {int(most_recent_year)}')
        earliest_year = df['Birth Year'].min()
        print(f'Earliest Year: {int(earliest_year)}')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
