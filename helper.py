import numpy as np


def data_over_time(df,col):

    nations_over_time = df.drop_duplicates(['Year', col])['Year'].value_counts().reset_index().sort_values('Year')
    nations_over_time.rename(columns={'Year': 'Edition', 'count': col}, inplace=True)
    return nations_over_time


def most_successful(df, sport):
    # Drop rows where the 'Medal' column is NaN
    temp_df = df.dropna(subset=['Medal'])

    # Filter by sport if it's not 'Overall'
    if sport != 'Overall':
        temp_df = temp_df[temp_df['Sport'] == sport]

    successful_athletes = temp_df['Name'].value_counts().reset_index().head(15)
    successful_athletes.columns = ['Name', 'Medal Count']
    merged_df = successful_athletes.merge(df, left_on='Name', right_on='Name', how='left')
    result_df = merged_df[['Name', 'Medal Count', 'Sport', 'region']].drop_duplicates('Name')
    return result_df


def fetch_medal_tally(df,unique_year, country):
    medal_df = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    flag = 0
    if unique_year == 'Overall' and country == 'Overall':
        temp_df = medal_df
    if unique_year == 'Overall' and country != 'Overall':
        flag = 1
        temp_df = medal_df[medal_df['region'] == country]
    if unique_year != 'Overall' and country == 'Overall':
        temp_df = medal_df[medal_df['Year'] == int(unique_year)]
    if unique_year != 'Overall' and country != 'Overall':
        temp_df = medal_df[(medal_df['Year'] == int(unique_year)) & (medal_df['region'] == country)]

    if flag == 1:
        x = temp_df.groupby('Year').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Year').reset_index()
    else:
        x = temp_df.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold',
                                                                                      ascending=False).reset_index()

    x['total'] = x['Gold'] + x['Silver'] + x['Bronze']
    return x

def medal_tally(df):
    medal_tally = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    medal_tally = medal_tally.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold',
                                                                                                ascending=False).reset_index()
    medal_tally['total'] = medal_tally['Gold'] + medal_tally['Silver'] + medal_tally['Bronze']
    return medal_tally


def country_year_list(df):
    unique_years = df['Year'].unique().tolist()
    unique_years.sort()
    unique_years.insert(0, "Overall")

    country = np.unique(df['region'].dropna().values).tolist()
    country.sort()
    country.insert(0, "Overall")

    return unique_years, country

def yearwise_medal_tally(df,country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)
    new_df = temp_df[temp_df['region'] == country]
    final_df = new_df.groupby('Year').count()['Medal'].reset_index()
    return final_df

def country_event_heatmap(df,country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)
    new_df = temp_df[temp_df['region'] == country]

    pt = new_df.pivot_table(index='Sport',columns='Year',values='Medal',aggfunc='count').fillna(0)
    return pt


def most_successful_country_wise(df, country):
    # Drop rows where the 'Medal' column is NaN
    temp_df = df.dropna(subset=['Medal'])

    temp_df = temp_df[temp_df['region'] == country]

    # Get the top 15 most successful athletes
    successful_athletes = temp_df['Name'].value_counts().reset_index().head(15)

    # Rename columns to avoid conflicts
    successful_athletes.columns = ['Name', 'Medal Count']

    # Merge with the original dataframe
    merged_df = successful_athletes.merge(df, left_on='Name', right_on='Name', how='left')

    result_df = merged_df[['Name', 'Medal Count', 'Sport', 'region']].drop_duplicates('Name')
    return result_df

def weight_v_height(df,sport):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    athlete_df['Medal'].fillna('No Medal', inplace=True)
    if sport != 'Overall':
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        return temp_df
    else:
        return athlete_df

def men_vs_women(df):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])

    men = athlete_df[athlete_df['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
    women = athlete_df[athlete_df['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()

    final = men.merge(women, on='Year', how='left')
    final.rename(columns={'Name_x': 'Male', 'Name_y': 'Female'}, inplace=True)

    final.fillna(0, inplace=True)

    return final