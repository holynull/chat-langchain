# DefiLlama API

## TVL

Retrieve TVL data

### List all protocols on defillama along with their tvl

Path:`/protocols`

Example:

```shell
curl -X 'GET' \ 'https://api.llama.fi/protocols' \ -H 'accept: */*'
```

Response example:

```json
[
  {
    "id": "2269",
    "name": "Binance CEX",
    "address": null,
    "symbol": "-",
    "url": "https://www.binance.com",
    "description": "Binance is a cryptocurrency exchange which is the largest exchange in the world in terms of daily trading volume of cryptocurrencies",
    "chain": "Multi-Chain",
    "logo": "https://icons.llama.fi/binance-cex.jpg",
    "audits": "0",
    "audit_note": null,
    "gecko_id": null,
    "cmcId": null,
    "category": "CEX",
    "chains": [
      "Bitcoin",
      "Ethereum",
      "Binance",
      "Tron",
      "Arbitrum",
      "Solana",
      "Ripple",
      "Optimism",
      "Polkadot",
      "Litecoin",
      "Avalanche",
      "Polygon",
      "Algorand",
      "Base",
      "zkSync Era",
      "Fantom",
      "Aptos"
    ],
    "module": "binance/index.js",
    "twitter": "binance",
    "forkedFrom": [],
    "oracles": [],
    "listedAt": 1668170565,
    "methodology": "We collect the wallets from this binance blog post https://www.binance.com/en/blog/community/our-commitment-to-transparency-2895840147147652626. We are not counting the Binance Recovery Fund wallet",
    "slug": "binance-cex",
    "tvl": 115594281982.37428,
    "chainTvls": {
      "Fantom": 0,
      "Aptos": 0,
      "Solana": 4486744674.495709,
      "Base": 99791908.77167307,
      "zkSync Era": 6646558.077417314,
      "Optimism": 1190459136.482315,
      "Polygon": 407012527.9190255,
      "Avalanche": 430680739.138134,
      "Algorand": 121050858.98453075,
      "Arbitrum": 4940745948.133643,
      "Ripple": 1941964766.4798925,
      "Binance": 18869600436.358295,
      "Ethereum": 30085924802.289776,
      "Polkadot": 1112693734.077716,
      "Tron": 14092902668.71106,
      "Bitcoin": 37331903595.22677,
      "Litecoin": 476159627.22831035
    },
    "change_1h": 0.06352061516885499,
    "change_1d": -1.4703264587864595,
    "change_7d": -3.3879363694525466,
    "tokenBreakdowns": {},
    "mcap": null
  },
  ...
]
```

### Simplified endpoint to get current TVL of a protocol

Path:`/tvl/{protocol}`

Parameters:
- `protocol` string (required,path): protocol slug

Example:
```shell
curl -X 'GET' \
  'https://api.llama.fi/tvl/uniswap' \
  -H 'accept: */*'
```

### Get current TVL of all chains

Path:`/v2/chains`

```shell
curl -X 'GET' \
  'https://api.llama.fi/v2/chains' \
  -H 'accept: */*'
```

Response:
```json
[
  {
    "gecko_id": "harmony",
    "tvl": 4815892.656507085,
    "tokenSymbol": "ONE",
    "cmcId": "3945",
    "name": "Harmony",
    "chainId": 1666600000
  },
  ...
]
```

## Coins 

General blockchain data used by defillama and open-sourced

### Get current prices of tokens by contract address

The goal of this API is to price as many tokens as possible, including exotic ones that never get traded, which makes them impossible to price by looking at markets.

The base of our data are prices pulled from coingecko, which is then extended through multiple means:

We price all bridged tokens by using the price of the token in it's original chain, so we fetch all bridged versions of USDC on arbitrum, fantom, avax... and price all them using the price for the token on Ethereum, which we know. Right now we support 10 different bridging protocols.

We have multiple adapters to price specialized sets of tokens by running custom code:

We price yearn's yToken LPs by checking how much underlying token can be withdrawn for each LP

