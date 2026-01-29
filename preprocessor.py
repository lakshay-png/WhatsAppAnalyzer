import re
import pandas as pd

def preprocess(data):
    pattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'

    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    df = pd.DataFrame({'user_message': messages, 'message_date': dates})
    df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%Y, %H:%M - ')
    df.rename(columns={'message_date': 'date'}, inplace=True)

    users = []
    messages_content = []  # Renamed to avoid conflict with the global 'messages' variable

    for message in df['user_message']:
        entry = re.split(r'([\w\W]+?):\s', message)

        if entry[1:]:
            users.append(entry[1])
            messages_content.append(entry[2])
        else:
            users.append('group_notification')
            messages_content.append(entry[0])

    df['user'] = users
    df['message'] = messages_content
    df.drop(columns=['user_message'], inplace=True)

    df['year'] = df['date'].dt.year
    df['month_num']= df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['day_name']=df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    period = []

    for hour in df['hour']:
        start = f"{hour:02d}"
        end = f"{(hour + 1) % 24:02d}"
        period.append(f"{start}-{end}")

    df['period'] = period

    return df
