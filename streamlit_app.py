# Import python packages
import requests
import streamlit as st
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(f":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write("""\
    Choose the fruits you want in your custom Smoothie!
""")

cnx = st.connection("snowflake")
session = cnx.session()

name = st.text_input('Name on Smoothie')
st.write(f'The name on your Smoothie will be: {name}')

fruit_df = session.table('smoothies.public.fruit_options').select(col('fruit_name'))
chosen_ingredients = st.multiselect(
    label='Choose up to 5 ingredients:',
    options=fruit_df,
    max_selections=5,
)

smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
st.text(smoothiefroot_response.json())

if all([chosen_ingredients, name, st.button('Submit Order')]):
    ingredients = ' '.join(chosen_ingredients)
    statement = f"""
        insert into smoothies.public.orders
            (ingredients, name_on_order) 
        values 
            ('{ingredients}', '{name}')
        """
    session.sql(statement).collect()
    st.success('Your Smoothie is ordered!', icon="✅")
