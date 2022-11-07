import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('love_sandwiches')


def get_sales_data():
    """
    gets sales figures input from the user 
    """
    print("Please enter sales data from the last market")
    print("Data should be six numbers seperated by commas")
    print("example: 1,2,3,4,5,6\n")

    data_str = input("Enter your data here: ")
    sales_data = data_str.split(",")
    validate_data(sales_data)


def validate_data(values):
    """
    inside the try, converts all string values into integers, 
    raises value error if string values cannot be converted into ints
    or if there arn't exactly 6 values.
    """
    print(values)
    try:
        [int(value) for value in values]
        if len(values) != 6:
            raise ValueError(
                f"Expected six values, you provided {len(values)}"
            )
    except ValueError as e:
        print(f"Invalid data: {e}, please try again.\n")


get_sales_data()