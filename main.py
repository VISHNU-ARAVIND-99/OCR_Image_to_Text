import streamlit as st
import pandas as pd
import back_end as bd


st.set_page_config(layout="wide")

st.title(":blue[Extracting Business Card Data with OCR]")
st.markdown(":blue[This is a web app allow to Extract text from Business Card Image.]")

st.sidebar.title("Navigation")
side_bar_object = st.sidebar.radio("Pages", options=["About", "Convert To Text", "Upload To OR View DB", "Edit or Delete The DB"])

if side_bar_object == "About":
    st.subheader(":green[About:]")
    st.markdown("A Streamlit application that allows users to upload an image of a business card and extract relevant "
                "information from it using OCR. This application would also allow users to save the extracted "
                "information into a database along with the uploaded business card image.")

if side_bar_object == "Convert To Text":
    col1, col2, col3 = st.columns([3, 3, 2])
    col2.markdown("### :green[Convert To Text]")
    st.write("")
    st.write("Upload a Business Card Image in png/jpeg/jpg")
    uploaded_file = st.file_uploader("Choose a Business Card Image", label_visibility="collapsed",
                                     type=["png", "jpeg", "jpg"])
    if uploaded_file is not None:
        save_path = "D:\Data science\Projects\OCR\saved_img.png"
        with open(save_path, "wb") as f:
            f.write(uploaded_file.read())

        col1, col2 = st.columns(2, gap="large")
        with col1:
            st.markdown("### You have uploaded the card")
            st.image("saved_img.png")

        if st.button("Convert to Text"):
            with st.spinner("Converting..."):
                st.dataframe(bd.image_to_text(i="saved_img.png"))
            st.success("Converted to Text!!!")


if side_bar_object == "Upload To OR View DB":
    col1, col2, col3 = st.columns([3, 3, 2])
    col2.markdown("### :green[Upload to OR View DB]")
    column1, column2 = st.columns(2, gap="large")
    with column1:
        try:
         st.image("saved_img.png")
         st.markdown("### Data ready to upload")
         b = pd.read_csv('data.csv')
         st.dataframe(b)
        except:
            st.warning("plz first convert to text")

        bd.update_to_db()
    with column2:
        st.markdown("View the table of DB data below")
        st.write(bd.view_data())

if side_bar_object == "Edit or Delete The DB":
    col1, col2, col3 = st.columns([3, 3, 2])
    col2.markdown("### :green[Edit or Delete The DB]")
    column1, column2 = st.columns(2, gap="large")
    with column1:
        bd.edit_and_update()
    with column2:
        bd.delete()
        st.markdown("View the table of DB data below")
        st.write(bd.view_data())



