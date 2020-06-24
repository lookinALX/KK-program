import pandas as pd


def csv_file_directory(directory):
    """"User gives file directory info"""
    df = pd.read_csv(directory)
    print(1)
    return df


if __name__ == '__main__':
    csv_file_directory('E:/Python Projects/KAESER_Program/test.csv')
