# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests

st.title(":cup_with_straw Customize Your Smoothie :cup_with_straw:")
st.write("Choose the fruits you want in your custom Smoothie")

name_on_order = st.text_input('Name on Smoothie: ')
st.write('The name of your Smoothie will be: ', name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()
df = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))

ingredients_list = st.multiselect('Choose up to 5 ingredients: ', df, max_selections=5)

if ingredients_list:
    ingredients_string = ' '.join(ingredients_list)
    insert_stmt = f"""insert into smoothies.public.orders(ingredients, name_on_order)
values ('{ingredients_string}', '{name_on_order}')"""
    submit_order_button = st.button('Submit Order')
    if submit_order_button:
        session.sql(insert_stmt).collect()
        st.success(f"Your Smoothie is ordered, {name_on_order}")

fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
fv_df = st.dataframe(data=fruityvice_response.json(), use_container_width=True)
