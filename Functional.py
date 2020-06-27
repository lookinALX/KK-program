import pandas as pd


def csv_file_directory(directory):
    """"User gives file directory info"""
    df = pd.read_csv(directory)
    return df


def New_Excel_creation(df, eq_name):
    writer = pd.ExcelWriter('E:/Python Projects/KAESER_Program/new_file.xlsx')
    select_rows(df, eq_name).to_excel(writer, 'Sheet1')
    writer.save()


def select_rows(df, eq_name, amount=0, change1='Wight', change2='Dimensions',
                eq='Equipment', pr='Price', fad='FAD'):
    """"Function selects particular rows and creates new DataFrame
        Takes DataFrame, change1 and change 2 (changeable name), eq='Equipment', pr='Price', fad='FAD'
        Takes amount (normally input)
    """
    if amount == 0:
        amount = int(input('Enter the number of equipment: '))
    # Создание нового фрейма, хз так себе...
    new_df = pd.DataFrame({eq: '_', pr: '_', change1: '_', change2: '_', fad: '_'}, index=[0])
    for i in range(amount):
        # Input and checks input
        eq_name = check_input(eq_name, list(df['Equipment']))
        # Search and receive data from DataFrame
        search = df['Equipment'] == eq_name
        new_df = pd.concat([new_df, df.loc[search]])
    return new_df


def check_input(example, list_of_sth):
    """"Function checks the written category"""
    i = True
    while i:
        if example in list_of_sth:
            i = False
        else:
            example = input('There is not this category or equipment. Please enter correct one: ')
    return example
