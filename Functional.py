import pandas as pd


def csv_file_directory(directory):
    """"User gives file directory info"""
    df = pd.read_csv(directory, error_bad_lines=False)
    return df


def new_excel_creation(df):
    writer = pd.ExcelWriter('E:/Python Projects/KAESER_Program/new_file.xlsx')
    df.to_excel(writer, 'Sheet1')
    writer.save()


def New_Excel_creation_with_selection(df, equip):
    writer = pd.ExcelWriter('E:/Python Projects/KAESER_Program/new_file.xlsx')
    new_df = select_rows(df, equip)

    del new_df['Sum price for peripherals ']
    del new_df['FAD 7.5']
    del new_df['FAD 10']
    del new_df['FAD 13']
    del new_df['delta FAD 7.5']
    del new_df['delta FAD 10']
    del new_df['delta FAD 13']

    new_df.to_excel(writer, 'Sheet1')
    writer.save()


def select_rows(df, equip, change1='Wight', change2='Dimensions'):
    """"Function selects particular rows and creates new DataFrame
        Takes DataFrame, change1 and change 2 (changeable name), eq='Equipment', pr='Price', fad='FAD'
        Takes equipment name list (normally input)
    """
    # Создание нового фрейма, хз так себе...
    new_df = pd.DataFrame(
        {'Equipment': '_', 'Price for equip.': '_', 'Sum price for peripherals ': '_', change1: '_', change2: '_',
         'FAD 7.5': '_', 'FAD 10': '_', 'FAD 13': '_', 'delta FAD 7.5': '_', 'delta FAD 10': '_',
         'delta FAD 13': '_'}, index=[0])
    for i in range(len(equip)):
        # Input and checks input
        if check_input(equip[i], list(df['Equipment'])):
            return False
        # Search and receive data from DataFrame
        search = df['Equipment'] == equip[i]
        new_df = pd.concat([new_df, df.loc[search]])
    return new_df


def sam_calculation(df, compr, sn_units, not_sn_units, not_sn_compr, dhs, dc):
    equip = []
    amount_column = ['_']
    if compr // 16 > 0:
        equip.append('SAM 2-16')
        amount_column.append(compr // 16)
    if compr % 16 <= 4:
        equip.append('SAM 2-4')
        amount_column.append(1)
    elif 4 < compr % 16 <= 8:
        equip.append('SAM 2-8')
        amount_column.append(1)
    elif 8 < compr % 16 <= 16:
        equip.append('SAM 2-16')
        amount_column.append(1)
    cables = ['SigmaNetwork Cable', 'Ethernet set', 'Plug Ethernet RJ45', 'Cable 2x0.75 analogue']
    for i in range(len(cables)):
        equip.append(cables[i])
    amount = ['max 100 m per unit', sn_units - (dhs + dc), sn_units, '30 m per pressure transducer']
    for i in range(len(amount)):
        amount_column.append(amount[i])
    selected_df = select_rows(df, equip, 'Material number', 'Max length per unit')

    del selected_df['Sum price for peripherals ']
    del selected_df['FAD 7.5']
    del selected_df['FAD 10']
    del selected_df['FAD 13']
    del selected_df['delta FAD 7.5']
    del selected_df['delta FAD 10']
    del selected_df['delta FAD 13']
    selected_df = selected_df.reset_index(drop=True)

    if not_sn_units != 0 and not_sn_compr == 0:
        amount_column.append('max 100 m per not SN unit')
        search = df['Equipment'] == 'Cable 2x0.75 digital'
        selected_df = pd.concat([selected_df, df.loc[search]])
    elif not_sn_units != 0 and not_sn_compr != 0 or not_sn_compr != 0:
        amount_column.append('max 100 m per not SN unit (compressors)')
        search = df['Equipment'] == 'Cable 2x0.75 digital'
        selected_df = pd.concat([selected_df, df.loc[search]])
        selected_df['Amount'] = amount_column
        selected_df['you probably need SBU, please contact application engineer'] = ['you probably need SBU, please '
                                                                                     'contact application engineer'
                                                                                     for n in range(len(amount_column))]
    if sn_units > 13:
        selected_df['Amount'] = amount_column
        selected_df['you probably need SBU, please contact application engineer'] = ['you probably need SBU, please '
                                                                                     'contact application engineer'
                                                                                     for n in range(len(amount_column))]

    if dhs != 0:
        amount_column.append(dhs)
        search = df['Equipment'] == 'Plug 4p M12 ETH'
        selected_df = pd.concat([selected_df, df.loc[search]])
    if dc != 0:
        amount_column.append(dc)
        search = df['Equipment'] == 'Plug LAN RJ45 SCS'
        selected_df = pd.concat([selected_df, df.loc[search]])

    selected_df['Amount'] = amount_column
    new_excel_creation(selected_df)


def control_gap_result(df, equip, pressure):
    new_df = select_rows(df, equip).reset_index(drop=True)
    mask = new_df['Equipment'].str.contains('SFC')
    sfc = new_df.loc[mask].reset_index(drop=True)
    if pressure == 8:
        delta = list(sfc['delta FAD 7.5'])
        return control_gap_check_sfc(mask, new_df, delta, 'FAD 7.5', sfc)
    elif pressure == 10:
        delta = list(sfc['delta FAD 10'])
        return control_gap_check_sfc(mask, new_df, delta, 'FAD 10', sfc)
    elif pressure == 13:
        delta = list(sfc['delta FAD 13'])
        return control_gap_check_sfc(mask, new_df, delta, 'FAD 13', sfc)


def control_gap_check_sfc(mask, new_df, delta, fad_column, sfc_df):
    mask2 = list(mask)
    for i in range(len(mask2)):
        if mask2[i] == 1:
            new_df.drop([i], inplace=True)

    new_df.drop([0], inplace=True)
    sfc_delta = float(delta[0])
    performance = list(new_df[fad_column])
    performance_float = []

    for fad in range(len(performance)):
        performance_float.append(float(performance[fad]))
        if float(performance[fad]) <= sfc_delta:
            return True

    performance_float = sorted(performance_float)
    sfc_fad_min = float(list(sfc_df[fad_column])[0]) - sfc_delta
    sfc_fad_min = float('{:.2f}'.format(sfc_fad_min))
    gap_list = []

    i = 0
    compr_sum = performance_float[0]

    while i < len(performance_float):
        if i == 0:
            gap_list.append(str(performance_float[i]) + '-' + str(sfc_fad_min + performance_float[i]))
        else:
            compr_sum += performance_float[i]
            min_and_compr_sum = sfc_fad_min + compr_sum
            min_and_compr_sum = float('{:.2f}'.format(min_and_compr_sum))
            gap_list.append(str(compr_sum) + '-' + str(min_and_compr_sum))
            if performance_float[i] != performance_float[i - 1]:
                gap_list.append(str(performance_float[i]) + '-' + str(sfc_fad_min + performance_float[i]))
        i += 1

    print(gap_list)

    return False


def check_input(example, list_of_sth):
    """"Function checks the written category"""
    if example not in list_of_sth:
        return True
