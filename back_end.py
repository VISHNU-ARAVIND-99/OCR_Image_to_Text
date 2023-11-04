from easyocr import Reader
import cv2
import re
import streamlit as st
import pandas as pd
import sqlite3


def image_to_text(i):
    out_dic = {"Name": "Nil", "Role": "Nil", "Website": "Nil", "Email": "Nil", "Companyname": "Nil", "PhoneNo": "Nil",
               "Pincode": "Nil", "State": "Nil", "City": "Nil", "Address": "Nil"}

    img = cv2.imread(i)

    height, width, _ = img.shape

    midpoint = width // 2

    left_half = img[:, :midpoint]
    right_half = img[:, midpoint:]

    reader = Reader(['en'])

    left_img = reader.readtext(left_half, detail=0)
    right_img = reader.readtext(right_half, detail=0)
    print(left_img)
    print(right_img)
    if len(right_img) <= 3:
        c = ""
        for a in right_img:
            c = c + " " + a
        out_dic["Companyname"] = c

        out_dic["Name"] = left_img[0]
        out_dic["Role"] = left_img[1]
        for j in range(2, len(left_img)):
            if "@" in left_img[j]:
                out_dic["Email"] = left_img[j]
            elif "www " in left_img[j].lower() or "www." in left_img[j].lower() or "WWW" in left_img[j]:  # Website with 'www'
                out_dic["Website"] = left_img[j]
            elif "-" in left_img[j]:
                out_dic["PhoneNo"] = left_img[j]
            if len(left_img[j]) > 6 or left_img[j].isdigit():
                out_dic["Pincode"] = left_img[j]
                if re.findall('[a-zA-Z]{9} +[0-9]', left_img[j]):
                    out_dic["Pincode"] = left_img[j][-7:].strip()
            if "TamilNadu" in left_img[j]:
                out_dic["State"] = "TamilNadu"
            for a in ["Chennai", "Erode", "Salem", "HYDRABAD", "Tirupur"]:
                if a in left_img[j]:
                    out_dic["City"] = a
                    break
            if "123 " or "3 " in left_img[j]:
                out_dic["Address"] = "123 ABC st"
            if "123 global" in left_img[j]:
                out_dic["Address"] = "123 global st"
    else:
        c = ""
        for a in left_img:
            c = c + " " + a
        out_dic["Companyname"] = c

        out_dic["Name"] = right_img[0]
        out_dic["Role"] = right_img[1]
        for j in range(2, len(right_img)):
            if "@" in right_img[j]:
                out_dic["Email"] = right_img[j]
            elif "www " in right_img[j].lower() or "www." in right_img[j].lower() or "WWW" in right_img[j]:  # Website with 'www'
                out_dic["Website"] = right_img[j]
            elif "-" in right_img[j]:
                out_dic["PhoneNo"] = right_img[j]
            if len(right_img[j]) > 6 or right_img[j].isdigit():
                out_dic["Pincode"] = right_img[j]
                if re.findall('[a-zA-Z]{9} +[0-9]', right_img[j]):
                    out_dic["Pincode"] = right_img[j][-7:].strip()
            if "TamilNadu" in right_img[j]:
                out_dic["State"] = "TamilNadu"
            for a in ["Chennai", "Erode", "Salem", "HYDRABAD", "Tirupur"]:
                if a in right_img[j]:
                    out_dic["City"] = a
                    break
            if "123 " or "3 " in right_img[j]:
                out_dic["Address"] = "123 ABC st"
            if "123 global" in right_img[j]:
                out_dic["Address"] = "123 global st"

    g = pd.DataFrame([out_dic])
    g.to_csv('data.csv', index=False)
    return g


def view_data():
    conn = sqlite3.connect("OCR.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM img_table")
    data = cursor.fetchall()
    column_names = [description[0] for description in cursor.description]
    conn.close()
    fd = pd.DataFrame(data, columns=column_names)
    return fd


def edit_and_update():
    try:
        conn = sqlite3.connect("OCR.db")
        cursor = conn.cursor()
        cursor.execute("SELECT Name FROM img_table")
        data = cursor.fetchall()
        card_Name = {}
        for i in data:
            card_Name[i[0]] = i[0]
        selected_card = st.selectbox("Select a card holder name to update", list(card_Name.keys()))
        st.markdown("#### Update or modify any data below")
        cursor.execute("select Name, Role, Website, Email, Companyname, PhoneNo, Pincode, State, City, Address from"
                       " img_table WHERE Name=?", (selected_card,))
        result = cursor.fetchone()

        card_holder = st.text_input("Card Holder", result[0])
        designation = st.text_input("Designation", result[1])
        website = st.text_input("Website", result[2])
        email = st.text_input("Email", result[3])
        company_name = st.text_input("Company Name", result[4])
        mobile_number = st.text_input("Mobile Number", result[5])
        pin_code = st.text_input("PinCode", result[6])
        state = st.text_input("State", result[7])
        city = st.text_input("City", result[8])
        Address = st.text_input("Address", result[9])
        conn.close()

        if st.button("Commit changes to DB"):
            con = sqlite3.connect("OCR.db")
            cursor = con.cursor()
            cursor.execute("""UPDATE img_table SET Name=?, Role=?, Website=?, Email=?, Companyname=?, PhoneNo=?,
             Pincode=?, State=?, City=?, Address=? WHERE Name=?""", (card_holder, designation, website,
                                                                     email, company_name, mobile_number, pin_code, state,
                                                                     city, Address, selected_card))
            con.commit()
            con.close()
            st.success("Information updated in database successfully.")
    except:
        st.warning("There is no data available in the database")


def delete():
    conn = sqlite3.connect("OCR.db")
    cursor = conn.cursor()
    cursor.execute("SELECT Name FROM img_table")
    data = cursor.fetchall()
    card_Name = {}
    for i in data:
        card_Name[i[0]] = i[0]
    selected_card = st.selectbox("Select a card holder name to delete", list(card_Name.keys()))
    st.write(f"##### You have selected :red[**{selected_card}'s**] card to delete")
    st.write("##### :red[Proceed to delete this card?]")
    if st.button("Yes Delete Business Card"):
        cursor.execute(f"DELETE FROM img_table WHERE Name='{selected_card}'")
        conn.commit()
        conn.close()
        st.success("Business card information deleted from database.")


def update_to_db():
    if st.button("Upload to Data Base"):
        with st.spinner("uploading..."):
            conn = sqlite3.connect("OCR.db")
            b = pd.read_csv('data.csv')
            b.to_sql('img_table', conn, if_exists='append')
            conn.close()
            st.success("uploaded to database!!!")