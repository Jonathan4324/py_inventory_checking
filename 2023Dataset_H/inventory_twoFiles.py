import pandas as pd

# Function to clean and standardize product names
def clean_product_names(df, column_name):
    """
    Standardize the product names in the given column.
    Args:
        df (DataFrame): The input DataFrame.
        column_name (str): The column to be cleaned.
    Returns:
        DataFrame: Updated DataFrame with cleaned product names.
    """
    df[column_name] = df[column_name].str.strip().str.lower()
    return df

# Function to compute remaining stock levels
def compute_remaining_stock(after_sales_df, before_sales_df):
    """
    Subtract the quantities sold from the initial inventory and determine stock status.
    Args:
        before_sales_df (DataFrame): DataFrame containing initial inventory data.
        after_sales_df (DataFrame): DataFrame containing sales data.
    Returns:
        DataFrame: Inventory with remaining stock and status information.
    """
    try:
        # Standardize product names
        after_sales_df = clean_product_names(after_sales_df, "Product_Name")
        before_sales_df = clean_product_names(before_sales_df, "Product_Name")

        # Group sales by 'Product_Name' to compute total quantities sold
        sales_summary = after_sales_df.groupby('Product_Name', as_index=False)['Quantity'].sum()

        # Merge the initial inventory data with sales data
        inventory_df = pd.merge(before_sales_df, sales_summary, how="left", on="Product_Name")

        # Replace NaN values with 0 (for products not sold)
        inventory_df["Quantity"] = inventory_df["Quantity"].fillna(0)

        # Compute the remaining stock
        inventory_df["Remaining Stock"] = inventory_df["Quantity_in_Store"] - inventory_df["Quantity"]

        # Determine stock status
        inventory_df["Stock Status"] = inventory_df.apply(
            lambda row: "Low Stock" if row["Remaining Stock"] < 0.1 * row["Quantity_in_Store"]
            else "In Stock",
            axis=1
        )

        # Determine overstock status
        inventory_df["Overstock Status"] = inventory_df.apply(
            lambda row: "Potential Over-stock" if row["Remaining Stock"] > 0.2 * row["Quantity_in_Store"]
            else "Normal Stock",
            axis=1
        )

        print("Remaining stock computed successfully.")
        return inventory_df

    except Exception as e:
        print(f"Error computing remaining stock: {e}")
        return None

# Main function
def main():
    """
    Main function to orchestrate inventory computation.
    """
    # Load data directly from file paths
    after_sales_file = '2023Dataset_H/2023_sales_data.csv'
    before_sales_file = '2023Dataset_H/2023_origin_data.csv'

    try:
        # Read the input data files
        after_sales_df = pd.read_csv(after_sales_file)
        before_sales_df = pd.read_csv(before_sales_file)

        # Ensure correct column names for initial inventory data
        if 'Product_Name' not in before_sales_df.columns or 'Quantity_in_Store' not in before_sales_df.columns:
            raise ValueError("Before sales file must contain 'Product_Name' and 'Quantity_in_Store' columns.")
        if 'Product_Name' not in after_sales_df.columns or 'Quantity' not in after_sales_df.columns:
            raise ValueError("After sales file must contain 'Product_Name' and 'Quantity' columns.")
        
    except Exception as e:
        print(f"Error loading data files: {e}")
        return

    # Compute the remaining stock levels
    inventory_df = compute_remaining_stock(after_sales_df, before_sales_df)

    if inventory_df is None:
        print("Error computing remaining stock. Exiting...")
        return

    # Display final inventory
    print("\nFinal Inventory Status:")
    print(inventory_df[["Product_Name", "Quantity_in_Store", "Quantity", "Remaining Stock", "Stock Status", "Overstock Status"]])


# Execute the main function
if __name__ == "__main__":
    main()
