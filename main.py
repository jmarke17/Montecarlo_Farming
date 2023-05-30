import requests
import numpy as np

# Initial values
CAPITAL_EUROS = 35000
EXCHANGE_RATE_EURO_USD = 1.12
NUM_SIMULATIONS = 1000
NUM_DAYS = 365

# Rates of return
RETURN_RATE_RON = 0.06
RETURN_RATE_ETH = 0.05
RETURN_RATE_FARMING = 0.60

# Fetch the prices of cryptocurrencies from the CoinGecko API
response = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=ethereum,ronin&vs_currencies=usd")
data = response.json()

ETH_PRICE_INITIAL = data["ethereum"]["usd"]
RON_PRICE_INITIAL = data["ronin"]["usd"]

# Convert the capital to dollars
CAPITAL_USD = CAPITAL_EUROS * EXCHANGE_RATE_EURO_USD

staking_simulations_total = []
farming_simulations_total = []

for i in range(NUM_SIMULATIONS):
    # Initialize the prices
    ron_price = RON_PRICE_INITIAL
    eth_price = ETH_PRICE_INITIAL

    # Scenario 1: Staking
    capital_ron = CAPITAL_USD / 2 / ron_price
    capital_eth = CAPITAL_USD / 2 / eth_price

    # Scenario 2: Yield Farming
    capital_ron_farming = CAPITAL_USD / 2 / ron_price
    capital_eth_farming = CAPITAL_USD / 2 / eth_price

    for _ in range(NUM_DAYS):
        # Generate a random price change
        price_change = np.random.uniform(-0.01, 0.01)

        # Update the prices
        ron_price *= (1 + price_change)
        eth_price *= (1 + price_change)

        # Update the capital for staking
        capital_ron *= (1 + RETURN_RATE_RON / NUM_DAYS)
        capital_eth *= (1 + RETURN_RATE_ETH / NUM_DAYS)

        # Update the capital for yield farming
        capital_ron_farming *= (1 + RETURN_RATE_FARMING / NUM_DAYS)
        capital_eth_farming *= (1 + RETURN_RATE_FARMING / NUM_DAYS)

    # Calculate the total value for staking
    total_staking = capital_ron * ron_price + capital_eth * eth_price
    staking_simulations_total.append(total_staking)

    # Calculate the total value for yield farming
    total_farming = capital_ron_farming * ron_price + capital_eth_farming * eth_price

    # Calculate the impermanent loss
    price_ratio_initial = RON_PRICE_INITIAL / ETH_PRICE_INITIAL
    price_ratio_final = ron_price / eth_price

    impermanent_loss = 2 * np.sqrt(price_ratio_final / price_ratio_initial) / (1 + price_ratio_final / price_ratio_initial) - 1

    # Calculate the total value for yield farming, taking into account the impermanent loss
    total_farming = (capital_ron_farming * ron_price + capital_eth_farming * eth_price) * (1 - impermanent_loss)
    farming_simulations_total.append(total_farming)

# Calculate the average, max and min of the simulations
staking_average_total = int(np.mean(staking_simulations_total))
staking_max_total = int(np.max(staking_simulations_total))
staking_min_total = int(np.min(staking_simulations_total))

farming_average_total = int(np.mean(farming_simulations_total))
farming_max_total = int(np.max(farming_simulations_total))
farming_min_total = int(np.min(farming_simulations_total))

# Print the results
print(f"Staking: Average = {staking_average_total} USD, Max = {staking_max_total} USD, Min = {staking_min_total} USD")
print(f"Yield Farming: Average = {farming_average_total} USD, Max = {farming_max_total} USD, Min = {farming_min_total} USD")

# Compare the two scenarios
if staking_average_total > farming_average_total:
    print(f"According to the Monte Carlo analysis, staking is more profitable on average.")
elif farming_average_total > staking_average_total:
    print(f"According to the Monte Carlo analysis, yield farming is more profitable on average.")
else:
    print(f"According to the Monte Carlo analysis, both scenarios are equally profitable on average.")
