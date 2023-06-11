
# BizCardX: Extracting Business Card Data with OCR

BizCardX is a simple Python application that extracts text from uploaded business card images using the EasyOCR library and saves the extracted data to a MySQL database. This application can be used to easily digitize business cards and maintain a database of important contact information.





## Prerequisites
To run this project, you need to have Python 3.x installed on your system along with the following libraries:
1. pandas
2. streamlit
3. easyocr
4. mysql-connector-python







## Necessary imports
1. import pandas as pd
2. import streamlit as st
3. import easyocr
4. import mysql.connector as sql
5. from PIL import Image
6. import io
7. import os
8. import re


## ## Project Overview
1. Upload an image of a business card to the application.
2. The uploaded image will be displayed on the screen.
3. The text from the image will be extracted using OCR.
4. The extracted text will be displayed on the screen.
5. Click the "Save Data" button to save the extracted data to a MySQL database.
6. To modify the data, select the "Modify" option from the sidebar and enter the ID of the entry you want to modify along with the new data.
7. Click the "Save" button to save the modified data to the database.
## ## Project Overview
1. Upload an image of a business card to the application.
2. The uploaded image will be displayed on the screen.
3. The text from the image will be extracted using OCR.
4. The extracted text will be displayed on the screen.
5. Click the "Save Data" button to save the extracted data to a MySQL database.
6. To modify the data, select the "Modify" option from the sidebar and enter the ID of the entry you want to modify along with the new data.
7. Click the "Save" button to save the modified data to the database.
## Contributing

If you would like to contribute to this project, please fork the repository and submit a pull request.

Contributions are always welcome!

## Credits
This script was created by Thirumalaivasan S.Feel free to modify and use it for your own purposes. If you have any questions or suggestions, feel free to reach out to me on LinkedIn at any time.
