<<<<<<< HEAD
import time
import pandas as pd
import numpy as np
from datetime import timedelta

# CITY_DATA dictionary defines the file name associated with each city.
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """Asks user to specify a city, month, and day to analyze.
    
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """ 
    print('\nHello! Let\'s explore some US bikeshare data!')
    # get user input for city and test the input validity 
    while True:
        try: 
            city = input('Would you like data on Washington, New York or Chicago?\nPlease type the city name: ').lower()
            if city in ['new york', 'chicago', 'washington']:
                print('Great, thanks for selecting {}.\n'.format(city.title()))
                break
            else:
                print('\nInvalid input, please try that again.')
        except ValueError:
            print('\nInvalid input, please try that again.')
        
    # get user input for month and test the input validity
    while True:
        try: 
            month = str(input('Which month would you like to get input on?\nPlease type a month from January to June or \"All\": ')).lower()
            if month in ['january', 'february', 'march', 'april', 'may', 'june', 'all']:
                print('Excellent choice, thanks for selecting {}.'.format(month.title()))
                break
            else:
                print('\nThat didn\'t match any of the choices, let\'s try that again!')
        except ValueError:
            print('\nInvalid input, please try that again.')
        
    # get user input for day of week and test the input validity
    while True:
        try: 
            day = str(input('\nWhich day would you like to get input on?\nPlease type any day of the week or \"All\": ')).lower()
            if day in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']:
                print('Awesome, thanks for selecting {}.'.format(day.title()))
                break
            else:
                print('\nInvalid input, please try that again.')
        except ValueError:
            print('\nInvalid input, please try that again.')
    
    print('-'*40)
    return city, month, day

def load_data(city, month, day):
    """Loads data for the specified city and filters by month and day if applicable.
    
    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month, day, changes index to date
    """
    # read the csv file for selected city
    file_name = CITY_DATA[city]
    df = pd.read_csv(file_name)
    
    # convert the Start anmd End Time column to to_datetime format
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    
    # extract month, day of week, hour, date and create new columns
    df['Month'] = df['Start Time'].dt.strftime('%B')
    df['Day of week'] = df['Start Time'].dt.day_name()
    df['Hour'] = df['Start Time'].dt.hour
    df['Date'] = df['Start Time'].dt.date
    # remove unwanted column for cleaner output
    df = df.drop('Unnamed: 0', axis=1)

    # filter by month if applicable
    if month != 'all':
        # filter by month to create the new dataframe
        df = df[df['Month']==(month).title()]
    
    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['Day of week']==(day).title()]
    
    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month using mode
    mode_month = df['Month'].mode()[0]
    print(f'The most common month is {mode_month}.')

    # display the most common day of week using mode
    mode_day = df['Day of week'].mode()[0]
    print(f'The most common day of the week is {mode_day}.')
    
    # display the most common start hour using mode
    mode_hour = df['Hour'].mode()[0]
    print(f'The most common hour of the day is {mode_hour}.')
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station using mode
    mode_start = df['Start Station'].mode()[0]
    print(f'Most commonly used start station is {mode_start}.')
    
    # display most commonly used end station using mode
    mode_end = df['End Station'].mode()[0]
    print(f'Most commonly used end station is {mode_end}.')
    
    # display most frequent combination of start station and end station trip
    # first, columns 'Start Station' and 'End Station' are joined to generate a string for entire journey
    df['Trip'] = df['Start Station'].astype(str)+(' to ')+df['End Station'].astype(str)
    mode_trip = df['Trip'].mode()[0] # mode used to find the most common complete journey
    print(f'The most frequent combination of start and end station: {mode_trip}')
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def seconds_to_hms(seconds):
    """Convert seconds to hours, minutes, seconds"""
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return hours, minutes, seconds

def trip_duration_stats(df):
    """Display statistics on the total and average trip duration."""
   
    # start_time to calculate computation time 
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    
    # display total travel time
    df['Trip Duration'] = df['End Time'] - df['Start Time']
    total_travel_time = df['Trip Duration'].sum()
    total_travel_time = int(total_travel_time.total_seconds())
    hours, minutes, seconds = seconds_to_hms(total_travel_time)
    print(f'The total amount of time travelled is {hours} hours, {minutes} minutes and {seconds} seconds.')

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    mean_travel_time = int(mean_travel_time.total_seconds())
    hours, minutes, seconds = seconds_to_hms(mean_travel_time)
    print(f'The average time travelled is {hours} hours, {minutes} minutes and {seconds} seconds.')
    
    # complete calculation of computation time
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
 
