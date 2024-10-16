# Import python packages
import streamlit as st
import requests
import pandas as pd
# from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw: ")
st.write(
    """Choose the fruits you want in your custom Smoothie!
    """
)


#option = st.selectbox(
#    "What is your favorite fruit?",
#    ("Banana", "Strawberries", "Peaches"),
#)

#st.write("Your favorite fruit is:", option)

name_on_order = st.text_input("Name on Smoothie: ")
st.write("The name of your smoothie will be: ", name_on_order)

cnx=st.connection("snowflake")
session =cnx.session()
# session = get_active_session()

my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))
#st.dataframe(data=my_dataframe, use_container_width=True)
#st.stop()


pd.df=my_dataframe.to_pandas()
#st.dataframe(pd.df)
#st.stop()
ingredient_list=st.multiselect(
    "Choose up to 5 ingredients",my_dataframe, max_selections=5
)
if ingredient_list:
    #st.write("You selected:", ingredient_list)
    #st.text( ingredient_list)

    ingredients_string=''
    for fruit_choosen in ingredient_list:
        ingredients_string += fruit_choosen +' '
        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        st.write('The search value for ', fruit_chosen,' is ', search_on, '.')
        st.subheader(fruit_choosen + ' Nutrition Information')
        fruityvice_response=requests.get("https://fruityvice.com/api/fruit/watermelon" + fruit_choosen)
        fv_df=st.dataframe(data=fruityvice_response.json(), use_container_width=True)
    #st.write(ingredients_string)
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,NAME_ON_ORDER)
            values ('""" + ingredients_string + """','"""+ name_on_order + """')"""

    #st.write(my_insert_stmt)
    #st.stop()
    time_to_insert=st.button('Submit_Order')
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered! '+ name_on_order, icon="✅")

