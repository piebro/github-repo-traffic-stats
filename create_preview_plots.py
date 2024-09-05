import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
from matplotlib.ticker import MaxNLocator
import calendar
from datetime import datetime, timedelta
import os
import numpy as np

def create_plot(df, title, filename):
    current_date = datetime.now().date()
    first_day_current_month = current_date.replace(day=1)
    last_day_previous_month = first_day_current_month - timedelta(days=1)
    first_day_previous_month = last_day_previous_month.replace(day=1)
    df_filtered = df.loc[first_day_previous_month:last_day_previous_month]

    # add zeros if there is no value 
    date_range = pd.date_range(start=first_day_previous_month, end=last_day_previous_month, freq='D').date
    df_full = pd.DataFrame(index=date_range, columns=df.columns).fillna(0)
    df_full.update(df_filtered)
    
    total_views = df_full["count"].sum()
    total_uniques = df_full["uniques"].sum()
    
    plt.figure(figsize=(12, 6))
    plt.plot(df_full.index, df_full["count"], label="Views", color='blue')
    plt.plot(df_full.index, df_full["uniques"], label="Unique Visitors", color='red')
    
    plt.title(f"{title} ({total_views} Views, {total_uniques} Unique Visitors)")
    plt.xlabel('Date')
    plt.ylabel('Count')
    plt.legend()
    plt.gca().xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
    plt.gcf().autofmt_xdate()
    plt.gca().yaxis.set_major_locator(MaxNLocator(integer=True))
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.savefig(filename, dpi=100, bbox_inches='tight', format='webp')
    plt.close()

def main():
    with open('github_username.txt', 'r') as file:
        owner = file.read().strip()

    data_dir = 'data/github_views'
    plots_dir = 'preview_plots'
    os.makedirs(plots_dir, exist_ok=True)

    for filename in sorted(os.listdir(data_dir)):
        if filename.endswith('.csv'):
            repo = filename[:-4]
            
            views_df = pd.read_csv(os.path.join(data_dir, filename), parse_dates=['date'])
            views_df.set_index('date', inplace=True)
            
            plot_filename = f'{plots_dir}/{repo}.webp'
            create_plot(views_df, f'{owner}/{repo}', plot_filename)
            print(f"Created plot for {owner}/{repo}")

if __name__ == "__main__":
    main()