Aave, compound and euler LP tokens are also priced based on their relationship against underlying tokens

Uniswap, curve, balancer and stargate LPs are priced using the underlying tokens in each pair

GMX's GLP token is priced based on the value of tokens given on withdrawal (which includes calculations based on trader's PnL)

Synthetix tokens are priced using forex prices of the coin they are pegged to

For tokens that we haven't been able to price in any other way, we find the pool with most liquidity for each on uniswap, curve and serum and then use the prices provided on those exchanges.

Unlike all the other tokens, we can't confirm that these prices are correct, so we only ingest the ones that have sufficient liquidity and, even in that case, we attach a confidence value to them that is related to the depth of liquidity and which represents our confidence in the quality of each price. API consumers can choose to filter out prices with low confidence values.

Our API server is fully open source and we are constantly adding more pricing adapters, extending the amount of tokens we support.

Tokens are queried using {chain}:{address}, where chain is an identifier such as ethereum, bsc, polygon, avax... You can also get tokens by coingecko id by setting coingecko as the chain, eg: coingecko:ethereum, coingecko:bitcoin. Examples:

ethereum:0xdF574c24545E5FfEcb9a659c229253D4111d87e1
bsc:0x762539b45a1dcce3d36d080f74d1aed37844b878
coingecko:ethereum
arbitrum:0x4277f8f2c384827b5273592ff7cebd9f2c1ac258

Path:`/prices/current/{coins}`

Parameters:

- `coins` string (required,path): set of comma-separated tokens defined as {chain}:{address}
- `searchWidth` string (optional,query): time range on either side to find price data, defaults to 6 hours
  
```shell
curl -X 'GET' \
  'https://coins.llama.fi/prices/current/ethereum:0xdF574c24545E5FfEcb9a659c229253D4111d87e1,coingecko:ethereum,bsc:0x762539b45a1dcce3d36d080f74d1aed37844b878,ethereum:0xdB25f211AB05b1c97D595516F45794528a807ad8?searchWidth=4h' \
  -H 'accept: application/json'
```

Response:
```json
{
  "coins": {
    "ethereum:0xdF574c24545E5FfEcb9a659c229253D4111d87e1": {
      "decimals": 8,
      "price": 0.022053735051098835,
      "symbol": "cDAI",
      "timestamp": 0.99
    }
  }
}
```

### Get historical prices of tokens by contract address

See /prices/current for explanation on how prices are sourced.

Path:`/prices/historical/{timestamp}/{coins}`

Parameters:
- `coins` string (required,path): set of comma-separated tokens defined as {chain}:{address}
- `timestamp` number (required,path): UNIX timestamp of time when you want historical prices
- `searchWidth` string (optional,query): time range on either side to find price data, defaults to 6 hours

```shell
curl -X 'GET' \
  'https://coins.llama.fi/prices/historical/1648680149/ethereum:0xdF574c24545E5FfEcb9a659c229253D4111d87e1,coingecko:ethereum,bsc:0x762539b45a1dcce3d36d080f74d1aed37844b878,ethereum:0xdB25f211AB05b1c97D595516F45794528a807ad8?searchWidth=4h' \
  -H 'accept: application/json'
```

Response:
```json
{
  "coins": {
    "ethereum:0xdF574c24545E5FfEcb9a659c229253D4111d87e1": {
      "decimals": 8,
      "price": 0.022053735051098835,
      "symbol": "cDAI",
      "timestamp": 1648680149
    }
  }
}
```

### Get historical prices for multiple tokens at multiple different timestamps

Strings accepted by period and searchWidth: Can use regular chart candle notion like ‘4h’ etc where: W = week, D = day, H = hour, M = minute (not case sensitive)

Path:`/batchHistorical`

Parameters:
- `coins` string (required,query): object where keys are coins in the form {chain}:{address}, and values are arrays of requested timestamps
- `searchWidth` string (optional,query): time range on either side to find price data, defaults to 6 hours

