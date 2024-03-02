import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
#-----------------------------------------------------------------------------------------
import re
import pandas as pd
import helper


def preprocess(data):
   # data = """
#["09/10/23, 9:50pm - Messages and calls are end-to-end encrypted. No one outside of this chat, not even WhatsApp, can read or listen to them. Tap to learn more.16/10/23, 12:29pm - ram: ramt=pLmVs2N1u9UgEPUYqS-LCA&s=08Follow and share with ur frnds if u find the content useful, Started 1 month back,  posted more than 100 job updates.16/10/23, 12:44pm - vig: Nice pa16/10/23, 12:44pm - vig: I will share16/10/23, 12:46pm - vig: Status updated🤝16/10/23, 12:46pm - ram: Bro status don't keep, normally u share in whatsapp16/10/23, 12:46pm - vig: You shared to our class people!?16/10/23, 12:47pm - ram: 5 to 6 key people who r having their frnd circle16/10/23, 12:47pm - vig: Nice16/10/23, 12:47pm - vig: Ok13/12/23, 7:57pm - vig: Beo13/12/23, 7:57pm - vig: Hw r u?13/12/23, 7:57pm - vig: Did not see u in clg past 3 days13/12/23, 8:44pm - ram: Fyn bro, how r u13/12/23, 8:44pm - ram: Monday my birthday so I was in home13/12/23, 8:44pm - ram: Tuesday also13/12/23, 8:44pm - ram: Today back to bangalore but have to go to office13/12/23, 8:44pm - ram: Tomorrow will try to come13/12/23, 10:24pm - vig: I am doing well13/12/23, 10:24pm - vig: Ohh belated happy b'day bro13/12/23, 10:25pm - vig: Aie hye🥲13/12/23, 10:25pm - vig: Ok bro14/12/23, 10:46am - vig: Bro14/12/23, 10:46am - vig: Send me exam schedule if u hv14/12/23, 10:47am - ram: <Media omitted>14/12/23, 10:50am - vig: Thnx bro15/12/23, 11:35am - ram: Congratulations bro15/12/23, 11:35am - ram: Happy for u15/12/23, 11:35am - ram: What the ctc15/12/23, 11:35am - ram: And base15/12/23, 11:35am - vig: Thanks bro😁15/12/23, 11:36am - vig: 5 to 7 they told not decided28/12/23, 12:35pm - ram: <Media omitted>28/12/23, 12:41pm - vig: \\bbooks?\\b\\bcolor\\.?\\b^\\d+(\\.\\d+)?$^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$\\b(?:[Mm][Hh]z|{Mm}ega[Hh]ertz)\\b16/01/24, 12:28am - vig: Broo16/01/24, 12:29am - vig: D E Shaw form how did u fill?16/01/24, 12:29am - ram: Open in edge16/01/24, 12:29am - ram: Place textbox and fill16/01/24, 12:29am - vig: Ohhhh16/01/24, 12:29am - ram: I did like that16/01/24, 12:29am - vig: Syk bro16/01/24, 12:30am - vig: Thnx yaar16/01/24, 12:30am - ram: If u get any coding question try sending bro in exam16/01/24, 12:30am - vig: Hehe sure broo26/01/24, 10:43pm - """
    date_pattern = r'\d{2}/\d{2}/\d{2}, \d{1,2}:\d{2}[ap]m'
    dates = re.findall(date_pattern, data)
    messages = re.split(date_pattern, data)[1:]
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
    
    df['user'] = users
    df['message'] = messages
    df.drop(columns=['Message', 'Date'], inplace=True)
    
    df['only_date'] = df['date'].dt.date
    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute
    
    period = []
    for hour in df['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))
    df['period'] = period
    
    return df


#-----------------------------------------------------------------------------------------------------
st.title("Whatsapp Chat Analyzer")

st.sidebar.title("Whatsapp Chat Analyzer")
st.write("Click on the Sidebar and upload your whatsapp chat and get an instant chat analysis")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocess(data)
    print(df)
    st.dataframe(df)
    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0,"Overall")
    selected_user = st.sidebar.selectbox("Show analysis wrt",user_list)
    if st.sidebar.button("Show Analysis"):
        # Stats Area
        num_messages, words, num_media_messages, num_links = helper.fetch_stats(selected_user,df)
        st.title("Top Statistics")
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header("Total Messages")
            st.title(num_messages)
        with col2:
            st.header("Total Words")
            st.title(words)
        with col3:
            st.header("Media Shared")
            st.title(num_media_messages)
        with col4:
            st.header("Links Shared")
            st.title(num_links)

         # monthly timeline
        st.title("Monthly Timeline")
        timeline = helper.monthly_timeline(selected_user,df)
        fig,ax = plt.subplots()
        ax.plot(timeline['time'], timeline['message'],color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # daily timeline
        st.title("Daily Timeline")
        daily_timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='black')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # activity map
        st.title('Activity Map')
        col1,col2 = st.columns(2)

        with col1:
            st.header("Most busy day")
            busy_day = helper.week_activity_map(selected_user,df)
            fig,ax = plt.subplots()
            ax.bar(busy_day.index,busy_day.values,color='purple')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.header("Most busy month")
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values,color='orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        st.title("Weekly Activity Map")
        user_heatmap = helper.activity_heatmap(selected_user,df)
        fig,ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)

        if selected_user == 'Overall':
            st.title('Most Busy Users')
            x,new_df = helper.most_busy_users(df)
            fig, ax = plt.subplots()

            col1, col2 = st.columns(2)

            with col1:
                ax.bar(x.index, x.values,color='red')
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)
        
         # WordCloud
        st.title("Wordcloud")
        df_wc = helper.create_wordcloud(selected_user,df)
        fig,ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        # most common words
        most_common_df = helper.most_common_words(selected_user,df)
        fig,ax = plt.subplots()
        ax.barh(most_common_df[0],most_common_df[1])
        st.title('Most commmon words')
        st.pyplot(fig)
        
        # emoji analysis
        emoji_df = helper.emoji_helper(selected_user,df)
        st.title("Emoji Analysis")
        col1,col2 = st.columns(2)
        with col1:
            st.dataframe(emoji_df)
        with col2:
            fig,ax = plt.subplots()
            ax.pie(emoji_df[1].head(),labels=emoji_df[0].head(),autopct="%0.2f")
            st.pyplot(fig)