def user_stats(df):
    """Display statistics on bikeshare users.
    Checks for the 'Gender' and 'Birth Year' columns, as Washington dataset does not cpontain this data.
    """
    # start_time to calculate computation time
    print('\nCalculating User Stats...\n')
    start_time = time.time()
    
    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print(user_types)

    # Display counts of gender
    if 'Gender' in df.columns:
        gender = df['Gender'].value_counts()
        print('\n',gender, sep='')

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        oldest = int(df['Birth Year'].min())
        youngest = int(df['Birth Year'].max())
        mode_age = int(df['Birth Year'].mode()[0])
        print(f'\nThe oldest traveller was born in {oldest}, the youngest in {youngest} and the most common birth year is {mode_age}.')
    
    # complete calcualtion of computation time
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data(df):
    """ User given choice to view raw data.
    If 'Y', data is displayed 5 lines at a time.
    Continue iterating through raw data 5 lines at a time until user inputs 'N'.
    """
    # ask user if they would like to view the raw data
    while True:
        try:
            raw_data = str(input('Would you like to see raw data? (Y/N): ')).lower()
            if raw_data in ('y','n'):
                print(f'Confirming you have selected {raw_data}')
                break
            else:
                print('\nInvalid input, please try that again.')
        except ValueError:
            print('\nInvalid input, please try that again.')
    # commence iterating through raw data 5 lines at a time
    if raw_data != 'n':
        start_index = 0
        while start_index<(len(df)-5):
            print('Displaying 5 lines of data:')
            print(df.iloc[start_index:start_index + 5]) 
            # ask user if they want to see another 5 lines. Deliberately using 'Y/N' (vs Yes/No) to enable faster cycling through data.
            while True:
                try:
                    user_input = input('\nWould you like to see another 5 lines? (Y/N): ').lower()
                    if user_input in ('y','n'):
                        break
                    else:
                        print('\nThat didn\'t match any of the choices, let\'s try that again!')
                except ValueError:
                    print('\nInvalid input, please try that again.')
            
            if user_input != 'y':
                break
            else:
                start_index += 5
    # if user reaches end of the dataset, the message will change based on the remaining number of lines
    if user_input != 'n':
        remaining_lines = len(df)-start_index
        print(f'Displaying the last {remaining_lines} lines of dataset.')
        print(df.iloc[start_index:start_index + remaining_lines])
                    
    return(df)

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)

        restart = input('\nWould you like to restart? (Y/N): ').lower()
        if restart != 'y':
            break

if __name__ == "__main__":
	main()
||||||| parent of 3446c6c (Initial commit of bikeshare project files)
=======
import time
import pandas as pd
import numpy as np
from datetime import timedelta

CITY_DATA = { 'chicago': 'c:/Users/phili/Udacity/Bikeshare/chicago.csv',
              'new york': 'c:/Users/phili/Udacity/Bikeshare/new_york_city.csv',
              'washington': 'c:/Users/phili/Udacity/Bikeshare/washington.csv' }

def get_filters():
    """Asks user to specify a city, month, and day to analyze.
    
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """ 
    print('\nHello! Let\'s explore some US bikeshare data!')
    # get user input for city
    while True:
        try: 
            city = input('Would you like data on Washington, New York or Chicago?\nPlease type the city name: ').lower()
            if city in ['new york', 'chicago', 'washington']:
                print('Great, thanks for selecting {}.\n'.format(city.title()))
                break
            else:
                print('\nInvalid input, please try that again.')
        except ValueError:
            print('\nInvalid input, please try that again.')
        
    # get user input for month
    while True:
        try: 
            month = str(input('Which month would you like to get input on?\nPlease type a month from January to June or \"All\": ')).lower()
            if month in ['january', 'february', 'march', 'april', 'may', 'june', 'all']:
                print('Excellent choice, thanks for selecting {}.'.format(month.title()))
                break
            else:
                print('\nThat didn\'t match any of the choices, let\'s try that again!')
        except ValueError:
            print('\nInvalid input, please try that again.')
        
    # get user input for day of week
    while True:
        try: 
            day = str(input('\nWhich day would you like to get input on?\nPlease type any day of the week or \"All\": ')).lower()
            if day in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']:
                print('Awesome, thanks for selecting {}.'.format(day.title()))
                break
            else:
                print('\nInvalid input, please try that again.')
        except ValueError:
            print('\nInvalid input, please try that again.')
    
    print('-'*40)
    return city, month, day