```shell
curl -X 'GET' \
  'https://coins.llama.fi/batchHistorical?coins=%7B%22avax:0xb97ef9ef8734c71904d8002f8b6bc66dd9c48a6e%22:%20%5B1666876743,%201666862343%5D,%20%22coingecko:ethereum%22:%20%5B1666869543,%201666862343%5D%7D%0A&searchWidth=600' \
  -H 'accept: application/json'
```

Response:
```json
{
  "coins": {
    "avax:0xb97ef9ef8734c71904d8002f8b6bc66dd9c48a6e": {
      "symbol": "USDC",
      "prices": [
        {
          "timestamp": 1666876674,
          "price": 0.999436,
          "confidence": 0.99
        }
      ]
    }
  }
}
```

### Get percentage change in price over time

Strings accepted by period: Can use regular chart candle notion like ‘4h’ etc where: W = week, D = day, H = hour, M = minute (not case sensitive)

Path:`/percentage/{coins}`

Parameters:
- `coins` string (required,path): set of comma-separated tokens defined as {chain}:{address}
- `timestamp` number (optional,query): timestamp of data point requested, defaults to time now
- `lookForward` boolean (optional,query): whether you want the duration after your given timestamp or not, defaults to false (looking back)
- `period` string (optional,query): duration between data points, defaults to 24 hours
  
```shell
curl -X 'GET' \
  'https://coins.llama.fi/percentage/ethereum:0xdF574c24545E5FfEcb9a659c229253D4111d87e1,coingecko:ethereum,bsc:0x762539b45a1dcce3d36d080f74d1aed37844b878,ethereum:0xdB25f211AB05b1c97D595516F45794528a807ad8?timestamp=1664364537&lookForward=false&period=3w' \
  -H 'accept: application/json'
```

Response:
```json
{
  "coins": {
    "ethereum:0xdF574c24545E5FfEcb9a659c229253D4111d87e1": -2.3009954568977147
  }
}
```

### Get earliest timestamp price record for coins

Path:`/prices/first/{coins}`

Parameters:
- `coins` string (required,path): set of comma-separated tokens defined as {chain}:{address}

```shell
curl -X 'GET' \
  'https://coins.llama.fi/prices/first/ethereum:0xdF574c24545E5FfEcb9a659c229253D4111d87e1,coingecko:ethereum,bsc:0x762539b45a1dcce3d36d080f74d1aed37844b878,ethereum:0xdB25f211AB05b1c97D595516F45794528a807ad8' \
  -H 'accept: application/json'
```

Response:
```json
{
  "coins": {
    "ethereum:0xdF574c24545E5FfEcb9a659c229253D4111d87e1": {
      "price": 0.9992047673109988,
      "symbol": "HUSD",
      "timestamp": 1568883821
    }
  }
}
```

### Get the closest block to a timestamp

Runs binary search over a blockchain's blocks to get the closest one to a timestamp. Every time this is run we add new data to our database, so each query permanently speeds up future queries.

Path:`/block/{chain}/{timestamp}`

Parameters:
- `chain` string (required,path): Chain which you want to get the block from
- `timestamp` integer (required,path): UNIX timestamp of the block you are searching for
  
```shell
curl -X 'GET' \
  'https://coins.llama.fi/block/bsc/1710816458' \
  -H 'accept: application/json'
```

Response:
```json
{
  "height": 11150916,
  "timestamp": 1603964988
}
```

## Stablecoins

Data from our stablecoins dashboard

### Get current mcap sum of all stablecoins on each chain 

path:`/stablecoinchains`

```shell
curl -X 'GET' \
  'https://stablecoins.llama.fi/stablecoinchains' \
  -H 'accept: */*'
```

