import pandas as pd

# Read the Excel file
df = pd.read_excel('C:\\Users\\Yehor\\Documents\\GitHub\\PythonBot\\scraped_data.xlsx')


def filter_games(platform, edition, region, activation_type):
    filtered_games = df[(df['Platform'] == platform) &
                        (df['Edition'] == edition) &
                        (df['Region'] == region) &
                        (df['Activation type'] == activation_type)]
    return filtered_games


def analyze_games(games):
    results_array = []

    # Find game with max price
    max_price_game = games.loc[games['Price'].idxmax()]
    max_price = max_price_game['Price']
    results_array.append((max_price_game, max_price))

    # Find game with min price
    min_price_game = games.loc[games['Price'].idxmin()]
    min_price = min_price_game['Price']
    results_array.append((min_price_game, min_price))

    # Calculate average price
    avg_price = games['Price'].mean()
    results_array.append(avg_price)

    return results_array


def analyze_filtered_games(platform, edition, region, activation_type):
    filtered_games = filter_games(platform, edition, region, activation_type)
    return analyze_games(filtered_games)


def main_filtered_games(platform, edition, region, activation_type):
    results = analyze_filtered_games(platform, edition, region, activation_type)

    # Output results
    results_strings = [
        f"Game with max price: {results[0][0]['Link']} - Price: {results[0][1]}",
        f"Game with min price: {results[1][0]['Link']} - Price: {results[1][1]}",
        f"Average price for games: {results[2]}"
    ]

    return results_strings


def main_all_games():
    results = analyze_games(df)

    # Output results
    results_strings = [
        f"Game with max price: {results[0][0]['Link']} - Price: {results[0][1]}",
        f"Game with min price: {results[1][0]['Link']} - Price: {results[1][1]}",
        f"Average price for games: {results[2]}"
    ]

    return results_strings


if __name__ == "__main__":
    # Example usage for filtered games
    platform = "pc"
    edition = "premium edition"
    region = "турция"
    activation_type = "с заходом на аккаунт"
    results_filtered = main_filtered_games(platform, edition, region, activation_type)
    print("Filtered games:")
    for result in results_filtered:
        print(result)

    # Example usage for all games
    print("\nAll games:")
    results_all = main_all_games()
    for result in results_all:
        print(result)