def load_data(city, month, day):
    """Loads data for the specified city and filters by month and day if applicable.
    
    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month, day, changes index to date
    """
    # read the csv file for selected city
    file_name = CITY_DATA[city]
    df = pd.read_csv(file_name)
    
    # convert the Start anmd End Time column to to_datetime format
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    
    # extract month, day of week, hour, date and create new columns
    df['Month'] = df['Start Time'].dt.strftime('%B')
    df['Day of week'] = df['Start Time'].dt.day_name()
    df['Hour'] = df['Start Time'].dt.hour
    df['Date'] = df['Start Time'].dt.date
    # remove unwanted column for cleaner output
    df = df.drop('Unnamed: 0', axis=1)

    # filter by month if applicable
    if month != 'all':
        # filter by month to create the new dataframe
        df = df[df['Month']==(month).title()]
    
    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['Day of week']==(day).title()]
    
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    mode_month = df['Month'].mode()[0]
    print(f'The most common month is {mode_month}.')

    # display the most common day of week
    mode_day = df['Day of week'].mode()[0]
    print(f'The most common day of the week is {mode_day}.')
    
    # display the most common start hour
    mode_hour = df['Hour'].mode()[0]
    print(f'The most common hour of the day is {mode_hour}.')
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    mode_start = df['Start Station'].mode()[0]
    print(f'Most commonly used start station is {mode_start}.')
    
    # display most commonly used end station
    mode_end = df['End Station'].mode()[0]
    print(f'Most commonly used end station is {mode_end}.')
    
    # display most frequent combination of start station and end station trip
    df['Trip'] = df['Start Station'].astype(str)+(' to ')+df['End Station'].astype(str)
    mode_trip = df['Trip'].mode()[0]
    print(f'The most frequent combination of start and end station: {mode_trip}')
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def seconds_to_hms(seconds):
    """Convert seconds to hours, minutes, seconds"""
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return hours, minutes, seconds

def trip_duration_stats(df):
    """Display statistics on the total and average trip duration."""
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    
    # display total travel time
    df['Trip Duration'] = df['End Time'] - df['Start Time']
    total_travel_time = df['Trip Duration'].sum()
    total_travel_time = int(total_travel_time.total_seconds())
    hours, minutes, seconds = seconds_to_hms(total_travel_time)
    print(f'The total amount of time travelled is {hours} hours, {minutes} minutes and {seconds} seconds.')

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    mean_travel_time = int(mean_travel_time.total_seconds())
    hours, minutes, seconds = seconds_to_hms(mean_travel_time)
    print(f'The average time travelled is {hours} hours, {minutes} minutes and {seconds} seconds.')
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
 
def user_stats(df):
    """Display statistics on bikeshare users.
    Checks for the 'Gender' and 'Birth Year' columns, as Washington dataset does not cpontain this data.
    """

    print('\nCalculating User Stats...\n')
    start_time = time.time()
    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print(user_types)

    # Display counts of gender
    if 'Gender' in df.columns:
        gender = df['Gender'].value_counts()
        print('\n',gender, sep='')

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        oldest = int(df['Birth Year'].min())
        youngest = int(df['Birth Year'].max())
        mode_age = int(df['Birth Year'].mode()[0])
        print(f'\nThe oldest traveller was born in {oldest}, the youngest in {youngest} and the most common birth year is {mode_age}.')
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data(df):
    """ User given choice to view raw data.
    If 'Y', data is displayed 5 lines at a time.
    Continue iterating through raw data 5 lines at a time until user inputs 'N'.
    """

    while True:
        try:
            raw_data = str(input('Would you like to see raw data? (Y/N): ')).lower()
            if raw_data in ('y','n'):
                print(f'Confirming you have selected {raw_data}')
                break
            else:
                print('\nInvalid input, please try that again.')
        except ValueError:
            print('\nInvalid input, please try that again.')
    # commence iterating through data 5 lines at a time
    if raw_data != 'n':
        start_index = 0
        while start_index<(len(df)-5):
            print('Displaying 5 lines of data:')
            print(df.iloc[start_index:start_index + 5]) 
            # ask user if they want to see another 5 lines. Deliberately using 'Y/N' (vs Yes/No) to enable faster cycling through data.
            while True:
                try:
                    user_input = input('\nWould you like to see another 5 lines? (Y/N): ').lower()
                    if user_input in ('y','n'):
                        break
                    else:
                        print('\nThat didn\'t match any of the choices, let\'s try that again!')
                except ValueError:
                    print('\nInvalid input, please try that again.')
            
            if user_input != 'y':
                break
            else:
                start_index += 5
    # if user reaches end of the dataset, the message will change based on the remaining number of lines
    if user_input != 'n':
        remaining_lines = len(df)-start_index
        print(f'Displaying the last {remaining_lines} lines of dataset.')
        print(df.iloc[start_index:start_index + remaining_lines])
                    
    return(df)

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)

        restart = input('\nWould you like to restart? (Y/N): ').lower()
        if restart != 'y':
            break


if __name__ == "__main__":
	main()
>>>>>>> 3446c6c (Initial commit of bikeshare project files)
