import pandas as pd

df = pd.read_excel('C:\\Users\\Yehor\\Documents\\GitHub\\PythonBot\\scraped_data.xlsx')

# Average of all prices in the table
average_price = df['Price'].mean()

# Filtering table by price, saving only prices that differ by ±25% from the average
lower_bound = average_price * 0.75
upper_bound = average_price * 1.25
filtered_df = df[(df['Price'] >= lower_bound) & (df['Price'] <= upper_bound)]


# Function to filter data by activation type
def filter_by_activation_type(df, activation_type):
    return df[df['Activation type'].str.contains(activation_type, na=False, case=False)]


# Function to filter data by platform
def filter_by_platform(df, platform):
    return df[df['Platform'].str.contains(platform, na=False, case=False)]


# Function to find and print row with extreme value (min/max)
def print_row_info(row, title):
    print(f"{title}:")
    print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    for column in row.index:
        print(f"{column}: {row[column]}")
    print()


# Filtering by activation type
key_activation_df = filter_by_activation_type(filtered_df, 'цифровой ключ')
present_activation_df = filter_by_activation_type(filtered_df, 'подарком')
account_activation_df = filter_by_activation_type(filtered_df, 'с заходом на аккаунт')

# Filtering by platform
pc_platform_df = filter_by_platform(filtered_df, 'pc')
xbox_platform_df = filter_by_platform(filtered_df, 'xbox')

# Finding rows with min/max values
max_price_row = filtered_df.loc[filtered_df['Price'].idxmax()]
min_price_row = filtered_df.loc[filtered_df['Price'].idxmin()]
max_rating_row = filtered_df.loc[filtered_df['Rating'].idxmax()]
max_stars_row = filtered_df.loc[filtered_df['Stars'].idxmax()]
min_key_row = key_activation_df.loc[key_activation_df['Price'].idxmin()]
min_present_row = present_activation_df.loc[present_activation_df['Price'].idxmin()]
min_account_row = account_activation_df.loc[account_activation_df['Price'].idxmin()]
min_pc_row = pc_platform_df.loc[pc_platform_df['Price'].idxmin()]
min_xbox_row = xbox_platform_df.loc[xbox_platform_df['Price'].idxmin()]

# Sorting the filtered DataFrame by 'Price'
sorted_df = filtered_df.sort_values(by='Price')


# Printing functions for specific rows
def max_price():
    print_row_info(max_price_row, "Row with the maximum price")


def min_price():
    print_row_info(min_price_row, "Row with the minimum price")


def top_rating():
    print_row_info(max_rating_row, "Row with the top rating")


def top_stars():
    print_row_info(max_stars_row, "Row with the top stars")


def minKey_price():
    print_row_info(min_key_row, "Row with the minimum price for Key activation type")


def minPresent_price():
    print_row_info(min_present_row, "Row with the minimum price for Present activation type")


def minAccount_price():
    print_row_info(min_account_row, "Row with the minimum price for Account activation type")


def minPC_price():
    print_row_info(min_pc_row, "Row with the minimum price for PC platform")


def minXBOX_price():
    print_row_info(min_xbox_row, "Row with the minimum price for Xbox platform")


#Custom search function
def custom_search_by_column(df):
    column_name = input("Enter the column name to search (Platform/Edition/Region/Activation type): ").strip()
    search_value = input(f"Enter the value to search in the {column_name} column: ").strip()

    if column_name not in df.columns:
        print(f"Column '{column_name}' does not exist in the DataFrame.")
        return

    # Filter the DataFrame based on the search value
    result_df = df[df[column_name].str.contains(search_value, na=False, case=False)]

    if result_df.empty:
        print("No matching records found.")
    else:
        print("Matching records:")
        for index, row in result_df.iterrows():
            print_row_info(row, f"Row {index}")


#custom_search_by_column(filtered_df)

# max_price()
# min_price()
# top_rating()
# top_stars()
# minKey_price()
# minPresent_price()
# minAccount_price()
# minPC_price()
# minXBOX_price()