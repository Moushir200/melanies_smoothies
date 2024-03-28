# The file is stored under Stages and can be downloaded
# Document: https://docs.streamlit.io/library/api-reference/widgets/st.selectbox
# Payhon libraries: https://repo.anaconda.com/pkgs/snowflake/
# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
from snowflake.snowpark.context import get_active_session

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom Smoothie!
    """
)

# Add text box
name_on_order = st.text_input('Name of Smoothie')
st.write('The name of your Smooothie will be:', name_on_order)

# Add a select box
#option = st.selectbox(
#    'What is your favorite fruit?',
#    ('Banana', 'Srawberries', 'Peaches'))
#st.write('Your favorite fruit is:', option)

# Load data from database
session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('Fruit_Name'))
#st.dataframe(data=my_dataframe, use_container_width=True)

# Add the data to multiselect box
ingredients_list = st.multiselect(
    'Chosse up to 5  ingredients:',
    my_dataframe,
    max_selections =5
)
if ingredients_list:
    #st.write(ingredients_list)
    #st.text(ingredients_list)
    ingredients_string=''
    #Convert List to String
    for fruit_chosen in ingredients_list:
        ingredients_string+=fruit_chosen+' '
    #st.write(ingredients_string)

    # Build a SQL Insert Statement
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
                values ('""" + ingredients_string + """','"""+name_on_order+"""')"""
    st.write(my_insert_stmt)
    #st.stop()
    
    # Add Submit button
    time_to_interst=st.button('Submit Order')
    if time_to_interst:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")