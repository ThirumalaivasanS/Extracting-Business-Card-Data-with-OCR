import pandas as pd
import streamlit as st
import easyocr
import mysql.connector as sql
from PIL import Image
import cv2
import os

os.environ['KMP_DUPLICATE_LIB_OK']='True'

# INITIALIZING THE EasyOCR READER
reader = easyocr.Reader(['en'])

# CONNECTING WITH MYSQL DATABASE
mydb = sql.connect(
    host="localhost",
    user="****",
    password="****",
    database="bizcardx_db"
)

mycursor = mydb.cursor(buffered=True)

# TABLE CREATION
mycursor.execute(
    "CREATE TABLE IF NOT EXISTS card_data ("
    "id INTEGER PRIMARY KEY AUTO_INCREMENT,"
    "company_name TEXT,"
    "card_holder TEXT,"
    "designation TEXT,"
    "mobile_number VARCHAR(50),"
    "email TEXT,"
    "website TEXT,"
    "area TEXT,"
    "city TEXT,"
    "state TEXT,"
    "pin_code VARCHAR(10),"
    "image LONGBLOB)"
)

# SETTING PAGE CONFIGURATIONS
st.set_page_config(page_title="BizCardX: Extracting Business Card Data with OCR",
                   layout="wide",
                   initial_sidebar_state="expanded",
                   )
st.markdown("BizCardX: Extracting Business Card Data with OCR", unsafe_allow_html=True)

selected_menu = st.sidebar.radio("Select an option", ("Upload & Extract","Modify"))

# UPLOAD AND EXTRACT MENU
if selected_menu == "Upload & Extract":
    st.markdown("### Upload a Business Card")
    uploaded_card = st.file_uploader("Upload an image of maximum size 10 MB", type=["png", "jpeg", "jpg"])
        
    if uploaded_card is not None:
        
        def save_card(uploaded_card):
            with open(os.path.join("uploaded_cards", uploaded_card.name), "wb") as f:
                f.write(uploaded_card.getbuffer())
                return

        save_card(uploaded_card)
        st.success("Image saved successfully!")
        
        # DISPLAYING UPLOADED IMAGE
        st.markdown("### Uploaded Image:")
        st.image(uploaded_card, use_column_width=True)

        # READING TEXT FROM IMAGE
        st.markdown("### Extracted Text:")
        img = cv2.imread(os.path.join("uploaded_cards", uploaded_card.name))
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = cv2.medianBlur(gray, 5)
        gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
        extracted_text = reader.readtext(gray, detail=0)

        # DISPLAYING EXTRACTED TEXT
        st.write(extracted_text)

        # SAVING DATA TO DATABASE
        if st.button("Save Data"):
            company_name, card_holder, designation, mobile_number, email, website, area, city, state, pin_code = None, None, None, None, None, None, None, None, None, None

            for text in extracted_text:
                if "company" in text.lower():
                    company_name = text
                if "name" in text.lower():
                    card_holder = text
                if "designation" in text.lower():
                    designation = text
                if "mobile" in text.lower() or "phone" in text.lower():
                    mobile_number = text
                if "email" in text.lower():
                    email = text
                if "website" in text.lower():
                    website = text
                if "area" in text.lower():
                    area = text
                if "city" in text.lower():
                    city = text
                if "state" in text.lower():
                    state = text
                if "pin" in text.lower() or "zip" in text.lower():
                    pin_code = text

            # INSERTING DATA INTO DATABASE
            try:
                with open(os.path.join("uploaded_cards", uploaded_card.name), "rb") as f:
                    image = f.read()

                mycursor.execute(
                    "INSERT INTO card_data (company_name, card_holder, designation, mobile_number, email, website, area, city, state, pin_code, image) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                    (company_name, card_holder, designation, mobile_number, email, website, area, city, state, pin_code, image)
                )
                mydb.commit()
                st.success("Data saved successfully!")
            except Exception as e:
                st.error(f"Error: {e}")

# MODIFY MENU
if selected_menu == "Modify":
    st.markdown("### Modify the Database")
    mycursor.execute("SELECT * FROM card_data")
    data = mycursor.fetchall()
    data = pd.DataFrame(data, columns=["ID", "Company Name", "Card Holder", "Designation", "Mobile Number", "Email", "Website", "Area", "City", "State", "Pin Code", "Image"])
    
    st.write(data)
    
    col1, col2 = st.columns(2)
    with col1:
        id = st.number_input("Enter the ID of the entry you want to modify", min_value=1)
        company_name = st.text_input("Enter the new Company Name")
        card_holder = st.text_input("Enter the new Card Holder Name")
        designation = st.text_input("Enter the new Designation")
        mobile_number = st.text_input("Enter the new Mobile Number")
        email = st.text_input("Enter the new Email")
        website = st.text_input("Enter the new Website URL")
    with col2:
        area = st.text_input("Enter the new Area")
        city = st.text_input("Enter the new City")
        state = st.text_input("Enter the new State")
        pin_code = st.text_input("Enter the new Pin Code")
        
    if st.button("Modify Data"):
      sql = "UPDATE card_data SET company_name=%s, card_holder=%s, designation=%s, mobile_number=%s, email=%s, website=%s, area=%s, city=%s, state=%s, pin_code=%s WHERE id=%s"
      val = (company_name, card_holder, designation, mobile_number, email, website, area, city, state, pin_code, id)
      mycursor.execute(sql, val)
      mydb.commit()
      st.success("Data modified successfully!")


