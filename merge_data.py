#!/usr/bin/env python3
import pandas as pd
import time

if __name__ == '__main__':
    merged = pd.read_csv('data/merged.csv')
    date = time.strftime('%Y-%m-%d')
    new_data = pd.read_csv(f'data/data-{date}.csv')
    old_num = len(merged)
    merged = pd.concat([merged, new_data]
                       ).drop_duplicates().reset_index(drop=True)
    new_num = len(merged)
    merged.to_csv('data/merged.csv', index=False, header=True)
    print(f'{new_num - old_num} rows merged into the csv')
