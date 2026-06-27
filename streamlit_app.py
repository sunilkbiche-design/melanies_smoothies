import streamlit as st
# New section to display smoothiefruit nutrition information

import requests

smoothiefruit_response = requests.get(
    "https://my.smoothiefroot.com/api/fruit/watermelon"
)

# st.text(smoothiefruit_response.json())

sf_df = st.dataframe(
    data=smoothiefruit_response.json(),
    use_container_width=True
)

from snowflake.snowpark.functions import col

# -------------------------------------------------------
# Title
# -------------------------------------------------------

st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")

st.write("Choose the fruits you want in your custom Smoothie!")

# -------------------------------------------------------
# Customer Name
# -------------------------------------------------------

name_on_order = st.text_input("Name on Smoothie:")

st.write("The name on your Smoothie will be:", name_on_order)

# -------------------------------------------------------
# Connect to Snowflake
# -------------------------------------------------------

cnx = st.connection("snowflake")
session = cnx.session()

# -------------------------------------------------------
# Read Fruit Options
# -------------------------------------------------------

my_dataframe = (
    session.table("smoothies.public.fruit_options")
    .select(col("FRUIT_NAME"))
)

fruit_list = my_dataframe.to_pandas()["FRUIT_NAME"].tolist()

# -------------------------------------------------------
# Fruit Selection
# -------------------------------------------------------

ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:",
    fruit_list,
    max_selections=5
)

# -------------------------------------------------------
# Build Ingredient String
# -------------------------------------------------------

if ingredients_list:

    ingredients_string = ", ".join(ingredients_list)

    st.write("Your ingredients are:")

    st.write(ingredients_string)

# -------------------------------------------------------
# Submit Order
# -------------------------------------------------------

time_to_insert = st.button("Submit Order")

if time_to_insert:

    if name_on_order == "":

        st.warning("Please enter your name.")

    elif len(ingredients_list) == 0:

        st.warning("Please choose at least one ingredient.")

    else:

        insert_sql = f"""
        INSERT INTO smoothies.public.orders
        (ingredients, name_on_order)
        VALUES
        ('{ingredients_string}', '{name_on_order}')
        """

        session.sql(insert_sql).collect()

        st.success("Your Smoothie is ordered!", icon="🥤")
