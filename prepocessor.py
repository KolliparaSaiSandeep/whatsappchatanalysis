import re
import pandas as pd

def preprocess(data):
    date_pattern = r'\d{2}/\d{2}/\d{2}, \d{1,2}:\d{2}[ap]m'
    dates = re.findall(date_pattern, data)
    messages = re.split(date_pattern, data)[1:]
    messages = messages[1:]
    df = pd.DataFrame(list(zip(messages, dates)), columns=['Message', 'Date'])
    df['message_date'] = pd.to_datetime(df['Date'], format='%d/%m/%y, %I:%M%p')
    df.rename(columns={'message_date': 'date'}, inplace=True)
    users = []
    messages = []
    for message in df['Message']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:  
            users.append(entry[1])
            messages.append(" ".join(entry[2:]))
        else:
            users.append('group_notification')
            messages.append(entry[0])
    df.drop('date',axis=1)
    df.drop('date',axis=1)
    users = []
    messages = []
    for message in df['Message']:
        entry = re.split('([\w\W]+?):\s', message)
        print(entry)
        if entry[1:]:  # user name
            users.append(entry[1])
            messages.append(" ".join(entry[2:]))
        else:
            users.append('group_notification')
            messages.append(entry[0])
    df['user'] = users
    df['message'] = messages
    df.drop(columns=['Message'], inplace=True)
    df.drop(columns=['Date'], inplace=True)
    df['only_date'] = df['date'].dt.date
    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute
    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))
    df['period'] = period
    print(df.head())
    return df
