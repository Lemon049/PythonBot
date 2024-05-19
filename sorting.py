import pandas as pd




def filter_games(platform, edition, region, activation_type):
    df = pd.read_excel('C:\\Users\\Yehor\\Documents\\GitHub\\PythonBot\\scraped_data.xlsx')
    filtered_games = df[(df['Platform'] == platform) &
                        (df['Edition'] == edition) &
                        (df['Region'] == region) &
                        (df['Activation type'] == activation_type)]
    return filtered_games


def analyze_games(games):
    results_array = []

    # Calculate average price
    avg_price = games['Price'].mean()

    # Determine the price range
    min_price_range = avg_price * 0.75
    max_price_range = avg_price * 1.25

    # Filter games within the price range
    games_within_range = games[(games['Price'] >= min_price_range) & (games['Price'] <= max_price_range)]

    if not games_within_range.empty:
        # Find game with max price within range
        max_price_game = games_within_range.loc[games_within_range['Price'].idxmax()]
        max_price = max_price_game['Price']
        results_array.append((max_price_game, max_price))

        # Find game with min price within range
        min_price_game = games_within_range.loc[games_within_range['Price'].idxmin()]
        min_price = min_price_game['Price']
        results_array.append((min_price_game, min_price))

        # Calculate average price within range
        avg_price_within_range = games_within_range['Price'].mean()
        results_array.append(avg_price_within_range)
    else:
        results_array.append(None)
        results_array.append(None)
        results_array.append(None)

    return results_array

def analyze_certain_amount_of_games(number_of_games):
    games = pd.read_excel('C:\\Users\\Yehor\\Documents\\GitHub\\PythonBot\\scraped_data.xlsx')
    results_array = []

    # Calculate average price
    avg_price = games['Price'].mean()

    # Determine the price range
    min_price_range = avg_price * 0.75
    max_price_range = avg_price * 1.25

    # Filter games within the price range
    games_within_range = games[(games['Price'] >= min_price_range) & (games['Price'] <= max_price_range)]

    return games_within_range.head(number_of_games)
def analyze_filtered_games(platform, edition, region, activation_type):
    filtered_games = filter_games(platform, edition, region, activation_type)
    return analyze_games(filtered_games)


def main_filtered_games(platform, edition, region, activation_type):
    results = analyze_filtered_games(platform, edition, region, activation_type)

    # Output results
    if results[0] is not None and results[1] is not None:
        results_strings = [
            f"Game with max price: {results[0][0]['Link']} - Price: {results[0][1]}",
            f"Game with min price: {results[1][0]['Link']} - Price: {results[1][1]}",
            f"Average price for games within range: {results[2]}"
        ]
    else:
        results_strings = ["No games found within the specified price range."]

    return results_strings

def all_games_data():
    df = pd.read_excel('C:\\Users\\Yehor\\Documents\\GitHub\\PythonBot\\scraped_data.xlsx')
    results = analyze_games(df)
    return results
def main_all_games():
    df = pd.read_excel('C:\\Users\\Yehor\\Documents\\GitHub\\PythonBot\\scraped_data.xlsx')
    results = analyze_games(df)

    # Output results
    if results[0] is not None and results[1] is not None:
        results_strings = [
            f"Game with max price: {results[0][0]['Link']} - Price: {results[0][1]} €",
            f"Game with min price: {results[1][0]['Link']} - Price: {results[1][1]} €",
            f"Average price for games within range: {results[2]:.2f} €"
        ]
    else:
        results_strings = ["No games found within the specified price range."]

    return results_strings

