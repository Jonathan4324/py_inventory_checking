import pandas as pd
import os

all_data = pd.read_csv('2023Dataset_H/2023_sales_data.csv')

# Festivals with date ranges
festivals = {
    'Thingyan': ('04-10', '04-30'),
    'Thadingyut': ('10-01', '10-31'),
    'Thasaungtine': ('11-01', '11-30'),
    'Christmas': ('12-23', '12-26'),
}

# Step 1: Prepare the data
all_data = all_data.dropna(how='all')  # Remove completely empty rows

# Convert 'Date' column to datetime and extract 'Month-Day' for filtering
all_data['Date'] = pd.to_datetime(all_data['Date'], format='%d/%m/%Y', dayfirst=True)
all_data['Month-Day'] = all_data['Date'].dt.strftime('%m-%d')

# Step 2: Analyze products during festivals
festival_results = {}

for festival, (start_date, end_date) in festivals.items():
    # Filter data for the current festival
    festival_data = all_data[(all_data['Month-Day'] >= start_date) & (all_data['Month-Day'] <= end_date)]

    # Aggregate quantity sold by product
    aggregated = festival_data.groupby('Product_Name')['Quantity'].sum().reset_index()

    # Sort to get top 10 most and least sold products
    top_10_most_sold = aggregated.sort_values(by='Quantity', ascending=False).head(10)
    top_10_least_sold = aggregated.sort_values(by='Quantity', ascending=True).head(10)

    # Save results for the festival
    festival_results[festival] = {
        'Top 10 Most Sold Products': top_10_most_sold,
        'Top 10 Least Sold Products': top_10_least_sold,
    }
    
# Step 3: Display the results
for festival, results in festival_results.items():
    print(f"\n{festival} Festival:")
    print("\nTop 10 Most Sold Products:")
    print(results['Top 10 Most Sold Products'])
    print("\nTop 10 Least Sold Products:")
    print(results['Top 10 Least Sold Products'])