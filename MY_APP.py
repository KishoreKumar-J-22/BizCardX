import easyocr
import streamlit as st
from streamlit_option_menu import option_menu
from PIL import Image
import pandas as pd
import numpy as np
import re
import io
import psycopg2
import base64

def image_to_text(path):

    input_image = Image.open(path)

    # Converting Image to arry formAT
    image_arry = np.array(input_image)

    Reader = easyocr.Reader(['en'])
    Text = Reader.readtext(image_arry,detail=0)
    return Text, input_image

def extracted_text(texts):
    extracted_dict = {"Name":[],"Designation":[],"Company Name":[],"Contact":[],"E-Mail":[],"Website":[],
                      "Address":[],"Pincode":[]}
    
    extracted_dict["Name"].append(texts[0])
    extracted_dict["Designation"].append(texts[1])
    
    for i in range(2,len(texts)):
        
        if texts[i].startswith("+") or (texts[i].replace("-","").isdigit() and '-' in texts[i]):
            extracted_dict["Contact"].append(texts[i])

        elif "@" in texts[i] and ".com" in texts[i]:
            extracted_dict["E-Mail"].append(texts[i])
        
        elif "www" in texts[i] or "WWW" in texts[i] or "Www" in texts[i] or "wWw" in texts[i] or "wwW" in texts[i]:
            small_letter = texts[i].lower()
            extracted_dict["Website"].append(small_letter)

        elif "TamilNadu" in texts[i] or "Tamil Nadu" in texts[i] or texts[i].isdigit():
            extracted_dict["Pincode"].append(texts[i])

        elif re.match(r'^[A-Za-z]',texts[i]):
            extracted_dict["Company Name"].append(texts[i])

        else:
            remove_colon = re.sub(r',;','',texts[i])
            extracted_dict["Address"].append(texts[i])

    for key, value in extracted_dict.items():
        if len(value) > 0:
            concadenate = " ".join(value)
            extracted_dict[key] = [concadenate]
        
        else:
            value = "NA"
            extracted_dict[key] = [value]

    return extracted_dict



# Streamlit Part

st.set_page_config(layout = "wide", page_title = "Bizcard", page_icon = "📇")

st.markdown("""
    <h1 style="font-family: 'castellar', sans-serif; font-size: 36px; color: green;">
        📇EXTRACTING BUSSINESS CARD DATA WITH 'OCR'
    </h1>
""", unsafe_allow_html=True)
#st.title("EXTRACTING BUSSINESS CARD DATA WITH 'OCR'")


with st.sidebar:
    #select = option_menu("Main Menu",["Home","Upload And Modifying","Delete"])
    select = option_menu(
                        menu_title = "Manin Menu",
                        options = ["Home","Upload And Modifying","Delete"],
                        icons = ["house","book","trash"],
                        menu_icon = "cast",
                        default_index = 0
                        )

if select == "Home":
    st.markdown("""

        <h3 style="font-family: 'castellar', sans-serif; font-size: 30px; color: orange;">
            Technologies Used : <h4>Python,easy OCR, Streamlit, SQL, Pandas</h4>
        </h3>
                
    """, unsafe_allow_html=True)

    st.markdown("""

    <h3 style="font-family: 'castellar', sans-serif; font-size: 30px; color: orange;">
        About : <h4>Bizcard is a Python application designed to extract information from business cards.
                The main purpose of Bizcard is to automate the process of extracting key details from business card images, such as the name, 
                designation, company, contact information, and other relevant data. By leveraging the power of OCR (Optical Character Recognition) 
                provided by EasyOCR, Bizcard is able to extract text from the images.</h4>
    </h3>
    """, unsafe_allow_html=True)
    #st.write(
     #       "### :green[**About :**] Bizcard is a Python application designed to extract information from business cards.")

    #st.write(
           # '### The main purpose of Bizcard is to automate the process of extracting key details from business card images, such as the name, designation, company, contact information, and other relevant data. By leveraging the power of OCR (Optical Character Recognition) provided by EasyOCR, Bizcard is able to extract text from the images.')

