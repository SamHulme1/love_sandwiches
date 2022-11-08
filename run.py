import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint

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
    while True:

        print("Please enter sales data from the last market")
        print("Data should be six numbers seperated by commas")
        print("example: 1,2,3,4,5,6\n")

        data_str = input("Enter your data here: ")
        sales_data = data_str.split(",")

        if validate_data(sales_data):
            print("data is valid")
            break

    return sales_data


def validate_data(values):
    """
    inside the try, converts all string values into integers, 
    raises value error if string values cannot be converted into ints
    or if there arn't exactly 6 values.
    """
    try:
        [int(value) for value in values]
        if len(values) != 6:
            raise ValueError(
                f"Expected six values, you provided {len(values)}"
            )
    except ValueError as e:
        print(f"Invalid data: {e}, please try again.\n")
        return False
    
    return True
    

def update_sales_worksheet(data):
    """
    update sales data, add new row with list data provided
    """
    print("Updating sales worksheet...\n")
    sales_worksheet = SHEET.worksheet("sales")
    sales_worksheet.append_row(data)
    print("Sales worksheet updated successfully\n")


def calculate_surplus_data(sales_row):
    """
    Compare sales data with stock to calculate surplus data
    surplus = sales data - stock data
    positive surplus = waste
    negative surplus = extra stock that needs to be produced to meet demand

    """
    print("Calculating surplus data...\n")
    stock = SHEET.worksheet("stock").get_all_values()
    stock_row = stock.pop()

    surplus_data = []
    for stock, sales in zip(stock_row, sales_row):
        surplus = int(stock) - sales
        surplus_data.append(surplus)
    return surplus_data


def update_surplus_worksheet(data):
    """
    update surplus data, add new row with list data provided
    """
    print("Updating surplus worksheet...\n")
    surplus_worksheet = SHEET.worksheet("surplus")
    surplus_worksheet.append_row(data)
    print("Surplus worksheet updated successfully\n")


def main():
    """
    Run main program functions 
    """
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_sales_worksheet(sales_data)
    new_surplus_data = calculate_surplus_data(sales_data)
    update_surplus_worksheet(new_surplus_data)


print("Welcome to Love Sandwiches data automation")
main()