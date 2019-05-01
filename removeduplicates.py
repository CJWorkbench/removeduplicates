import pandas as pd


def removeduplicates(table, colnames, action):
    if action == 'delete':
        # Greedy drop duplicate rows, only keep first instance
        mask = table[colnames].duplicated()
        table = table[~mask]
        table.reset_index(drop=True, inplace=True)
        # Reset categories, for testing
        for column in table.columns:
            series = table[column]
            if hasattr(series, 'cat'):
                series.cat.remove_unused_categories(inplace=True)
        return table
    elif action == 'cumcount':
        table['Duplicate number'] = table.groupby(colnames).cumcount() + 1
        return table
    else:
        raise ValueError('Unknown action %s' % action)


def render(table, params):
    if not params['colnames']:
        return table

    return removeduplicates(table, params['colnames'], params['action'])


def _migrate_params_v0_to_v1(params):
    """
    v0: colnames is comma-separated str, type is 0|1 (delete|cumcount).

    v1: colnames is List[str], action is delete|cumcount.
    """
    return {
        'colnames': [c for c in params['colnames'].split(',') if c],
        'action': ['delete', 'cumcount'][params['type']]
    }


def migrate_params(params):
    if isinstance(params['colnames'], str):
        params = _migrate_params_v0_to_v1(params)
    return params