elif select == "Upload And Modifying":
    st.markdown("""
                <h3 style="font-family: 'comic sans ms', sans-serif; font-size: 18px; color: orange;">
            Upload The Image Below :</h4>
        </h3>
    """, unsafe_allow_html=True)
    Image_open = st.file_uploader("",type = ["png","jpg","jpeg",])
    
    if Image_open is not None:
        st.image(Image_open,width= 400)

        text_image , input_image = image_to_text(Image_open)

        Text_dictionary = extracted_text(text_image)
        if Text_dictionary:
            st.success("TEXT IS EXTRACTED SUCCESSFULLY")

        df = pd.DataFrame(Text_dictionary)

        # Converting Image To Bytes

        Image_Bytes = io.BytesIO()
        input_image.save(Image_Bytes, format="PNG")

        image_data = Image_Bytes.getvalue()

        # Creating Dictionary
        data = {"Image":[image_data]}

        Data_Frame_1 = pd.DataFrame(data)

        concadenate_data_frame = pd.concat([df,Data_Frame_1], axis=1)
        st.dataframe(concadenate_data_frame)
        button_1 = st.button("Save", use_container_width=True)

        if button_1:
            # SQL connection

            my_database = psycopg2.connect(host = "localhost",
                                                user = "postgres",
                                                password = "admin123",
                                                database = "Biz-Card-X",
                                                port = "5432")
            cursor = my_database.cursor()
            # Table Creation

            create_table_query = '''CREATE TABLE IF NOT EXISTS bizcard_details (Name varchar(225),
                                                                            Designation varchar(225),
                                                                            Company_Name varchar(225),
                                                                            Contact varchar(225),
                                                                            Email varchar(225),
                                                                            Website text,
                                                                            Address text,
                                                                            Pincode varchar(225),
                                                                            Image text )'''

            cursor.execute(create_table_query)
            my_database.commit()

            # Check for duplicates
            check_query = '''SELECT * FROM bizcard_details 
                            WHERE Name = %s AND Designation = %s AND Company_Name = %s AND Contact = %s'''
            cursor.execute(check_query, (df.iloc[0]['Name'], df.iloc[0]['Designation'], df.iloc[0]['Company Name'], df.iloc[0]['Contact']))
            existing_data = cursor.fetchall()

            if existing_data:
                st.warning("Data already exists in the database!")
            else:
                # Insert Query
                insert_query = '''INSERT INTO bizcard_details (Name, Designation, Company_Name, Contact, Email, Website, Address, Pincode, Image)
                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)'''
                Datas = concadenate_data_frame.values.tolist()[0]
                cursor.execute(insert_query, Datas)
                my_database.commit()
                st.success("SAVED SUCCESSFULLY")
            # Insert Query

           # insert_query = '''INSERT INTO bizcard_details (Name, Designation, Company_name, Contact, Email, Website, Address, Pincode, Image)
                           # values(%s,%s,%s,%s,%s,%s,%s,%s,%s)'''

            #Datas = concadenate_data_frame.values.tolist()[0]
            #cursor.execute(insert_query,Datas)
            #my_database.commit()
            
            #st.success("SAVED SUCCESSFULLY")
    st.markdown("""
                <h3 style="font-family: 'comic sans ms', sans-serif; font-size: 18px; color: orange;">
            Select The Method Given Below
        </h3>
    """, unsafe_allow_html=True)
    method = st.radio("",["None","Preview","Modify"])
    if method == "None":
        st.write("")
    if method == "Preview":
        my_database = psycopg2.connect(host = "localhost",
                                                user = "postgres",
                                                password = "admin123",
                                                database = "Biz-Card-X",
                                                port = "5432")
        cursor = my_database.cursor()
        
        # Select query

        select_query = "SELECT * FROM bizcard_details"

        cursor.execute(select_query)
        table = cursor.fetchall()
        my_database.commit()

        table_df = pd.DataFrame(table,columns = ("NAME","DESIGNATION","COMPANY_NAME","CONTACT","EMAIL","WEBSITE","ADDRESS","PINCODE","IMAGE"))
        st.dataframe(table_df)

    elif method == "Modify":
        my_database = psycopg2.connect(host = "localhost",
                                                user = "postgres",
                                                password = "admin123",
                                                database = "Biz-Card-X",
                                                port = "5432")
        cursor = my_database.cursor()
        
        # Select query

        select_query = "SELECT * FROM bizcard_details"

        cursor.execute(select_query)
        table = cursor.fetchall()
        my_database.commit()

        table_df = pd.DataFrame(table,columns = ("NAME","DESIGNATION","COMPANY_NAME","CONTACT","EMAIL","WEBSITE","ADDRESS","PINCODE","IMAGE"))
        
        col_1,col_2 = st.columns(2)
        with col_1:
            
            selected_name = st.selectbox("Select the name",table_df["NAME"])

        df_3 = table_df[table_df["NAME"]==selected_name]
        
        df_4 = df_3.copy()

        

        col_1,col_2 = st.columns(2)
        with col_1:
            modify_name = st.text_input("Name",df_3["NAME"].unique()[0])
            modify_designation = st.text_input("Designation",df_3["DESIGNATION"].unique()[0])
            modify_company_name = st.text_input("Company_Name",df_3["COMPANY_NAME"].unique()[0])
            modify_contact = st.text_input("Contact",df_3["CONTACT"].unique()[0])
            modify_email = st.text_input("Email",df_3["EMAIL"].unique()[0])
            
            df_4["NAME"] = modify_name
            df_4["DESIGNATION"] = modify_designation
            df_4["COMPANY_NAME"] = modify_company_name
            df_4["CONTACT"] = modify_contact
            df_4["EMAIL"] = modify_email

        with col_2:
            modify_website = st.text_input("Website",df_3["WEBSITE"].unique()[0])
            modify_address = st.text_input("Address",df_3["ADDRESS"].unique()[0])
            modify_pincode = st.text_input("Pincode",df_3["PINCODE"].unique()[0])
            modify_image = st.text_input("Image",df_3["IMAGE"].unique()[0])

            df_4["WEBSITE"] = modify_website
            df_4["ADDRESS"] = modify_address
            df_4["PINCODE"] = modify_pincode
            df_4["IMAGE"] = modify_image

        st.dataframe(df_4)

        col_1,col_2 = st.columns(2)
        with col_1:
            button_3 = st.button("Save Changes", use_container_width = True)

            
        
        if button_3:
            my_database = psycopg2.connect(host = "localhost",
                                        user = "postgres",
                                        password = "admin123",
                                        database = "Biz-Card-X",
                                        port = "5432")
            cursor = my_database.cursor()

            cursor.execute(f"DELETE FROM bizcard_details WHERE NAME = '{selected_name}'")
            my_database.commit()

            # Check for duplicates
            check_query_1 = '''SELECT * FROM bizcard_details 
                            WHERE Name = %s AND Designation = %s AND Company_Name = %s'''
            cursor.execute(check_query_1, (df.iloc[0]['Name'], df.iloc[0]['Designation'], df.iloc[0]['Company Name']))
            existing_data = cursor.fetchall()

            if existing_data:
                st.warning("Data already exists in the database!")

            # Insert Query
            else:
                insert_query = '''INSERT INTO bizcard_details(Name, Designation, Company_name, Contact, Email, Website, Address, Pincode, Image)
                                values(%s,%s,%s,%s,%s,%s,%s,%s,%s)'''

                Datas = df_4.values.tolist()[0]
                cursor.execute(insert_query,Datas)
                my_database.commit()
                
                st.success("MODIFIED SUCCESSFULLY")

