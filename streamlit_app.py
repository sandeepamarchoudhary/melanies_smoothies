# Import python packages
import streamlit as st
import requests
import pandas as pd
# from snowflake.snowpark.context import get_active_session 
from snowflake.snowpark.functions import col
# import get_active_session as active

# Write directly to the app
st.title("Customize Your Smoothis!:cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom smoothis.
    """
)
# option = st.selectbox(
#     'What is in your favourite fruit?',
#     ('Banana', 'Strawberries', 'Peaches'))

# st.write('You selected:', option)

name_of_order = st.text_input('Name Of The Smoothie:')
st.write('The name of your smoothie ', name_of_order)


cnx = st.connection('snowflake')
session = cnx.session()
# session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))
# st.dataframe(data=my_dataframe, use_container_width=True)

#convert snowfark data frame to pandas dataframe
pd_df = my_dataframe.to_pandas()
# st.dataframe(pd_df)
# st.stop()

ingredients_list = st.multiselect('Choose upto 5 ingredients',my_dataframe,max_selections = 5)

if ingredients_list:
    # st.write(ingredients_list)
    # st.text(ingredients_list)
    ingredients_string=''
    for each_fruit in ingredients_list:
        ingredients_string += each_fruit+' '
        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == each_fruit, 'SEARCH_ON'].iloc[0]
        # st.write('The search value for ', each_fruit,' is ', search_on, '.')
        st.subheader(each_fruit +' Nutrition Information!')
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+ search_on)
        # st.text(fruityvice_response.json()
        fv_df = st.dataframe(data = fruityvice_response.json(), use_container_width = True)
        
    # st.write(ingredients_string)
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
                values ('""" + ingredients_string + """','"""+name_of_order+"""')"""
    # st.write(my_insert_stmt)
    # st.stop()
    time_to_insert = st.button('Submit Order')
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")




