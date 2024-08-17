# Import python packages
import streamlit as st
# from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

cnx = st.connection('snowflake')
session = cnx.session()

# Write directly to the app
st.title("Customize Your Smoothie!")
st.write(
    """Choose the fruits you want in your smoothie.
    """
)

# Get the current credentials


my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
# st.dataframe(data=my_dataframe, use_container_width=True)

# option = st.selectbox("How would you like to be contacted.",
#                       ('Email','Home Phone', 'Mobile Phone'))

# option = st.selectbox("What is favorite fruit?.",
#                       ('Banana','Strawberries', 'Peachs'))

# st.write('Your favorite fruite is '+ option)

name = st.text_input("Name on smoothie")
# st.write(name)

ilist = st.multiselect('Choose my ingredients: ', my_dataframe, max_selections = 5)


if ilist:
    str_ilist = ''
    for i in ilist:
        str_ilist = str_ilist + i + ' '
    # st.write(str_ilist)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + str_ilist + """', '""" + name + """')"""
    # st.write(my_insert_stmt)
    btn = st.button("Submit")
    if btn:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")