elif select == "Delete":
    my_database = psycopg2.connect(host = "localhost",
                                                user = "postgres",
                                                password = "admin123",
                                                database = "Biz-Card-X",
                                                port = "5432")
    cursor = my_database.cursor()

    col_1,col_2 = st.columns(2)
    with col_1:
    
        # Select query
        select_query_1 = "SELECT NAME FROM bizcard_details"

        cursor.execute(select_query_1)
        table_1 = cursor.fetchall()
        my_database.commit()

        names = []

        for i in table_1:
            names.append(i[0])
        st.markdown("<h4 style='text-align: left;font-family: Comic Sans MS;font-size: 18px; color: orange;'>Select The Name</h4>",unsafe_allow_html=True)
        name_select = st.selectbox("",names)

    with col_2:
    
        # Select query
        select_query_2 = f"SELECT DESIGNATION FROM bizcard_details WHERE NAME = '{name_select}'"

        cursor.execute(select_query_2)
        table_2 = cursor.fetchall()
        my_database.commit()

        designations = []

        for i in table_2:
            designations.append(i[0])
        st.markdown("<h4 style='text-align: left;font-family: Comic Sans MS;font-size: 18px; color: orange;'>Select The Designation</h4>",unsafe_allow_html=True)
        designation_select = st.selectbox("",designations)
    
    if name_select and designation_select:
        col_1,col_2,col_3 = st.columns(3)

        with col_1:
            st.markdown("<h4 style='text-align: left;font-family: Comic Sans MS;font-size: 15px; color: orange;'>Selected Name :</h4>",unsafe_allow_html=True)
            st.write(f"{name_select}")
            #st.write(" ")
            #st.write(" ")
            #st.write(" ")
            st.markdown("<h4 style='text-align: left;font-family: Comic Sans MS;font-size: 15px; color: orange;'>Selected Designation :</h4>",unsafe_allow_html=True)
            st.write(f"{designation_select}")

        with col_2:
            st.write(" ")
            st.write(" ")
            st.write(" ")
            st.write(" ")
            st.write(" ")
            st.write(" ")
            st.write(" ")
            st.write(" ")
            st.write(" ")
            st.write(" ")
            st.write(" ")
            
            remove = st.button("Delete",use_container_width=True)

            if remove:

                cursor.execute(f"DELETE FROM bizcard_details WHERE NAME = '{name_select}' AND DESIGNATION = '{designation_select}'")
                my_database.commit()

                st.warning("DELETED")