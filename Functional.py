import pandas as pd


def csv_file_directory(directory):
    """"User gives file directory info"""
    df = pd.read_csv(directory)
    return df


def New_Excel_creation(df, equip):
    writer = pd.ExcelWriter('E:/Python Projects/KAESER_Program/new_file.xlsx')
    select_rows(df, equip).to_excel(writer, 'Sheet1')
    writer.save()


def select_rows(df, equip, change1='Wight', change2='Dimensions',
                eq='Equipment', pr='Price', fad='FAD'):
    """"Function selects particular rows and creates new DataFrame
        Takes DataFrame, change1 and change 2 (changeable name), eq='Equipment', pr='Price', fad='FAD'
        Takes equipment name list (normally input)
    """
    # Создание нового фрейма, хз так себе...
    new_df = pd.DataFrame({eq: '_', pr: '_', change1: '_', change2: '_', fad: '_'}, index=[0])
    for i in range(len(equip)):
        # Input and checks input
        if check_input(equip[i], list(df['Equipment'])):
            return False
        # Search and receive data from DataFrame
        search = df['Equipment'] == equip[i]
        new_df = pd.concat([new_df, df.loc[search]])
    return new_df


def check_input(example, list_of_sth):
    """"Function checks the written category"""
    if example not in list_of_sth:
        return True

