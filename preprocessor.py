import re
import pandas as pd

def preprocess(data):
    # add current whatsapp format of data 
    pattern = r'\[(\d{1,2}/\d{1,2}/\d{2},\s\d{1,2}:\d{2}:\d{2}.*?)]\s'

    messages = re.split(pattern, data)[1:]

    dates = messages[0::2]
    user_messages = messages[1::2]

    df = pd.DataFrame({
        'message_date': dates,
        'user_message': user_messages
    })
    
    #Fix datetime parsing for AM/PM timestamps
    df['message_date'] = pd.to_datetime(
        df['message_date'],
        format='%d/%m/%y, %I:%M:%S %p'
    )

    df.rename(columns={'message_date': 'date'}, inplace=True)

    users = []
    messages = []

    for message in df['user_message']:
        entry = re.split(r'([\w\W]+?):\s', message, maxsplit=1)

        if len(entry) > 2:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group_notification')
            messages.append(entry[0])

    df['user'] = users
    df['message'] = messages

    df.drop(columns=['user_message'], inplace=True)

    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    period = []
 # setting a timeline
    for hour in df['hour']:
        start = str(hour)
        end = str((hour + 1) % 24)
        period.append(start + "-" + end)

    df['period'] = period

    return df
