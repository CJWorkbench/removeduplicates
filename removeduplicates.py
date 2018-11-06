import pandas as pd

count_col_name = 'Duplicate number'

def removeduplicates(table, colnames, type):
    try:
        sub_table = table[colnames]
    except KeyError as err:
        return 'You chose a missing column'

    # Greedy drop duplicate rows, only keep first instance
    if type == 0:
        mask = sub_table.duplicated()
        idx = mask[~mask].index
        return table.loc[idx].reset_index(drop=True) # reset index for testing

    # Add duplicate cumulative count
    elif type == 1:
        table[count_col_name] = table.groupby(colnames).cumcount() + 1
        return table

    return table


def render(table, params):
    colnames = list([c for c in params['colnames'].split(',') if c])
    type = params['type']
    if not colnames:
        return table

    return removeduplicates(table, colnames, type)
