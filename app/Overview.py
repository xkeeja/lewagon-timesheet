import streamlit as st
import datetime
from calendar import monthrange
import pandas as pd
import gspread


st.set_page_config(
    page_title='Overview',
    layout='wide'
)


st.markdown('# Overview')

# insert line spacer
st.markdown('***')


# define functions
# @st.cache_data
def load_df_from_gsheet():
    gc = gspread.service_account_from_dict(st.secrets.service_account)
    sh = gc.open_by_key(st.secrets.sheet.sheet_key)
    df = pd.DataFrame(sh.sheet1.get_all_records())
    df['Date'] = pd.to_datetime(df['Date']).dt.date
    return df


# load df
df = load_df_from_gsheet()


# set start date & end dates
a, b = st.columns(2)
with a:
    d_start = st.date_input("Start Date", datetime.date(2023, 1, 1))

with b:
    d_end = st.date_input("End Date", datetime.date.today())


# choose location
loc = st.selectbox('Location', df.Location.unique())


# insert line spacer
st.markdown('***')


# filter df to chosen start & end dates
df_interval = df[(df.Date >= d_start) & (df.Date <= d_end) & (df.Location == loc)].sort_values(by=['Date'])
df_interval.set_index('Date', inplace=True)


# metrics
## as lead
st.markdown('As Lead:')
full, half, other, _ = st.columns(4)
with full:
    st.metric('Full', len(df_interval[(df_interval.Position == 'Lead') & (df_interval.Length == 'Full')]))

with half:
    st.metric('Half', len(df_interval[(df_interval.Position == 'Lead') & (df_interval.Length == 'Half')]))

with other:
    st.metric('Other', len(df_interval[(df_interval.Position == 'Lead') & (df_interval.Length == 'Other')]))

## as TA
st.markdown('As TA:')
full, full_proj, half, other = st.columns(4)
with full:
    st.metric('Full', len(df_interval[(df_interval.Position == 'TA') & (df_interval.Length == 'Full') & (df_interval.Topic != 'Project')]))

with full_proj:
    st.metric('Full Project', len(df_interval[(df_interval.Position == 'TA') & (df_interval.Length == 'Full') & (df_interval.Topic == 'Project')]))

with half:
    st.metric('Half', len(df_interval[(df_interval.Position == 'TA') & (df_interval.Length == 'Half')]))

with other:
    st.metric('Other', len(df_interval[(df_interval.Position == 'TA') & (df_interval.Length == 'Other')]))


# show dataframe
st.dataframe(df_interval, use_container_width=True)
