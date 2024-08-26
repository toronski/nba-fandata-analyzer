def add_dd_and_td(df):
    df['DD'] = ((df['PTS'] >= 10) + (df['REB'] >= 10) + (df['AST'] >= 10) 
                   + (df['STL'] >= 10) + (df['BLK'] >= 10)) >= 2
    df['DD'] = df['DD'].astype(int)

    df['TD'] = ((df['PTS'] >= 10) + (df['REB'] >= 10) + (df['AST'] >= 10) 
                   + (df['STL'] >= 10) + (df['BLK'] >= 10)) >= 3
    df['TD'] = df['TD'].astype(int)
    
    return df

def fantasypts_counter(df):
    df['FAN_PTS'] = (df['PTS'] +
                            (df['REB'] * 1.2) +
                            (df['AST'] * 1.5) +
                            (df['BLK'] * 3) +
                            (df['STL'] * 3) +
                            (df['TOV'] * -2) +
                            df['FG3M'] +
                            df['DD'] +
                            df['TD'])

    return df

def opponent_shorter(df):
    df['MATCHUP'] = df['MATCHUP'].apply(
        lambda x: x.split(' ')[2]
    )

    return df