Response:
```json
[
  {
    "gecko_id": null,
    "totalCirculatingUSD": {
      "peggedUSD": 700850838.6129216,
      "peggedEUR": 706059.3159108019,
      "peggedVAR": 123933.55556221842,
      "peggedJPY": 0.663584
    },
    "tokenSymbol": null,
    "name": "Optimism"
  },
  {
    "gecko_id": null,
    "totalCirculatingUSD": {
      "peggedUSD": 1492984.008
    },
    "tokenSymbol": null,
    "name": "Statemine"
  },
  {
    "gecko_id": "harmony",
    "totalCirculatingUSD": {
      "peggedUSD": 8146971.423366884
    },
    "tokenSymbol": "ONE",
    "name": "Harmony"
  },
  ...
]
```

## Yields

Data from our yields/APY dashboard

### Retrieve the latest data for all pools, including enriched information such as predictions

Path:`/pools`

```shell
curl -X 'GET' \
  'https://yields.llama.fi/pools' \
  -H 'accept: */*'
```

Response:
```json
{
  "status": "success",
  "data": [
    {
      "chain": "Ethereum",
      "project": "lido",
      "symbol": "STETH",
      "tvlUsd": 33354769942,
      "apyBase": 3.125,
      "apyReward": null,
      "apy": 3.125,
      "rewardTokens": null,
      "pool": "747c1d2a-c668-4682-b9f9-296708a3dd90",
      "apyPct1D": -0.186,
      "apyPct7D": -0.461,
      "apyPct30D": -0.001,
      "stablecoin": false,
      "ilRisk": "no",
      "exposure": "single",
      "predictions": {
        "predictedClass": "Down",
        "predictedProbability": 51,
        "binnedConfidence": 1
      },
	  ...
  ]
}
```

## abi-decoder

Function and event signatures decoded

### Get the ABI for a function or event signature.

Path:`/fetch/signature`

Parameters:
- `functions` string (query): function 4 byte signatures, you can add many signatures by joining them with ','
- `events` string (query): event signatures, you can add many signatures by joining them with ','

```shell
curl -X 'GET' \
  'https://abi-decoder.llama.fi/fetch/signature?functions=0x23b872dd,0x18fccc76,0xb6b55f25,0xf5d07b60&events=0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef,0xc42079f94a6350d7e6235f29174924f928cc2ac818eb64fed8004e115fbcca67,0x4cc7e95e48af62690313a0733e93308ac9a73326bc3c29f1788b1191c376d5b6' \
  -H 'accept: */*'
```

Response:
```json
{
  "functions": {
    "0x23b872dd": [
      "gasprice_bit_ether(int128)",
      "transferFrom(address,address,uint256)",
      "watch_tg_invmru_faebe36(bool,bool,bool)"
    ],
    "0xf5d07b60": [
      "beefIn(address,uint256,address,uint256)"
    ],
    "0x18fccc76": [
      "harvest(uint256,address)"
    ],
    "0xb6b55f25": [
      "deposit(uint256)"
    ]
  },
  "events": {
    "0xc42079f94a6350d7e6235f29174924f928cc2ac818eb64fed8004e115fbcca67": "Swap(address,address,int256,int256,uint160,uint128,int24)",
    "0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef": "Transfer(address,address,uint256)",
    "0x4cc7e95e48af62690313a0733e93308ac9a73326bc3c29f1788b1191c376d5b6": "BoughtV3(bytes16,address,uint256,address,address,address,address,uint256,uint256,uint256)"
  }
}
```

### Get the verbose ABI for a function or event signature for a particular contract

Path:`/fetch/contract/{chain}/{address}`

```shell
curl -X 'GET' \
  'https://abi-decoder.llama.fi/fetch/contract/ethereum/0x02f7bd798e765369a9d204e9095b2a526ef01667?functions=0xf43f523a,0x95d89b41,0x95d89b41,0x70a08231,0x70a08231&events=0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef,0x8c5be1e5ebec7d5bd14f71427d1e84f3dd0314c0f7b2291e5b200ac8c7c3b925' \
  -H 'accept: */*'
```

## Bridges

Data from our bridges dashboard

#### List all bridges along with summaries of recent bridge volumes.

Path:`/bridges`

Parameters:
- `includeChains` boolean (query): set whether to include current previous day volume breakdown by chain

