# BizCardX
**📇EXTRACTING BUSSINESS CARD DATA WITH 'OCR'**

**Problem Statement:**

    You have been tasked with developing a Streamlit application that allows users to
    upload an image of a business card and extract relevant information from it using
    easyOCR. The extracted information should include the company name, card holder
    name, designation, mobile number, email address, website URL, area, city, state,
    and pin code. The extracted information should then be displayed in the application's
    graphical user interface (GUI).

    In addition, the application should allow users to save the extracted information into
    a database along with the uploaded business card image. The database should be
    able to store multiple entries, each with its own business card image and extracted
    information.
    
    To achieve this, you will need to use Python, Streamlit, easyOCR, and a database
    management system like SQLite or MySQL. The application should have a simple
    and intuitive user interface that guides users through the process of uploading the
    business card image and extracting its information. The extracted information should
    be displayed in a clean and organized manner, and users should be able to easily
    add it to the database with the click of a button. And Allow the user to Read the data,
    Update the data and Allow the user to delete the data through the streamlit UI
    This project will require skills in image processing, OCR, GUI development, and
    database management. It will also require you to carefully design and plan the
    application architecture to ensure that it is scalable, maintainable, and extensible.
    Good documentation and code organization will also be important for this project.

**Approach:**

    1. Install the required packages: 
        You will need to install Python, Streamlit,
        easyOCR, and a database management system like SQLite or MySQL.
    
    3. Design the user interface:
        Create a simple and intuitive user interface using
        Streamlit that guides users through the process of uploading the business
        card image and extracting its information. You can use widgets like file
        uploader, buttons, and text boxes to make the interface more interactive.
    
    4. Implement the image processing and OCR: 
        Use easyOCR to extract the
        relevant information from the uploaded business card image. You can use
        image processing techniques like resizing, cropping, and thresholding to
        enhance the image quality before passing it to the OCR engine.
    
    6. Display the extracted information:
        Once the information has been extracted,
        display it in a clean and organized manner in the Streamlit GUI. You can use
        widgets like tables, text boxes, and labels to present the information.
    
    8. Implement database integration: 
        Use a database management system like
        SQLite or MySQL to store the extracted information along with the uploaded
        business card image. You can use SQL queries to create tables, insert data,
        and retrieve data from the database, Update the data and Allow the user to
        delete the data through the streamlit UI
    
    10. Test the application: 
        Test the application thoroughly to ensure that it works as
        expected. You can run the application on your local machine by running the
        command streamlit run app.py in the terminal, where app.py is the name of
        your Streamlit application file.
    
    12. Improve the application:
        Continuously improve the application by adding new
        features, optimizing the code, and fixing bugs. You can also add user
        authentication and authorization to make the application more secure.



** Workflow**

    1. **Image Upload:**
        User uploads a business card image via a web or mobile application.
    
    2. **Image Preprocessing:**
        Improve the image quality for better OCR performance.
    
    3. **Text Extraction:**
        Use OCR to extract text and identify structured data fields.
    
    4. **Data Organization:**
        Categorize extracted data into specific fields using NLP algorithms.
    
    5. **Output:**
        Display data for user validation or directly save to a database, contact list, or CRM.

**Here Some of the Screenshots**
        
![Screenshot (112)](https://github.com/user-attachments/assets/df0fffe5-c10f-471c-8b30-89d7e6587da1)


![Screenshot (113)](https://github.com/user-attachments/assets/c024646b-af9d-47e1-be59-6806644d7b04)


![Screenshot (114)](https://github.com/user-attachments/assets/24b46ea6-f377-44f8-80f3-39d312e98f62)


![Screenshot (115)](https://github.com/user-attachments/assets/cebbcd0b-3654-4aa3-82b2-ce900d5f26fb)
