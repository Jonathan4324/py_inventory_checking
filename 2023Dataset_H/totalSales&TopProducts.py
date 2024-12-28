import pandas as pd
import json
# Load the new dataset
all_data = pd.read_csv("2023Dataset_H/2023_sales_data.csv")

# Remove any rows with all NaN values
all_data = all_data.dropna(how='all')

# Ensure 'Date' is parsed properly to datetime format
all_data['Date'] = pd.to_datetime(all_data['Date'], format='%d/%m/%Y', errors='coerce')

# Drop rows with invalid dates
all_data = all_data.dropna(subset=['Date'])

# Extract Month and Year for grouping
all_data['Month'] = all_data['Date'].dt.to_period('M')  # Extract month and year
all_data['Year'] = all_data['Date'].dt.year  # Extract year

# Add a "Sales" column (from the 'Total' column for this dataset)
all_data['Sales'] = all_data['Total']

# Calculate total yearly sales
yearly_sales = all_data.groupby('Year')['Sales'].sum().reset_index()
print("\nTotal Yearly Sales:")
print(yearly_sales)

# Calculate monthly sales
monthly_sales = all_data.groupby('Month')['Sales'].sum().reset_index()
monthly_sales['Month'] = monthly_sales['Month'].dt.strftime('%B %Y')  # Convert to a readable format
monthly_sales.index += 1  # Make the index start from 1
print("\nTotal Monthly Sales:")
print(monthly_sales)

# Find the month with the highest sales
highest_sales = monthly_sales['Sales'].max()
highest_month = monthly_sales[monthly_sales['Sales'] == highest_sales]['Month'].iloc[0]
print(f"\nMonth with the Highest Sales: {highest_month}, Total Sales: {highest_sales}")

# Calculate daily sales
daily_sales = all_data.groupby(all_data['Date'].dt.date)['Sales'].sum().reset_index()
daily_sales.columns = ['Date', 'Total Sales']
daily_sales.index += 1  # Make the index start from 1
print("\nTotal Daily Sales:")
print(daily_sales)

# Calculate total quantity sold by product
product_sales_quantity = all_data.groupby('Product_Name')['Quantity'].sum().reset_index()
product_sales_quantity = product_sales_quantity.sort_values(by='Quantity', ascending=False).head(10).reset_index(drop=True)
product_sales_quantity.index += 1  # Make the index start from 1
print("\nTop 10 Products by Quantity Sold:")
print(product_sales_quantity)

# Calculate total sales by product
product_sales_total = all_data.groupby('Product_Name')['Sales'].sum().reset_index()
product_sales_total = product_sales_total.sort_values(by='Sales', ascending=False).head(10).reset_index(drop=True)
product_sales_total.index += 1  # Make the index start from 1
print("\nTop 10 Products by Total Sales:")
print(product_sales_total)

# Calculate least sold products by quantity
least_quantity_sold = all_data.groupby('Product_Name')['Quantity'].sum().reset_index()
least_quantity_sold = least_quantity_sold.sort_values(by='Quantity', ascending=True).head(10).reset_index(drop=True)
least_quantity_sold.index += 1  # Make the index start from 1
print("\nTop 10 Products with Least Quantity Sold:")
print(least_quantity_sold)

# Calculate least sold products by total sales
least_sales_amount = all_data.groupby('Product_Name')['Sales'].sum().reset_index()
least_sales_amount = least_sales_amount.sort_values(by='Sales', ascending=True).head(10).reset_index(drop=True)
least_sales_amount.index += 1  # Make the index start from 1
print("\nTop 10 Products with Least Total Sales:")
print(least_sales_amount)


#Testing Json structure for total sales for monthly, daily and one year

# Create the JSON structure for total monthly sales
# total_monthly_sales_json = {
#     "TotalMonthlySales": monthly_sales.to_dict(orient="records")  # Convert DataFrame to list of dictionaries
# }

# # Save the JSON structure to a file
# with open("total_monthly_sales.json", "w") as json_file:
#     json.dump(total_monthly_sales_json, json_file, indent=4)

# print("\nJSON file created successfully. Check the file 'total_monthly_sales.json'.")