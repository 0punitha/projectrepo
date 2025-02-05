import streamlit as st
from mysql.connector import connection
from PIL import Image, ImageDraw, ImageFont
import io

# Database connection
con = connection.MySQLConnection(
    user='root',
    password='root',
    host='127.0.0.1',
    database='child_details'
)
mycursor = con.cursor()

st.title("Brth certificate")

# Sidebar options
option = st.sidebar.selectbox("Select an operation", ("Create", "Update", "View", "Delete", "Generate Certificate"))

# Certificate generation function
def generate_certificate(data):
    """
    Generate a certificate using Pillow with the provided data.

    Args:
        data (tuple): A tuple containing the data for certificate generation.

    Returns:
        BytesIO: BytesIO object of the generated certificate image.
    """
    template_path = r"C:\\Users\\MATRIX\\Downloads\\template (2).jpg"
    output = io.BytesIO()

    image = Image.open(template_path)
    draw = ImageDraw.Draw(image)

    font_path = r"C:\\Windows\\Fonts\\arial.ttf"
    font = ImageFont.truetype(font_path, 40)

    draw.text((250, 200), f"ID: {data[0]}", font=font, fill="black")
    draw.text((250, 250), f"Baby Name: {data[1]}", font=font, fill="black")
    draw.text((250, 300), f"Father's Name: {data[2]}", font=font, fill="black")
    draw.text((250, 350), f"Mother's Name: {data[3]}", font=font, fill="black")
    draw.text((250, 400), f"Date of Birth: {data[4]}", font=font, fill="black")
    draw.text((250, 450), f"Birth Time: {data[5]}", font=font, fill="black")
    draw.text((250, 500), f"City: {data[6]}", font=font, fill="black")
    draw.text((250, 550), f"Gender: {data[7]}", font=font, fill="black")

    image.save(output, format="JPEG")
    output.seek(0)
    return output

if option == "Create":
    st.subheader("Create a Record")
    Id = st.number_input("Enter the ID: ", min_value=1)
    Baby_Fullname = st.text_input("Enter the Baby's Full Name: ")
    Father_name = st.text_input("Enter the Father's Name: ")
    Mother_name = st.text_input("Enter the Mother's Name: ")
    Date_of_Birth = st.date_input("Enter the Baby's Date of Birth:")
    Time = st.time_input("Enter the Birth Time:")
    City = st.text_input("Enter the Baby's Native Place: ")
    baby_gender = st.selectbox("Select the Baby's Gender:", ["Male", "Female", "Other"])
    if st.button("Create"):
        sql = """
            INSERT INTO baby_information 
            (Id, Baby_Fullname, Father_name, Mother_name, Date_of_Birth, Time, City, baby_gender) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        user = (Id, Baby_Fullname, Father_name, Mother_name, Date_of_Birth, Time, City, baby_gender)
        mycursor.execute(sql, user)
        con.commit()
        st.success("Record created successfully!")

if option == "Update":
    st.subheader("Update a Record")
    Id = st.number_input("Enter the ID: ", min_value=1)
    Baby_Fullname = st.text_input("Enter the Baby's Full Name: ")
    Father_name = st.text_input("Enter the Father's Name: ")
    Mother_name = st.text_input("Enter the Mother's Name: ")
    Date_of_Birth = st.date_input("Enter the Baby's Date of Birth:")
    Time = st.time_input("Enter the Birth Time:")
    City = st.text_input("Enter the Baby's Native Place: ")
    baby_gender = st.selectbox("Select the Baby's Gender:", ["Male", "Female", "Other"])
    if st.button("Update"):
        sql = """
            UPDATE baby_information 
            SET Baby_Fullname=%s, Father_name=%s, Mother_name=%s, Date_of_Birth=%s, Time=%s, City=%s, baby_gender=%s 
            WHERE Id=%s
        """
        user = (Baby_Fullname, Father_name, Mother_name, Date_of_Birth, Time, City, baby_gender, Id)
        mycursor.execute(sql, user)
        con.commit()
        st.success("Record updated successfully!")

if option == "View":
    st.subheader("View All Records")
    sql = """
        SELECT Id, Baby_Fullname, Father_name, Mother_name, Date_of_Birth, Time, City, baby_gender 
        FROM baby_information
    """
    mycursor.execute(sql)
    result = mycursor.fetchall()
    if result:
        st.table(result)
    else:
        st.warning("No records found.")

if option == "Delete":
    st.subheader("Delete a Record")
    Id = st.number_input("Enter the ID: ", min_value=1)
    if st.button("Delete"):
        sql = "DELETE FROM baby_information WHERE Id=%s"
        user = (Id,)
        mycursor.execute(sql, user)
        con.commit()
        st.success("Record deleted successfully!")

if option == "Generate Certificate":
    st.subheader("Generate a Certificate")
    sql = """
        SELECT Id, Baby_Fullname, Father_name, Mother_name, Date_of_Birth, Time, City, baby_gender 
        FROM baby_information
    """
    mycursor.execute(sql)
    result = mycursor.fetchall()
    if result:
        selected_id = st.selectbox("Select an ID", [row[0] for row in result])
        record = next((row for row in result if row[0] == selected_id), None)
        if record:
            if st.button("Generate Certificate"):
                cert_image = generate_certificate(record)
                st.image(cert_image, caption="Generated Certificate")
                st.download_button(
                    label="Download Certificate",
                    data=cert_image,
                    file_name=f"certificate_{record[0]}.jpg",
                    mime="image/jpeg"
                )
    else:
        st.warning("No records found.")