```shell
curl -X 'GET' \
  'https://bridges.llama.fi/bridges?includeChains=true' \
  -H 'accept: */*'
```

Response:
```json
{
  "bridges": [
    {
      "id": 11,
      "name": "synapse",
      "displayName": "Synapse",
      "icon": "icons:synapse",
      "volumePrevDay": 86447533.5,
      "volumePrev2Day": 60643126.5,
      "lastHourlyVolume": 195282.20835817506,
      "currentDayVolume": 81533888.03262417,
      "lastDailyVolume": 86447533.5,
      "dayBeforeLastVolume": 60643126.5,
      "weeklyVolume": 270726860.5,
      "monthlyVolume": 1043383077,
      "chains": [
        "Arbitrum",
        "Ethereum",
        "BSC",
        "Optimism",
        "Avalanche",
        "Metis",
        "Polygon",
        "Fantom",
        "Aurora",
        "Base",
        "Moonbeam",
        "Moonriver",
        "Blast"
      ],
      "destinationChain": "false"
    },
	...
  ]
}
```

### Get summary of bridge volume and volume breakdown by chain

Path:`/bridge/{id}`

Parameters:
- `id` integer (required,path): bridge ID, you can get these from /bridges

```shell
curl -X 'GET' \
  'https://bridges.llama.fi/bridge/1' \
  -H 'accept: */*'
```

Response:
```json
{
  "id": 1,
  "name": "polygon",
  "displayName": "Polygon PoS Bridge",
  "lastHourlyVolume": 0,
  "currentDayVolume": 0,
  "lastDailyVolume": 11536543,
  "dayBeforeLastVolume": 7027700,
  "weeklyVolume": 204986795,
  "monthlyVolume": 731823025,
  "lastHourlyTxs": {
    "deposits": 0,
    "withdrawals": 0
  },
  "currentDayTxs": {
    "deposits": 0,
    "withdrawals": 0
  },
  "prevDayTxs": {
    "deposits": 293,
    "withdrawals": 293
  },
  "dayBeforeLastTxs": {
    "deposits": 165,
    "withdrawals": 165
  },
  "weeklyTxs": {
    "deposits": 3428,
    "withdrawals": 3428
  },
  "monthlyTxs": {
    "deposits": 11595,
    "withdrawals": 11595
  },
  "chainBreakdown": {
    "Ethereum": {
      "lastHourlyVolume": 0,
      "currentDayVolume": 0,
      "lastDailyVolume": 5768271.5,
      "dayBeforeLastVolume": 3513850,
      "weeklyVolume": 102493397.5,
      "monthlyVolume": 365911512.5,
      "lastHourlyTxs": {
        "deposits": 0,
        "withdrawals": 0
      },
      "currentDayTxs": {
        "deposits": 0,
        "withdrawals": 0
      },
      "prevDayTxs": {
        "deposits": 185,
        "withdrawals": 108
      },
      "dayBeforeLastTxs": {
        "deposits": 91,
        "withdrawals": 74
      },
      "weeklyTxs": {
        "deposits": 1774,
        "withdrawals": 1654
      },
      "monthlyTxs": {
        "deposits": 6150,
        "withdrawals": 5445
      }
    },
    "Polygon": {
      "lastHourlyVolume": 0,
      "currentDayVolume": 0,
      "lastDailyVolume": 5768271.5,
      "dayBeforeLastVolume": 3513850,
      "weeklyVolume": 102493397.5,
      "monthlyVolume": 365911512.5,
      "lastHourlyTxs": {
        "deposits": 0,
        "withdrawals": 0
      },
      "currentDayTxs": {
        "deposits": 0,
        "withdrawals": 0
      },
      "prevDayTxs": {
        "deposits": 108,
        "withdrawals": 185
      },
      "dayBeforeLastTxs": {
        "deposits": 74,
        "withdrawals": 91
      },
      "weeklyTxs": {
        "deposits": 1654,
        "withdrawals": 1774
      },
      "monthlyTxs": {
        "deposits": 5445,
        "withdrawals": 6150
      }
    }
  },
  "destinationChain": "Polygon"
}
```

