from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji

extract = URLExtract()

def fetch_states(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    num_messages=df.shape[0]
    words=[]
    for message in df['message']:
        words.extend(message.split())

    num_media_messages = df[df['message'] == '<Media omitted>\n'].shape[0]
    links=[]
    for message in df['message']:
        links.extend(extract.find_urls(message))

    return num_messages,len(words),num_media_messages,len(links)

def most_busy_users(df):
    x=df['user'].value_counts().head()
    df=round((df['user'].value_counts()/df.shape[0])*100,2).reset_index().rename(columns={'index':'name','user':'percent'})
    return x,df

def create_wordcloud(selected_user, df):
        with open('stop_hinglish.txt', 'r') as f:
            stop_words = set(f.read().split())

        if selected_user != 'Overall':
            df = df[df['user'] == selected_user]

        if df.empty or df['message'].str.cat(sep=" ").strip() == "":
            return None

        temp = df[df['user'] != 'group_notification']
        temp = temp[temp['message'] != '<Media omitted>\n']

        temp['message'] = temp['message'].astype(str)

        text = temp['message'].str.cat(sep=" ")

        if not text.strip():
            return None

        wc = WordCloud(
            width=500,
            height=500,
            min_font_size=10,
            background_color='white',
            stopwords=stop_words
        )

        return wc.generate(text)

def remove_stop_words(message, stop_words):
        return " ".join(
            word for word in message.lower().split()
            if word not in stop_words
        )


# Updated snippet for helper.py
def most_common_words(selected_user, df):
    # Always specify encoding to avoid platform-specific errors
    with open('stop_hinglish.txt', 'r', encoding='utf-8') as f:
        stop_words = set(f.read().split())

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # Filter out junk messages early
    df = df[df['user'] != 'group_notification']
    df = df[df['message'] != '<Media omitted>\n']

    if df.empty:
        return pd.DataFrame() # Return empty DataFrame to avoid errors in app.py

    # Use list comprehension for better performance
    words = [word for message in df['message'] for word in message.lower().split() if word not in stop_words]
    
    return pd.DataFrame(Counter(words).most_common(25))

def emoji_helper(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    emojis = [c for message in df['message'] for c in message if c in emoji.EMOJI_DATA]
    
    emoji_counts = Counter(emojis).most_common()
    
    # Explicitly name the columns
    emoji_df = pd.DataFrame(emoji_counts, columns=['Emoji', 'Count'])
    return emoji_df

def monthly_timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    timeline=df.groupby(['year','month_num','month']).count()['message'].reset_index()

    time=[]
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i]+"-"+str(timeline['year'][i]))
    timeline['time']=time
    return timeline

def week_activity_map(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['day_name'].value_counts()

def month_activity_map(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['month'].value_counts()

def activity_heatmap(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    user_heatmap=df.pivot_table(index='day_name',columns='period',values='message',aggfunc='count').fillna(0)

    return user_heatmap
