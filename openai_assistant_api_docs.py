cmc_quote_lastest_api_doc = """
Base URL: https://pro-api.coinmarketcap.com/v2/cryptocurrency/quotes/latest

Quotes Latest v2 API Documentation
Returns the latest market quote for 1 or more cryptocurrencies. Use the "convert" option to return market values in multiple fiat and cryptocurrency conversions in the same call.
There is no need to use aux to specify a specific market data, and the returned quote contains all market data.

PARAMETERS:
slug: Alternatively pass a comma-separated list of cryptocurrency slugs. Example: "bitcoin,ethereum"
symbol: Alternatively pass one or more comma-separated cryptocurrency symbols. Example: "BTC,ETH". At least one "id" or "slug" or "symbol" is required for this request.
convert: Optionally calculate market quotes in up to 120 currencies at once by passing a comma-separated list of cryptocurrency or fiat currency symbols. Each additional convert option beyond the first requires an additional call credit. A list of supported fiat options can be found here. Each conversion is returned in its own "quote" object.

RESPONSE
id: The unique CoinMarketCap ID for this cryptocurrency.
name: The name of this cryptocurrency.
symbol: The ticker symbol for this cryptocurrency.
slug: The web URL friendly shorthand version of this cryptocurrency name.
cmc_rank: The cryptocurrency's CoinMarketCap rank by market cap.
num_market_pairs: The number of active trading pairs available for this cryptocurrency across supported exchanges.
circulating_supply: The approximate number of coins circulating for this cryptocurrency.
total_supply: The approximate total amount of coins in existence right now (minus any coins that have been verifiably burned).
market_cap_by_total_supply: The market cap by total supply. This field is only returned if requested through the aux request parameter.
max_supply: The expected maximum limit of coins ever to be available for this cryptocurrency.
date_added: Timestamp (ISO 8601) of when this cryptocurrency was added to CoinMarketCap.
tags: Array of tags associated with this cryptocurrency. Currently only a mineable tag will be returned if the cryptocurrency is mineable. Additional tags will be returned in the future.
platform: Metadata about the parent cryptocurrency platform this cryptocurrency belongs to if it is a token, otherwise null.
self_reported_circulating_supply: The self reported number of coins circulating for this cryptocurrency.
self_reported_market_cap: The self reported market cap for this cryptocurrency.
quote: A map of market quotes in different currency conversions. The default map included is USD. See the flow Quote Map Instructions.

Quote Map Instructions:
price: Price in the specified currency.
volume_24h: Rolling 24 hour adjusted volume in the specified currency.
volume_change_24h: 24 hour change in the specified currencies volume.
volume_24h_reported: Rolling 24 hour reported volume in the specified currency. This field is only returned if requested through the aux request parameter.
volume_7d: Rolling 7 day adjusted volume in the specified currency. This field is only returned if requested through the aux request parameter.
volume_7d_reported: Rolling 7 day reported volume in the specified currency. This field is only returned if requested through the aux request parameter.
volume_30d: Rolling 30 day adjusted volume in the specified currency. This field is only returned if requested through the aux request parameter.
volume_30d_reported: Rolling 30 day reported volume in the specified currency. This field is only returned if requested through the aux request parameter.
market_cap: Market cap in the specified currency.
market_cap_dominance: Market cap dominance in the specified currency.
fully_diluted_market_cap: Fully diluted market cap in the specified currency.
percent_change_1h: Percentage price increase within 1 hour in the specified currency.
percent_change_24h: Percentage price increase within 24 hour in the specified currency.
percent_change_7d: Percentage price increase within 7 day in the specified currency.
percent_change_30d: Percentage price increase within 30 day in the specified currency.
"""
cmc_trending_latest_api_doc = """
Base URL: https://pro-api.coinmarketcap.com/v1/cryptocurrency/trending/latest

Trending Latest
Returns a paginated list of all trending cryptocurrency market data, determined and sorted by CoinMarketCap search volume.

PARAMETERS:
start: Default is 1. Optionally offset the start (1-based index) of the paginated list of items to return. 
limit: Default is 100. Optionally specify the number of results to return. Use this parameter and the "start" parameter to determine your own pagination size.
time_period: Default is "24h". Valid values: "24h" "30d" "7d". Adjusts the overall window of time for the latest trending coins. 
convert: Optionally calculate market quotes in up to 120 currencies at once by passing a comma-separated list of cryptocurrency or fiat currency symbols. Each additional convert option beyond the first requires an additional call credit. A list of supported fiat options can be found here. Each conversion is returned in its own "quote" object.

RESPONSE
id: The unique CoinMarketCap ID for this cryptocurrency.
name: The name of this cryptocurrency.
symbol: The ticker symbol for this cryptocurrency.
slug: The web URL friendly shorthand version of this cryptocurrency name.
cmc_rank: The cryptocurrency's CoinMarketCap rank by market cap.
num_market_pairs: The number of active trading pairs available for this cryptocurrency across supported exchanges.
circulating_supply: The approximate number of coins circulating for this cryptocurrency.
total_supply: The approximate total amount of coins in existence right now (minus any coins that have been verifiably burned).
market_cap_by_total_supply: The market cap by total supply. This field is only returned if requested through the aux request parameter.
max_supply: The expected maximum limit of coins ever to be available for this cryptocurrency.
date_added: Timestamp (ISO 8601) of when this cryptocurrency was added to CoinMarketCap.
tags: Array of tags associated with this cryptocurrency. Currently only a mineable tag will be returned if the cryptocurrency is mineable. Additional tags will be returned in the future.
platform: Metadata about the parent cryptocurrency platform this cryptocurrency belongs to if it is a token, otherwise null.
self_reported_circulating_supply: The self reported number of coins circulating for this cryptocurrency.
self_reported_market_cap: The self reported market cap for this cryptocurrency.
quote: A map of market quotes in different currency conversions. The default map included is USD. See the flow Quote Map Instructions.

Quote Map Instructions:
price: Price in the specified currency.
volume_24h: Rolling 24 hour adjusted volume in the specified currency.
volume_change_24h: 24 hour change in the specified currencies volume.
volume_24h_reported: Rolling 24 hour reported volume in the specified currency. This field is only returned if requested through the aux request parameter.
volume_7d: Rolling 7 day adjusted volume in the specified currency. This field is only returned if requested through the aux request parameter.
volume_7d_reported: Rolling 7 day reported volume in the specified currency. This field is only returned if requested through the aux request parameter.
volume_30d: Rolling 30 day adjusted volume in the specified currency. This field is only returned if requested through the aux request parameter.
volume_30d_reported: Rolling 30 day reported volume in the specified currency. This field is only returned if requested through the aux request parameter.
market_cap: Market cap in the specified currency.
market_cap_dominance: Market cap dominance in the specified currency.
fully_diluted_market_cap: Fully diluted market cap in the specified currency.
percent_change_1h: Percentage price increase within 1 hour in the specified currency.
percent_change_24h: Percentage price increase within 24 hour in the specified currency.
percent_change_7d: Percentage price increase within 7 day in the specified currency.
percent_change_30d: Percentage price increase within 30 day in the specified currency.
"""
cmc_trending_gainers_losers_api_doc = """
Base URL: https://pro-api.coinmarketcap.com/v1/cryptocurrency/trending/gainers-losers

Trending Gainers & Losers
Returns a paginated list of all trending cryptocurrencies, determined and sorted by the largest price gains or losses.

PARAMETERS:
start: Default is 1. Optionally offset the start (1-based index) of the paginated list of items to return. 
limit: Default is 100. Optionally specify the number of results to return. Use this parameter and the "start" parameter to determine your own pagination size.
time_period: Default is "24h". Valid values: "24h" "30d" "7d". Adjusts the overall window of time for the latest trending coins. 
convert: Optionally calculate market quotes in up to 120 currencies at once by passing a comma-separated list of cryptocurrency or fiat currency symbols. Each additional convert option beyond the first requires an additional call credit. A list of supported fiat options can be found here. Each conversion is returned in its own "quote" object.
sort: Default is "percent_change_24h". Valid values are "percent_change_24h". What field to sort the list of cryptocurrencies by.
sort_dir: Valid values are "asc" and "desc". The direction in which to order cryptocurrencies against the specified sort.

RESPONSE
id: The unique CoinMarketCap ID for this cryptocurrency.
name: The name of this cryptocurrency.
symbol: The ticker symbol for this cryptocurrency.
slug: The web URL friendly shorthand version of this cryptocurrency name.
cmc_rank: The cryptocurrency's CoinMarketCap rank by market cap.
num_market_pairs: The number of active trading pairs available for this cryptocurrency across supported exchanges.
circulating_supply: The approximate number of coins circulating for this cryptocurrency.
total_supply: The approximate total amount of coins in existence right now (minus any coins that have been verifiably burned).
market_cap_by_total_supply: The market cap by total supply. This field is only returned if requested through the aux request parameter.
max_supply: The expected maximum limit of coins ever to be available for this cryptocurrency.
date_added: Timestamp (ISO 8601) of when this cryptocurrency was added to CoinMarketCap.
tags: Array of tags associated with this cryptocurrency. Currently only a mineable tag will be returned if the cryptocurrency is mineable. Additional tags will be returned in the future.
platform: Metadata about the parent cryptocurrency platform this cryptocurrency belongs to if it is a token, otherwise null.
self_reported_circulating_supply: The self reported number of coins circulating for this cryptocurrency.
self_reported_market_cap: The self reported market cap for this cryptocurrency.
quote: A map of market quotes in different currency conversions. The default map included is USD. See the flow Quote Map Instructions.

Quote Map Instructions:
price: Price in the specified currency.
volume_24h: Rolling 24 hour adjusted volume in the specified currency.
volume_change_24h: 24 hour change in the specified currencies volume.
volume_24h_reported: Rolling 24 hour reported volume in the specified currency. This field is only returned if requested through the aux request parameter.
volume_7d: Rolling 7 day adjusted volume in the specified currency. This field is only returned if requested through the aux request parameter.
volume_7d_reported: Rolling 7 day reported volume in the specified currency. This field is only returned if requested through the aux request parameter.
volume_30d: Rolling 30 day adjusted volume in the specified currency. This field is only returned if requested through the aux request parameter.
volume_30d_reported: Rolling 30 day reported volume in the specified currency. This field is only returned if requested through the aux request parameter.
market_cap: Market cap in the specified currency.
market_cap_dominance: Market cap dominance in the specified currency.
fully_diluted_market_cap: Fully diluted market cap in the specified currency.
percent_change_1h: Percentage price increase within 1 hour in the specified currency.
percent_change_24h: Percentage price increase within 24 hour in the specified currency.
percent_change_7d: Percentage price increase within 7 day in the specified currency.
percent_change_30d: Percentage price increase within 30 day in the specified currency.
"""
cmc_trending_most_visited_api_doc = """
Base URL: https://pro-api.coinmarketcap.com/v1/cryptocurrency/trending/most-visited

Trending Most Visited
Returns a paginated list of all trending cryptocurrency market data, determined and sorted by traffic to coin detail pages.

PARAMETERS:
start: Default is 1. Optionally offset the start (1-based index) of the paginated list of items to return. 
limit: Default is 100. Optionally specify the number of results to return. Use this parameter and the "start" parameter to determine your own pagination size.
time_period: Default is "24h". Valid values: "24h" "30d" "7d". Adjusts the overall window of time for the latest trending coins. 
convert: Optionally calculate market quotes in up to 120 currencies at once by passing a comma-separated list of cryptocurrency or fiat currency symbols. Each additional convert option beyond the first requires an additional call credit. A list of supported fiat options can be found here. Each conversion is returned in its own "quote" object.

RESPONSE
id: The unique CoinMarketCap ID for this cryptocurrency.
name: The name of this cryptocurrency.
symbol: The ticker symbol for this cryptocurrency.
slug: The web URL friendly shorthand version of this cryptocurrency name.
cmc_rank: The cryptocurrency's CoinMarketCap rank by market cap.
num_market_pairs: The number of active trading pairs available for this cryptocurrency across supported exchanges.
circulating_supply: The approximate number of coins circulating for this cryptocurrency.
total_supply: The approximate total amount of coins in existence right now (minus any coins that have been verifiably burned).
market_cap_by_total_supply: The market cap by total supply. This field is only returned if requested through the aux request parameter.
max_supply: The expected maximum limit of coins ever to be available for this cryptocurrency.
date_added: Timestamp (ISO 8601) of when this cryptocurrency was added to CoinMarketCap.
tags: Array of tags associated with this cryptocurrency. Currently only a mineable tag will be returned if the cryptocurrency is mineable. Additional tags will be returned in the future.
platform: Metadata about the parent cryptocurrency platform this cryptocurrency belongs to if it is a token, otherwise null.
self_reported_circulating_supply: The self reported number of coins circulating for this cryptocurrency.
self_reported_market_cap: The self reported market cap for this cryptocurrency.
quote: A map of market quotes in different currency conversions. The default map included is USD. See the flow Quote Map Instructions.

Quote Map Instructions:
price: Price in the specified currency.
volume_24h: Rolling 24 hour adjusted volume in the specified currency.
volume_change_24h: 24 hour change in the specified currencies volume.
volume_24h_reported: Rolling 24 hour reported volume in the specified currency. This field is only returned if requested through the aux request parameter.
volume_7d: Rolling 7 day adjusted volume in the specified currency. This field is only returned if requested through the aux request parameter.
volume_7d_reported: Rolling 7 day reported volume in the specified currency. This field is only returned if requested through the aux request parameter.
volume_30d: Rolling 30 day adjusted volume in the specified currency. This field is only returned if requested through the aux request parameter.
volume_30d_reported: Rolling 30 day reported volume in the specified currency. This field is only returned if requested through the aux request parameter.
market_cap: Market cap in the specified currency.
market_cap_dominance: Market cap dominance in the specified currency.
fully_diluted_market_cap: Fully diluted market cap in the specified currency.
percent_change_1h: Percentage price increase within 1 hour in the specified currency.
percent_change_24h: Percentage price increase within 24 hour in the specified currency.
percent_change_7d: Percentage price increase within 7 day in the specified currency.
percent_change_30d: Percentage price increase within 30 day in the specified currency.
"""
cmc_metadata_api_doc = """
Base URL: https://pro-api.coinmarketcap.com/v2/cryptocurrency/info

Metadata
Returns all static metadata available for one or more cryptocurrencies. This information includes details like logo, description, official website URL, social links, and links to a cryptocurrency's technical documentation.

PARAMETERS:
id: One or more comma-separated CoinMarketCap cryptocurrency IDs. Example: "1,2"
symbol: Alternatively pass one or more comma-separated cryptocurrency symbols. Example: "BTC,ETH". At least one "id" or "slug" or "symbol" is required for this request. Please note that starting in the v2 endpoint, due to the fact that a symbol is not unique, if you request by symbol each data response will contain an array of objects containing all of the coins that use each requested symbol. The v1 endpoint will still return a single object, the highest ranked coin using that symbol.
address: Alternatively pass in a contract address. Example: "0xc40af1e4fecfa05ce6bab79dcd8b373d2e436c4e"

RESPONSE
id: The unique CoinMarketCap ID for this cryptocurrency.
name: The name of this cryptocurrency.
symbol: The ticker symbol for this cryptocurrency.
slug: The web URL friendly shorthand version of this cryptocurrency name.
logo: Link to a CoinMarketCap hosted logo png for this cryptocurrency. 64px is default size returned. Replace "64x64" in the image path with these alternative sizes: 16, 32, 64, 128, 200.
description: A CoinMarketCap supplied brief description of this cryptocurrency. This field will return null if a description is not available.
date_added: Timestamp (ISO 8601) of when this cryptocurrency was added to CoinMarketCap.
date_launched: Timestamp (ISO 8601) of when this cryptocurrency was launched.
notice: A Markdown formatted notice that may highlight a significant event or condition that is impacting the cryptocurrency or how it is displayed, otherwise null. A notice may highlight a recent or upcoming mainnet swap, symbol change, exploit event, or known issue with a particular exchange or market, for example. If present, this notice is also displayed in an alert banner at the top of the cryptocurrency's page on coinmarketcap.com.
tags: Tags associated with this cryptocurrency.
self_reported_circulating_supply: The self reported number of coins circulating for this cryptocurrency.
self_reported_market_cap: The self reported market cap for this cryptocurrency.
self_reported_tags: Array of self reported tags associated with this cryptocurrency.
infinite_supply: The cryptocurrency is known to have an infinite supply.
urls: An object containing various resource URLs for this cryptocurrency.
website: Array of website URLs.
technical_doc: Array of white paper or technical documentation URLs.
explorer: Array of block explorer URLs.
source_code: Array of source code URLs.
message_board: Array of message board URLs.
chat: Array of chat service URLs.
announcement: Array of announcement URLs.
reddit: Array of Reddit community page URLs.
twitter: Array of official twitter profile URLs.
"""
