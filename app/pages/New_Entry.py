import streamlit as st
import datetime
import pandas as pd
import gspread

st.set_page_config(
        page_title='New Entry',
        layout='wide'
)

st.markdown('# New Entry')


with st.form("my_form", clear_on_submit=True):
   # set date as today
   d = st.date_input("Date", datetime.date.today())

   # calculate day of the week
   dow_idx = d.weekday()
   dow_dict = {
           0: 'Mon',
           1: 'Tue',
           2: 'Wed',
           3: 'Thu',
           4: 'Fri',
           5: 'Sat',
           6: 'Sun',
   }
   dow = dow_dict[dow_idx]

   # position
   pos = st.radio('Position', (
            'Lead',
            'TA'
            ))

   # length of session
   length = st.radio('Length of Session', (
           'Full',
           'Half',
           'Other',
           ))

   # bootcamp
   camp = st.text_input('Bootcamp', '')

   # location
   loc = st.text_input('Location', '')

   # topic
   topic = st.text_input('Topic of the session', '')

   # every form must have a submit button.
   submitted = st.form_submit_button("Submit")
   if submitted:
        success = st.empty()
        with st.spinner('⏳ Writing entry...'):
                # df for new entry
                columns = ['Date', 'Day', 'Position', 'Length', 'Bootcamp', 'Location', 'Topic']
                new_entry = [str(d), dow, pos, length, camp, loc, topic]
                df = pd.DataFrame(dict(zip(columns, new_entry)), index=[0])
                st.dataframe(df, use_container_width=True)

                # load gsheet & write new entry
                gc = gspread.service_account_from_dict(st.secrets.service_account)
                sh = gc.open_by_key(st.secrets.sheet.sheet_key)
                worksheet = sh.sheet1
                index = len(worksheet.col_values(1)) + 1
                worksheet.update(f'A{index}', [new_entry])
        success.success('Entry updated!', icon='✅')
