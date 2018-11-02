import pandas as pd

count_col_name = 'Duplicate count'

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

    # Add duplicate labels
    elif type == 1:
        # group duplicates and shift index to use as count
        groups = table.groupby(colnames).count()
        groups = pd.DataFrame(list(groups.index), columns=colnames).reset_index()

        # left join to add group count
        new_table = pd.merge(table, groups, on=colnames, how='left')

        return new_table.rename(index=str, columns={'index': count_col_name}).reset_index(drop=True) # reset index for testing

    return table


def render(table, params):
    colnames = list([c for c in params['colnames'].split(',') if c])
    type = params['type']
    if not colnames:
        return table

    return removeduplicates(table, colnames, type)
