import pandas as pd
import os

all_data = pd.read_csv('2023Dataset_H/2023_sales_data.csv')

all_data = all_data.dropna(how='all')  # Remove rows with all NaN values
all_data = all_data[all_data['Date'].str[0:2] != 'Or']  # Remove invalid rows

# Convert columns to appropriate types
all_data['Date'] = pd.to_datetime(all_data['Date'], errors='coerce')
all_data = all_data.dropna(subset=['Date'])  # Remove rows with invalid dates
all_data['Quantity'] = pd.to_numeric(all_data['Quantity'])
all_data['Unit price'] = pd.to_numeric(all_data['Unit price'])

# Add Sales column
all_data['Sales'] = all_data['Quantity'] * all_data['Unit price']

# Step 3: Define seasonal date ranges
seasons = {
    'Winter': ('2023-01-01', '2023-02-28'),
    'Summer': ('2023-03-01', '2023-06-30'),
    'Rainy': ('2023-07-01', '2023-09-30'),
}

# Step 4: Analyze each season
seasonal_analysis = {}

for season, (start_date, end_date) in seasons.items():
    # Filter data for the season
    season_data = all_data[(all_data['Date'] >= start_date) & (all_data['Date'] <= end_date)]

    # Calculate total sales for the season
    total_sales = season_data['Sales'].sum()

    # Top 10 products by sales
    top_products_sales = (season_data.groupby('Product_Name')['Sales']
                          .sum()
                          .sort_values(ascending=False)
                          .head(10)
                          .reset_index())

    # Top 10 products by quantity sold
    top_products_quantity = (season_data.groupby('Product_Name')['Quantity']
                             .sum()
                             .sort_values(ascending=False)
                             .head(10)
                             .reset_index())

    # Save results for the season
    seasonal_analysis[season] = {
        'Total Sales': total_sales,
        'Top Products by Sales': top_products_sales,
        'Top Products by Quantity': top_products_quantity,
    }

# Step 5: Display the results
for season, analysis in seasonal_analysis.items():
    print(f"\n{season} Season:")
    print(f"Total Sales: {analysis['Total Sales']:.2f}")
    print("\nTop 10 Products by Sales:")
    print(analysis['Top Products by Sales'])
    print("\nTop 10 Products by Quantity:")
    print(analysis['Top Products by Quantity'])

# Optionally, save seasonal analysis results to separate CSV files

#for season, analysis in seasonal_analysis.items():
    #   analysis['Top Products by Sales'].to_csv(f"{season}_Top_Products_by_Sales.csv", index=False)
    #  analysis['Top Products by Quantity'].to_csv(f"{season}_Top_Products_by_Quantity.csv", index=False)