### Get historical volumes for a bridge, chain, or bridge on a particular chain

Path:`/bridgevolume/{chain}`

Parameters:
- `chain` string (required,path): chain slug, you can get these from /chains. Call also use 'all' for volume on all chains.
- `id` integer (query): bridge ID, you can get these from /bridges

```shell
curl -X 'GET' \
  'https://bridges.llama.fi/bridgevolume/Ethereum?id=5' \
  -H 'accept: */*'
```

Response:
```json
[
  {
    "date": "1666396800",
    "depositUSD": 2769237,
    "withdrawUSD": 4515497,
    "depositTxs": 327,
    "withdrawTxs": 259
  },
  ...
]
```

### Get a 24hr token and address volume breakdown for a bridge

Path:`/bridgedaystats/{timestamp}/{chain}`

Parameters:
- `timestamp` integer (required,path): Unix timestamp. Data returned will be for the 24hr period starting at 00:00 UTC that the timestamp lands in.
- `chain` sting (required,path): chain slug, you can get these from /chains.
- `id` integer (query): bridge ID, you can get these from /bridges   

```shell
curl -X 'GET' \
  'https://bridges.llama.fi/bridgedaystats/1667304000/Ethereum?id=5' \
  -H 'accept: */*'
```

Response:
```json
{
  "date": 1667260800,
  "totalTokensDeposited": {},
  "totalTokensWithdrawn": {},
  "totalAddressDeposited": {},
  "totalAddressWithdrawn": {}
}
```

### Get all transactions for a bridge within a date range

Path:`/transactions/{id}`

Parameters:
- `id` integer (required,path): bridge ID, you can get these from /bridges
- `starttimestamp` integer (query): start timestamp (Unix Timestamp) for date range
- `endtimestamp` integer (query): end timestamp (Unix timestamp) for date range
- `sourcechain` string (query): Returns only transactions that are bridging from the specified source chain.
- `address` string (query): Returns only transactions with specified address as "from" or "to". Addresses are quried in the form {chain}:{address}, where chain is an identifier such as ethereum, bsc, polygon, avax... 
- `limit` integer (query): limit to number of transactions returned, maximum is 6000

```shell
curl -X 'GET' \
  'https://bridges.llama.fi/transactions/1?starttimestamp=1667260800&endtimestamp=1667347200&sourcechain=Polygon&address=ethereum:0x69b4B4390Bd1f0aE84E090Fe8af7AbAd2d95Cc8E&limit=200' \
  -H 'accept: */*'
```

Response:
```json
[
  {
    "tx_hash": "0x7a7e54dce4a9f2447742c25b9090f504909e63769318ac63b759fb178f6ce1dd",
    "ts": "2022-11-01T21:03:35.000Z",
    "tx_block": 15877738,
    "tx_from": "0x8484Ef722627bf18ca5Ae6BcF031c23E6e922B30",
    "tx_to": "0x69b4B4390Bd1f0aE84E090Fe8af7AbAd2d95Cc8E",
    "token": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
    "amount": "1890000000000000000",
    "chain": "ethereum",
    "bridge_name": "polygon",
    "usd_value": null,
    "sourceChain": "polygon"
  },
  {
    "tx_hash": "0xa75697c79ff728d9f912b5e95987bfe4b4b99252289bf75ef8e69560318d845f",
    "ts": "2022-11-01T20:03:35.000Z",
    "tx_block": 15877442,
    "tx_from": "0x8484Ef722627bf18ca5Ae6BcF031c23E6e922B30",
    "tx_to": "0x69b4B4390Bd1f0aE84E090Fe8af7AbAd2d95Cc8E",
    "token": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
    "amount": "10000000000000000",
    "chain": "ethereum",
    "bridge_name": "polygon",
    "usd_value": null,
    "sourceChain": "polygon"
  }
]
```

## 

