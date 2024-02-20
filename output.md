# Get supported chains

- **GET** `https://api.0xscope.com/v2/basic/chains`

Returns the list of current support chains.

## Sample Request

```bash
curl --request GET \
     --url https://api.0xscope.com/v2/basic/chains \
     --header 'API-KEY: your_api_key' \
     --header 'accept: */*'
```

## Sample Response

```json
{
  "code": 0,
  "data": [
    "ethereum",
    "bsc"
  ],
  "uuid": 1631546627552874500
}
```

This information provides guidance on how to make a request to the API endpoint to get a list of supported chains and what response to expect.

# Get credits remaining

- **HTTP Method:** GET
- **URL:** `https://api.0xscope.com/v2/basic/credits`

Returns the users' remaining credits.

## Sample Request

```curl
curl --request GET \
     --url https://api.0xscope.com/v2/basic/credits \
     --header 'API-KEY: your_api_key' \
     --header 'accept: */*'
```

## Sample Response

```json
{
  "code": 0,
  "data": 2999671,
  "uuid": 1631549254684545000
}
```

# Get address portfolio on all supported chains

**GET** `https://api.0xscope.com/v2/address/portfolio`

Returns the portfolio of the address on all supported chains.

## Sample Request

```curl
curl --request GET \
     --url 'https://api.0xscope.com/v2/address/portfolio?address=0x690b9a9e9aa1c9db991c7721a92d351db4fac990' \
     --header 'API-KEY: your_api_key' \
     --header 'accept: */*'
```

## Sample Response

```json
{
    "code":0,
    "message":"ok",
    "data":[
        {
            "chain":"eth",
            "time_at":1615386222,
            "token_id":"0xb3863e02d6930762933f672ca134c1ccecd0d413",
            "name":"Dog Token",
            "symbol":"DOG",
            "price":0.0000000027610551384550184,
            "amount":96.90407247305971,
            "value":0.0000000027
        },
        {
            "chain":"bsc",
            "time_at":1615386222,
            "token_id":"0xdf574c24545e5ffecb9a659c229253d4111d87e1",
            "name":"HUSD",
            "symbol":"HUSD",
            "price":0.15,
            "amount":100,
            "value":15
        }
        ...
    ]
}
```

# Get one specific token balance of an address

**GET** `https://api.0xscope.com/v2/address/tokenBalance`

Returns the balance of the user in one specific token

## Sample Request

```curl
curl --request GET \
     --url 'https://api.0xscope.com/v2/address/tokenBalance?address=0x690b9a9e9aa1c9db991c7721a92d351db4fac990&chain=ethereum&token_address=0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48' \
     --header 'API-KEY: YOUR-API_KEY' \
     --header 'accept: */*'
```

## Sample Response

```json
{
  "code": 0,
  "data": {
    "chain": "ethereum",
    "time_at": 1683860337,
    "token_id": "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48",
    "name": "USD Coin",
    "symbol": "USDC",
    "price": 1,
    "amount": 0.02,
    "value": 0.02
  },
  "uuid": 1656856457926541300
}
```

This page provides detailed documentation on how to use the API to get the balance of a specific token held by an address on the Ethereum chain.

# Get all the identity tag of an address

**GET** `https://api.0xscope.com/v2/address/identityTag`

Get all the identity tag of an eoa/contract address.

## Sample Request

```curl
curl --request GET \
     --url 'https://api.0xscope.com/v2/address/identityTag?address=0x690b9a9e9aa1c9db991c7721a92d351db4fac990&chain=ethereum' \
     --header 'API-KEY: your-api-key' \
     --header 'accept: */*'
```

## Sample Response

```json
{
  "code": 0,
  "data": [
    {
      "address": "0x690b9a9e9aa1c9db991c7721a92d351db4fac990",
      "tag": "builder0x69",
      "type": "others",
      "subgroup": "mev-builder"
    }
  ],
  "uuid": 1656856982415868000
}
```

# Get ENS by address, or get address by ENS

- **HTTP Method:** GET
- **URL:** `https://api.0xscope.com/v2/address/ENS`

## Sample Request

```curl
curl --request GET \
     --url 'https://api.0xscope.com/v2/address/ENS?address=0x690b9a9e9aa1c9db991c7721a92d351db4fac990&chain=ethereum' \
     --header 'API-KEY: your-api-key' \
     --header 'accept: */*'
```

## Sample Response

```json
{
  "code": 0,
  "data": "builder0x69.eth",
  "uuid": 1656857255674773500
}
```

# Get social media info of an address

**GET** `https://api.0xscope.com/v2/address/socialMedia`

Get social media info of an address.

## Sample Request

```curl
curl --request GET \
     --url 'https://api.0xscope.com/v2/address/socialMedia?address=0xb6f165a70e2a394f2981ab2f0fa953c03f1871d4&chain=ethereum' \
     --header 'API-KEY: your-api-key' \
     --header 'accept: */*'
```

## Sample Response

```json
{
  "code": 0,
  "data": [
    {
      "address": "0xb6f165a70e2a394f2981ab2f0fa953c03f1871d4",
      "twitter": "PavelSolomatin9",
      "debankAccount": "Pavel",
      "github": null,
      "isMirrorAuthority": null
    }
  ],
  "uuid": 1656857521312628700
}
```

# Get token transfers of an address

**GET** `https://api.0xscope.com/v2/address/tokenTransfers`

Get token transfers of an address.

## Sample Request

```curl
curl --request GET \
     --url 'https://api.0xscope.com/v2/address/tokenTransfers?address=0x690b9a9e9aa1c9db991c7721a92d351db4fac990&chain=ethereum&token_address=0xdac17f958d2ee523a2206206994597c13d831ec7&limit=10&page=1' \
     --header 'API-KEY: your-api-key' \
     --header 'accept: */*'
```

## Sample Response

```json
{
  "code": 0,
  "data": {
    "total": 9,
    "limit": 10,
    "page": 1,
    "rows": [
      {
        "txhash": "0x608b8281bfb40047cb5fb977618a4717d0133d9b54af1c916f98192ebd5fcae2",
        "timestamp": "2023-01-16 09:16:47",
        "from": "0x690b9a9e9aa1c9db991c7721a92d351db4fac990",
        "to": "0xe1f3ce3b0bff3ae9162d86de4d971b639eb71127",
        "token_address": "0xdac17f958d2ee523a2206206994597c13d831ec7",
        "token_name": "Tether USD",
        "token_symbol": "USDT",
        "token_decimal": "6",
        "token_valueUSD": 0
      },
      {
        "txhash": "0x4fb0c30a501e56dc123884fb9b87d32c7f3df7724b37df9f02eddd082a545732",
        "timestamp": "2023-01-16 09:16:35",
        "from": "0x690b9a9e9aa1c9db991c7721a92d351db4fac990",
        "to": "0x3842b718012e26c1cfb32e6d2978394cc6b19297",
        "token_address": "0xdac17f958d2ee523a2206206994597c13d831ec7",
        "token_name": "Tether USD",
        "token_symbol": "USDT",
        "token_decimal": "6",
        "token_valueUSD": 0
      },
      {
        "txhash": "0x6744ffd378fb30c9170b4f6145c74efaf060969761b0ed0744acab26c0814ffa",
        "timestamp": "2023-01-16 02:31:23",
        "from": "0x690b9a9e9aa1c9db991c7721a92d351db4fac990",
        "to": "0xe1ee1cd28caabee6c2c6c92460af567c7999cacf",
        "token_address": "0xdac17f958d2ee523a2206206994597c13d831ec7",
        "token_name": "Tether USD",
        "token_symbol": "USDT",
        "token_decimal": "6",
        "token_valueUSD": 0
      }
    ]
  },
  "uuid": 1656857724413411300
}
```

Please note that the sample response is truncated for brevity.

# Get transactions of an address

**Method**: GET

**URL**: `https://api.0xscope.com/v2/address/transactions`

**Description**: 
Get transactions of an address.

## Sample Request

```curl
curl --request GET \
     --url 'https://api.0xscope.com/v2/address/transactions?address=0x690b9a9e9aa1c9db991c7721a92d351db4fac990&chain=ethereum&limit=10&page=1' \
     --header 'API-KEY: your-api-key' \
     --header 'accept: */*'
```

## Sample Response

```json
{
  "code": 0,
  "data": {
    "total": 76695,
    "limit": 10,
    "page": 1,
    "rows": [
      {
        "txhash": "0x3d0c68d1dabd75ef547847475e4f14a8916f9cb7f7126ca430e532be9c4f25e7",
        "timestamp": 1683860675,
        "from": "0x0000000000e3c7175357aae6fce025be01aa13ca",
        "to": "0x690b9a9e9aa1c9db991c7721a92d351db4fac990",
        "value": [
          {
            "amount": 0.00001030747850452,
            "amountString": "0.00001030747850452",
            "tokenAddress": "0x0000000000000000000000000000000000000000",
            "symbol": "ETH",
            "tokenType": null
          }
        ],
        "method_decoded": "0x641b9274"
      },
      {
        "txhash": "0x55fcc129982a8c5df71e2f2ce1d5e4bb03ef25d9e95dff4a80a4e441d4ed4cc5",
        "timestamp": 1683860675,
        "from": "0x690b9a9e9aa1c9db991c7721a92d351db4fac990",
        "to": "0x388c818ca8b9251b393131c08a736a67ccb19297",
        "value": [
          {
            "amount": -1.644178608521564,
            "amountString": "-1.644178608521564",
            "tokenAddress": "0x0000000000000000000000000000000000000000",
            "symbol": "ETH",
            "tokenType": null
          }
        ],
        "method_decoded": "0x"
      },
      {
        "txhash": "0x607a2a62e100ec855856c53be49d6480cb4d45d949819eaeab8faa95d9c76f91",
        "timestamp": 1683860627,
        "from": "0x690b9a9e9aa1c9db991c7721a92d351db4fac990",
        "to": "0x388c818ca8b9251b393131c08a736a67ccb19297",
        "value": [
          {
            "amount": -0.3607678603042195,
            "amountString": "-0.3607678603042195",
            "tokenAddress": "0x0000000000000000000000000000000000000000",
            "symbol": "ETH",
            "tokenType": null
          }
        ],
        "method_decoded": "0x"
      },
      ...
    ]
  },
  "uuid": 1656858124629704700
}
```

This response includes a sample of transaction data for a given address, including transaction hashes, timestamps, from/to addresses, amounts, and the associated token information.

# Get NFT transactions of an address

## Endpoint
GET `https://api.0xscope.com/v2/address/NFTtransactions`

This API endpoint retrieves NFT transactions associated with a given address.

### Sample Request

```bash
curl --request GET \
     --url 'https://api.0xscope.com/v2/address/NFTtransactions?address=0x097703c488ecc613b6b6bfd419893be1625d28ba&chain=ethereum&limit=10&page=1' \
     --header 'API-KEY: your-api-key' \
     --header 'accept: */*'
```

### Sample Response

```json
{
  "code": 0,
  "data": {
    "total": 2,
    "limit": 10,
    "page": 1,
    "rows": [
      {
        "txhash": "0x15b1711613921f9d3b10f46dec9146b8aa5f398bcd793ae82f64f2c5bfb75924",
        "timestamp": 1681449515,
        "action": "buy",
        "from": "0x0bfff40545a2250c3f11993e7b75dbbcb11e36ac",
        "to": "0x097703c488ecc613b6b6bfd419893be1625d28ba",
        "quantity": "Single",
        "token_contract_address": "0xbc4ca0eda7647a8ab7c2061c2e118a18a936f13d",
        "token_id": "5992",
        "token_name": "",
        "price": 58.9
      },
      {
        "txhash": "0x94c6adb3b4f23fcf01df4bbbaf6728bc65506fbc53bf1159c1f5b6060a09e0b7",
        "timestamp": 1681447739,
        "action": "sell",
        "from": "0x097703c488ecc613b6b6bfd419893be1625d28ba",
        "to": "0xa3e0c08ac55c3da4d19028876ad305119062cf71",
        "quantity": "Single",
        "token_contract_address": "0xbc4ca0eda7647a8ab7c2061c2e118a18a936f13d",
        "token_id": "390",
        "token_name": "",
        "price": 53.63
      }
    ]
  },
  "uuid": 1656858656798802000
}
```

This response provides details about NFT transactions, including the transaction hash, timestamp, action (buy or sell), addresses involved, quantity, token contract address, token ID, token name (if available), and the price at which the transaction occurred.

# get detail of the token

**GET** `https://api.0xscope.com/v2/token/detail`

get detail of the token

### Sample Request

```curl
curl --request GET \
     --url 'https://api.0xscope.com/v2/token/detail?token_address=0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48&chain=ethereum' \
     --header 'API-KEY: your-api-key' \
     --header 'accept: */*'
```

### Sample Response

```json
{
  "code": 0,
  "data": {
    "token_address": "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48",
    "token_name": "USD Coin",
    "token_symbol": "USDC",
    "token_decimals": "6",
    "chain": "ethereum",
    "is_erc20": true,
    "is_erc721": false,
    "is_erc1155": false,
    "deployer": "0x95ba4cf87d6723ad9c0db21737d862be80e93911",
    "txhash": "0xe7e0fe390354509cd08c9a0168536938600ddc552b3f7cb96030ebef62e75895",
    "block_number": "6082465",
    "block_timestamp": "1533324504"
  },
  "uuid": 1656859840133595100
}
```

# get holders count of the token

**GET** `https://api.0xscope.com/v2/token/holdersCount`

Retrieves the count of holders for a specified token.

## Sample Request

```curl
curl --request GET \
     --url 'https://api.0xscope.com/v2/token/holdersCount?token_address=0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48&chain=ethereum' \
     --header 'API-KEY: your-api-key' \
     --header 'accept: */*'
```

## Sample Response

```json
{
  "code": 0,
  "data": 1690552,
  "uuid": 1656860114080366600
}
```

This API endpoint provides the number of holders for a given token on the specified blockchain network.

# get transfers of the token

**GET** `https://api.0xscope.com/v2/token/transfers`

## Sample Request

```curl
curl --request GET \
     --url 'https://api.0xscope.com/v2/token/transfers?token_address=0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48&chain=ethereum&limit=10&page=1' \
     --header 'API-KEY: your-api-key' \
     --header 'accept: */*'
```

## Sample Response

```json
{
  "code": 0,
  "data": [
    {
      "timestamp": "2023-05-12 03:17:11",
      "txhash": "0x8f366436423b29825033b58244675f79846623bbf2ccb88a36f5ad4c8f988b78",
      "from": "0xe34fc36e80816df44df3fa78e5e0525d49002f71",
      "to": "0x512f4514375909aec1d164da7059fd52abca9500",
      "value": 14686.959494,
      "token_price": 0.996334
    },
    {
      "timestamp": "2023-05-12 03:17:11",
      "txhash": "0xacc7602ad3b549e04ffa5b2d7e920c303fc7aca5e3f31462478c55ec2ce73bb0",
      "from": "0x88e6a0c2ddd26feeb64f039a2c41296fcb3f5640",
      "to": "0x289aa48798649b398150a2c5e92cece34fa75daf",
      "value": 15849.594504260944,
      "token_price": 0.996334
    },
    {
      "timestamp": "2023-05-12 03:17:23",
      "txhash": "0xf94491f22b80243c3de358a1802ecf5216124e69efe29eebda486d1ab3601970",
      "from": "0x88ad09518695c6c3712ac10a214be5109a655671",
      "to": "0x65a8f07bd9a8598e1b5b6c0a88f4779dbc077675",
      "value": 29890.02,
      "token_price": 0.996334
    },
    {
      "timestamp": "2023-05-12 03:17:35",
      "txhash": "0x8eb253333eb46b0d68e7e2c34bb087fa8748ba8b3597ec9701977c7bc3442ea4",
      "from": "0x88e6a0c2ddd26feeb64f039a2c41296fcb3f5640",
      "to": "0xdef171fe48cf0115b1d80b88dc8eab59176fee57",
      "value": 3086.196028640102,
      "token_price": 0.996334
    },
    ...
  ],
  "uuid": 1656861356454183000
}
```

This document outlines the API endpoint to get transfers of a specified token, including a sample request using cURL and a sample response in JSON format.

# get top 1000 holders of the token

**GET** `https://api.0xscope.com/v2/token/topHolders`

This API endpoint retrieves the top 1000 holders of a specific token.

## Sample Request

```curl
curl --request GET \
     --url 'https://api.0xscope.com/v2/token/topHolders?token_address=0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48&chain=ethereum' \
     --header 'API-KEY: your-api-key' \
     --header 'accept: */*'
```

## Sample Response

```json
{
  "code": 0,
  "data": [
    {
      "address": "0x0a59649758aa4d66e25f08dd01271e891fe52199",
      "balance": 1664321254.005198,
      "percentage": 5.549526383572078
    },
    {
      "address": "0xcee284f754e854890e311e3280b767f80797180d",
      "balance": 1317019525.863523,
      "percentage": 4.391480664487376
    },
    {
      "address": "0x47ac0fb4f2d84898e4d9e7b4dab3c24507a6d503",
      "balance": 772999999.84,
      "percentage": 2.577497513349604
    },
    {
      "address": "0x40ec5b33f54e0e8a33a975908c5ba1c14e5bbbdf",
      "balance": 636196858.636452,
      "percentage": 2.121340001909054
    },
    ...
  ]
}
```

Please replace `'API-KEY: your-api-key'` with your actual API key when making the request.

# get volume of the token deposit to cex hourly

**GET** `https://api.0xscope.com/v2/token/cexDeposit`

This API endpoint retrieves the volume of a specific token deposited to centralized exchanges (CEX) on an hourly basis.

### Sample Request

```curl
curl --request GET \
     --url 'https://api.0xscope.com/v2/token/cexDeposit?token_address=0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48&chain=ethereum' \
     --header 'API-KEY: your-api-key' \
     --header 'accept: */*'
```

### Sample Response

```json
{
  "code": 0,
  "data": [
    {
      "timestamp": "2023-05-11 14:00:00",
      "volume": 3000,
      "cex_name": "AscendEX"
    },
    {
      "timestamp": "2023-05-11 16:00:00",
      "volume": 4194.766005,
      "cex_name": "Bitget"
    },
    ...
    {
      "timestamp": "2023-05-11 18:00:00",
      "volume": 180,
      "cex_name": "bibox"
    },
    {
      "timestamp": "2023-05-11 19:00:00",
      "volume": 2180510.794586,
      "cex_name": "binance"
    },
    ...
  ],
  "uuid": 1656862678247145500
}
```

This response includes the timestamp, volume deposited, and the name of the CEX for each entry. The sample showcases data from various exchanges, such as AscendEX, Bitget, bibox, and binance, among others, providing insights into the hourly deposit volumes of a specified token across different platforms.

# Get Volume of the Token Withdraw from CEX Hourly

## GET
**URL**: `https://api.0xscope.com/v2/token/cexWithdraw`

**Description**: Get volume of the token withdraw from CEX hourly.

### Sample Request

```curl
curl --request GET \
     --url 'https://api.0xscope.com/v2/token/cexWithdraw?token_address=0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48&chain=ethereum' \
     --header 'API-KEY: your-api-key' \
     --header 'accept: */*'
```

### Sample Response

```json
{
  "code": 0,
  "data": [
    {
      "timestamp": "2023-05-11 03:00:00",
      "volume": 1034.9234,
      "cex_name": "AscendEX"
    },
    {
      "timestamp": "2023-05-11 16:00:00",
      "volume": 464,
      "cex_name": "AscendEX"
    },
    ...
    {
      "timestamp": "2023-05-11 21:00:00",
      "volume": 26768,
      "cex_name": "WhiteBIT"
    }
  ],
  "uuid": 1656863004404613000
}
```

This output shows an array of withdrawal volumes for various CEXs, including the timestamp, volume, and CEX name.

# get amount of the token held by cex address

**GET** `https://api.0xscope.com/v2/token/cexHolding`

Description: get amount of the token held by cex address

## Sample Request

```curl
curl --request GET \
     --url 'https://api.0xscope.com/v2/token/cexHolding?token_address=0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48&chain=ethereum' \
     --header 'API-KEY: your-api-key' \
     --header 'accept: */*'
```

## Sample Response

```json
{
  "code": 0,
  "data": [
    {
      "timestamp": "2023-05-11",
      "holding": 913175381.854418,
      "cex_name": "Binance"
    },
    {
      "timestamp": "2023-05-11",
      "holding": 245650822.46487698,
      "cex_name": "Crypto.com"
    },
    {
      "timestamp": "2023-05-11",
      "holding": 202942366.146464,
      "cex_name": "Coinbase"
    },
    {
      "timestamp": "2023-05-11",
      "holding": 135018254.179354,
      "cex_name": "Kraken"
    },
    {
      "timestamp": "2023-05-11",
      "holding": 112903535.456743,
      "cex_name": "OKX"
    },
    {
      "timestamp": "2023-05-11",
      "holding": 97311119.55940899,
      "cex_name": "bitget"
    },
    {
      "timestamp": "2023-05-11",
      "holding": 48347580.74227,
      "cex_name": "Kucoin"
    },
    {
      "timestamp": "2023-05-11",
      "holding": 37458441.948800996,
      "cex_name": "Deribit"
    },
    {
      "timestamp": "2023-05-11",
      "holding": 31103028.375804998,
      "cex_name": "Bybit"
    },
    {
      "timestamp": "2023-05-11",
      "holding": 25883573.958800003,
      "cex_name": "Bitfinex"
    }
  ],
  "uuid": 1656863210965696500
}
```

# get supported projects

**GET** `https://api.0xscope.com/v2/project/supported`

get supported projects

## Sample Request

```curl
curl --request GET \
     --url 'https://api.0xscope.com/v2/project/supported?chain=ethereum&limit=10&page=1' \
     --header 'API-KEY: your-api-key' \
     --header 'accept: */*'
```

## Sample Response

```json
{
  "code": 0,
  "data": {
    "total": 2588,
    "page": 1,
    "limit": 10,
    "rows": [
      {
        "project_id": "5eth",
        "project_name": "5eth"
      },
      {
        "project_id": "acrocc_v2",
        "project_name": "Across V2"
      },
      {
        "project_id": "airswap",
        "project_name": "AirSwap"
      },
      {
        "project_id": "baex",
        "project_name": "baex"
      },
      {
        "project_id": "battle-festival-pre-sale",
        "project_name": "battle festival pre sale"
      },
      {
        "project_id": "bet100",
        "project_name": "bet100"
      },
      {
        "project_id": "blocklords",
        "project_name": "blocklords"
      },
      {
        "project_id": "bloxmove",
        "project_name": "BloXmove"
      },
      {
        "project_id": "brewlabs",
        "project_name": "Brew Labs"
      },
      {
        "project_id": "chic-cow-bullzz",
        "project_name": "chic cow bullzz"
      }
    ]
  },
  "uuid": 1656863852572573700
}
```

# get detail of the project

Method: `GET`  
URL: `https://api.0xscope.com/v2/project/detail`

## Sample Request

```curl
curl --request GET \
     --url 'https://api.0xscope.com/v2/project/detail?project_id=anyswap&chain=ethereum' \
     --header 'API-KEY: your-api-key' \
     --header 'accept: */*'
```

## Sample Response

```json
{
  "code": 0,
  "data": {
    "website": "https://anyswap.exchange/",
    "twitter": "https://twitter.com/anyswapnetwork",
    "github": "https://github.com/anyswap",
    "maintoken": "0xf99d58e463a2e07e5692127302c20a191861b4d6",
    "categorys": [
      "DEX Aggregator"
    ],
    "contracts": [
      "0xf99d58e463a2e07e5692127302c20a191861b4d6",
      "0xad2c1d2a9a599eef950f5baf6830d68e2be34d38",
      "0xbbfe35115d20407913f8b057ea0b375134d86c8a",
      "0xddfceafe8a92f015a07b3ab5c4ffe3fe0e03fe1c",
      "0xb622499e750d26e35601671581032efa7a12c1dc",
      "0x3a326acccba6f61ad9c55d3f78c14a6d3860bc49",
      "0x9e38909d4f62353a58a60501b6af7911392839b2",
      "0x4d00cc3b309170888ae2bc43859f4c4dc5143711",
      "0xf0459ecd5fa4e7e342664ef532a1addec6c2dde4",
      "0x8d419c5b95b8394dbca99af33101863f50e72fc2",
      "0x2296c4a9186b823db1612e831808536ed451cbbe",
      "0x08236943b93566e35d5922a6a767e570e836ce15",
      "0x3367e581f8a431a4f6f3ede5da657d97ac36b076",
      "0x7ba4f6dc65170d3affa04eb88221dde445a7af89",
      "0x52c373b3d11fcf04221a27ba2aaf37202006142f",
      "0xb63d5b98fa56c1a2e3b4ec7c41e38b2cf7d6dc12",
      "0x71035dea521e651e53794be87b1d0785e5c9a6aa",
      "0x1d396c3fc33a44e106665fc45ca39b3042120241",
      "0x7b000a7fb91bab4dfd525d284d3725a7b5ccc204",
      "0x27fe7455055d5dfc1559f3b5818734f701d1b48a"
    ]
  },
  "uuid": 1735180060044583000
}
```

# get tvl of the project

**GET** `https://api.0xscope.com/v2/project/tvl`

get tvl of the project

## Sample Request

```curl
curl --request GET \
     --url 'https://api.0xscope.com/v2/project/tvl?project_id=uniswap-v2&chain=ethereum&date=2023-04-23' \
     --header 'API-KEY: your-api-key' \
     --header 'accept: */*'
```

## Sample Response

```json
{
  "code": 0,
  "data": "1167465179.00000000",
  "uuid": 1656864202490773500
}
```

# get daily active address of the project

- **GET**: `https://api.0xscope.com/v2/project/activeAddress`

This API endpoint retrieves the daily active address count of the project.

## Sample Request

```curl
curl --request GET \
     --url 'https://api.0xscope.com/v2/project/activeAddress?project_id=uniswap-v2&chain=ethereum&date=2023-04-23' \
     --header 'API-KEY: your-api-key' \
     --header 'accept: */*'
```

## Sample Response

```json
{
  "code": 0,
  "data": 7073,
  "uuid": 1656864362826432500
}
```

This endpoint returns the number of daily active addresses for a specified project, chain, and date.

# get daily active entity of the project

**GET** `https://api.0xscope.com/v2/project/activeEntity`

get daily active entity of the project

## Sample Request

```curl
curl --request GET \
     --url 'https://api.0xscope.com/v2/project/activeEntity?project_id=uniswap-v2&chain=ethereum&date=2023-04-23' \
     --header 'API-KEY: your-api-key' \
     --header 'accept: */*'
```

## Sample Response

```json
{
  "code": 0,
  "data": 6247,
  "uuid": 1656864485019091000
}
```

# Get daily new address of the project

**GET** `https://api.0xscope.com/v2/project/newAddress`

Gets daily new address of the project.

## Sample Request

```curl
curl --request GET \
     --url 'https://api.0xscope.com/v2/project/newAddress?project_id=uniswap-v2&chain=ethereum&date=2023-04-23' \
     --header 'API-KEY: your-api-key' \
     --header 'accept: */*'
```

## Sample Response

```json
{
  "code": 0,
  "data": 1621,
  "uuid": 1656864618259546000
}
```

# get daily new entity of the project

- **HTTP Method**: GET
- **URL**: `https://api.0xscope.com/v2/project/newEntity`

## Sample Request

```curl
curl --request GET \
     --url 'https://api.0xscope.com/v2/project/newEntity?project_id=uniswap-v2&chain=ethereum&date=2023-04-23' \
     --header 'API-KEY: your-api-key' \
     --header 'accept: */*'
```

## Sample Response

```json
{
  "code": 0,
  "data": 1534,
  "uuid": 1656864758437380000
}
```

This content gives a brief overview of how to make a GET request to `https://api.0xscope.com/v2/project/newEntity` and provides a sample request and response for obtaining the daily new entity of a project.

# get related addresses

- **GET** `https://api.0xscope.com/v2/entity/relatedAddress`

Returns a batch of addresses belonging to the same entity as the input address.

## Sample Request

```curl
curl --request GET \
     --url 'https://api.0xscope.com/v2/entity/relatedAddress?address=0x934b510d4c9103e6a87aef13b816fb080286d649&chain=ethereum' \
     --header 'API-KEY: your-api-key' \
     --header 'accept: */*'
```

## Sample Response

```json
{
  "code": 0,
  "data": [
    {
      "address": "0x172059839d80773ec8617c4cb33835175d364cee",
      "certainty": 9,
      "description": [
        "Multiple Transactions between address",
        "Possible Gas provider",
        "Deposited funds to same CEX deposit address",
        "Possible Assets Transfer"
      ]
    },
    {
      "address": "0x7cbba07e31dc7b12bb69a1209c5b11a8ac50acf5",
      "certainty": 9,
      "description": [
        "Multiple Transactions between address",
        "Possible Gas provider",
        "Deposited funds to same CEX deposit address",
        "Possible Assets Transfer"
      ]
    },
    // Additional data omitted for brevity
  ],
  "uuid": 1656866963588513800
}
```

This response includes a list of addresses related to the input address, along with a certainty level and descriptions detailing the reasons for the connection between the addresses.

# Get reasons why 2 addresses are connected

**GET** `https://api.0xscope.com/v2/entity/relatedReason`

Returns the reason path why 2 addresses are connected.

## Sample Request

```curl
curl --request GET \
     --url 'https://api.0xscope.com/v2/entity/relatedReason?address=0x934b510d4c9103e6a87aef13b816fb080286d649&relatedAddress=0xaab900656d7f37ae675f35560f163e2681e38b8a&chain=ethereum' \
     --header 'API-KEY: your-api-key' \
     --header 'accept: */*'
```

## Sample Response

```json
{
  "code": 0,
  "data": {
    "total": 3,
    "rows": [
      {
        "connectionType": "Deposited funds to same CEX deposit address",
        "proof": [
          "0xfae5fac388234a675cbbbc13eb5399b3dffc2a135e7661d0c36eec1161054899",
          "0x42b505e1b3937e24b6ac3cbbfe0a5eb06b915249ca3f5e93c602a76844fa1f86",
          "0xe98b993376670a737514127f9df424ef9563b9f39fded736573f92527d7e23e6",
          "0xa24fcc9669418e7c17adbaa2c9e78610cec799eab98f21b780b14190d85ded5c",
          "0xac0a2bf01fe37b7e04b761e029a79240341334e31075c1c50a582aee561e7b0d",
          "0x6631c607e7c7020b6cc79bb15cb1475cf023cf1b8aa314789d8d1f6f724d1f57"
        ]
      },
      {
        "connectionType": "Multiple Transactions between address",
        "proof": [
          "0xe88f5f727771c5518eda472e312dbc04efa2c017439010b4a6ac823a0cea4269",
          "0x1b05f5902ad3791c579caa31f1f74cf11bf95f216b3e023a0bcc6de747624c1a",
          "0x42800c77f79652f324cb05ad6fa06837b04f1dbad4e61f37ad7fa2f0d757f696",
          "0x1bd7226cad8393de5d9ff31b6a3872f317351616abb4ce752d8b3a2aca78b596",
          "0x5e0de2a86d084aedafa512180c2e34548ad88d2126a12652687b4cae0b40ac58",
          "0x322a2de7a9147e1e4779f6f193ca7a32d797230d378a3ba00e6b37c6187efcac",
          "0x39e0825dd903fc7ec10d9352a49384569721c401ed146ade7ceac381bab472c2",
          "0x37eb295aa8ce3ced8ae11d373eba6c85571e0cd1ef72a8e29d48c1ca927afebc",
          "0x74c222672f79643c2e0925b8f539f13c30b1aec749fb56995beb1160ab8efb5f",
          "0x3a08555b2c07b5494a7324ec455bb743037613fccdf51b42e97bec59ab4213e4",
          "0x0d864d9c10d7a8e06ba7f8bd4b16fc585839cd0ecb9a97259a02b69b252ab57c"
        ]
      },
      {
        "connectionType": "Possible Gas provider",
        "proof": [
          "0x1b05f5902ad3791c579caa31f1f74cf11bf95f216b3e023a0bcc6de747624c1a"
        ]
      }
    ]
  },
  "uuid": 1656867198138187800
}
```

The content above provides detailed information about how to make a request to the API to get reasons why two addresses are connected, along with a sample request and response.

# Divide Addresses into Different Entities

**POST** `https://api.0xscope.com/v2/entity/clusters`

Divide input addresses into different entities.

## Sample Request

```curl
curl --request POST \
     --url https://api.0xscope.com/v2/entity/clusters \
     --header 'API-KEY: your-api-key' \
     --header 'accept: */*' \
     --header 'content-type: application/json' \
     --data '
{
  "addresses": [
    "0xcc6cdD3b84BeE496b94F223d049Ca6638B05e507",
    "0xd81cc51b50eb1c254947971fcca4f24a1208c5a2",
    "0x934b510d4c9103e6a87aef13b816fb080286d649"
  ],
  "chain": "ethereum"
}
'
```

## Sample Response

```json
{
  "code": 0,
  "data": [
    [
      "0x934b510d4c9103e6a87aef13b816fb080286d649"
    ],
    [
      "0xcc6cdd3b84bee496b94f223d049ca6638b05e507",
      "0xd81cc51b50eb1c254947971fcca4f24a1208c5a2"
    ]
  ],
  "uuid": 1656868483679780900
}
```

# Returns risky score of the address

**GET** `https://api.0xscope.com/v2/kye/riskyScore`

Returns risky score of the address.

## Sample Request

```curl
curl --request GET \
     --url 'https://api.0xscope.com/v2/kye/riskyScore?address=0x934b510d4c9103e6a87aef13b816fb080286d649&chain=ethereum' \
     --header 'API-KEY: your-api-key' \
     --header 'accept: */*'
```

## Sample Response

```json
{
  "code": 0,
  "data": {
    "totalScore": 80,
    "highScore": 30,
    "mediumScore": 60,
    "lowScore": 100
  },
  "uuid": 1668204304458846200
}
```

# (batch) Returns risky scores of a batch of addresses

**POST** `https://api.0xscope.com/v2/kye/riskyScoreBatch`

This endpoint returns risky scores for a batch of addresses.

## Sample Request

```curl
curl --request POST \
     --url https://api.0xscope.com/v2/kye/riskyScoreBatch \
     --header 'accept: */*' \
     --header 'API-KEY: your-api-key' \
     --header 'content-type: application/json' \
     --data '
{
  "addresses": [
    "0x934b510d4c9103e6a87aef13b816fb080286d649",
    "0xedd650a1b2d7e7049e1228bb5e60bd4cd5f7d67b",
    "0xd8da6bf26964af9d7eed9e03e53415d37aa96045"
  ],
  "chain": "ethereum"
}
'
```

## Sample Response

```json
{
  "code": 0,
  "data": [
    {
      "address": "0x934b510d4c9103e6a87aef13b816fb080286d649",
      "totalScore": 80,
      "highScore": 30,
      "mediumScore": 60,
      "lowScore": 100
    },
    {
      "address": "0xedd650a1b2d7e7049e1228bb5e60bd4cd5f7d67b",
      "totalScore": 99,
      "highScore": 100,
      "mediumScore": 60,
      "lowScore": 100
    },
    {
      "address": "0xd8da6bf26964af9d7eed9e03e53415d37aa96045",
      "totalScore": 86,
      "highScore": 100,
      "mediumScore": 100,
      "lowScore": 100
    }
  ],
  "uuid": 1735178942656831500
}
```

# Returns specific risk behavior of the address

**GET** `https://api.0xscope.com/v2/kye/riskyDetail`

Returns specific risk behavior of the address, you can find more info here [https://0xscope.readme.io/reference/list-of-risk-types](https://0xscope.readme.io/reference/list-of-risk-types)

## Sample Request

```curl
curl --request GET \
     --url 'https://api.0xscope.com/v2/kye/riskyDetail?address=0xedd650a1b2d7e7049e1228bb5e60bd4cd5f7d67b&chain=ethereum' \
     --header 'API-KEY: your-api-key' \
     --header 'accept: */*'
```

## Sample Response

```json
{
  "code": 0,
  "data": [
    {
      "riskName": "Associated with Malicious address",
      "riskType": "Hacker/Heist related",
      "riskLevel": "High",
      "riskDescription": "This address has transacted with malicious addresses, one or more times within one hop",
      "riskReason": [
        {
          "txhash": "0xec20ef1e0196aaa9db0f585002cda7a9f329834cd38c85a25714a6209610ff92",
          "related_addr": "0xb80db67828f44318aacb796c686d30d9d3f81e75",
          "total_value": 55500,
          "type": "Hack transfer"
        }
      ]
    },
    {
      "riskName": "Risk entity",
      "riskType": "Entity related",
      "riskLevel": "Medium",
      "riskDescription": "This address seems to be connected to a risk entity",
      "riskReason": [
        {
          "txhash": null,
          "related_addr": "0x93a203cf171d5a6f83da1b84877d06aa0e8f57e1",
          "total_value": 90,
          "type": "Entity involved"
        }
      ]
    },
    {
      "riskName": "Mixer indirect transfer ",
      "riskType": "Mixing related",
      "riskLevel": "Medium",
      "riskDescription": "This address has received transfers from mixer user addresses within three hops",
      "riskReason": [
        {
          "txhash": "0xec20ef1e0196aaa9db0f585002cda7a9f329834cd38c85a25714a6209610ff92",
          "related_addr": "0x69a04a0dc5b21bf0612877b460c89446364306c8",
          "total_value": 55500,
          "type": "Mixing transfer indirectly"
        }
      ]
    }
  ],
  "uuid": 1668204706705182700
}
```

# (batch) Returns specific risk behavior of a batch of addresses

- **HTTP Method**: POST
- **URL**: `https://api.0xscope.com/v2/kye/riskyDetailBatch`

This API endpoint returns specific risk behavior of a batch of addresses. For more information on the types of risks, visit [List of risk types](https://0xscope.readme.io/reference/list-of-risk-types).

## Sample Request

```curl
curl --request POST \
     --url https://api.0xscope.com/v2/kye/riskyDetailBatch \
     --header 'API-KEY: your-api-key' \
     --header 'accept: */*' \
     --header 'content-type: application/json' \
     --data '
{
  "addresses": [
    "0x934b510d4c9103e6a87aef13b816fb080286d649",
    "0xedd650a1b2d7e7049e1228bb5e60bd4cd5f7d67b",
    "0xd8da6bf26964af9d7eed9e03e53415d37aa96045"
  ],
  "chain": "ethereum"
}
'
```

## Sample Response

```json
{
  "code": 0,
  "data": [
    {
      "address": "0x934b510d4c9103e6a87aef13b816fb080286d649",
      "addressRiskType": [
        {
          "riskName": "Risk entity",
          "riskType": "Entity related",
          "riskLevel": "Medium",
          "riskDescription": "This address seems to be connected to a risk entity",
          "riskReason": [
            {
              "txhash": null,
              "related_addr": "0x9492510bbcb93b6992d8b7bb67888558e12dcac4",
              "total_value": 80,
              "type": "Entity involved"
            }
          ]
        },
        {
          "riskName": "Mixer indirect transfer",
          "riskType": "Mixing related",
          "riskLevel": "Medium",
          "riskDescription": "This address has received transfers from mixer user addresses within three hops",
          "riskReason": [
            {
              "txhash": "0x322a2de7a9147e1e4779f6f193ca7a32d797230d378a3ba00e6b37c6187efcac",
              "related_addr": "0x0d09dc9a840b1b4ea25194998fd90bb50fc2008a",
              "total_value": 2444,
              "type": "Mixing transfer indirectly"
            },
            {
              "txhash": "0x37eb295aa8ce3ced8ae11d373eba6c85571e0cd1ef72a8e29d48c1ca927afebc",
              "related_addr": "0x0d09dc9a840b1b4ea25194998fd90bb50fc2008a",
              "total_value": 173341,
              "type": "Mixing transfer indirectly"
            }
          ]
        },
        {
          "riskName": "Associated with Malicious entity",
          "riskType": "Entity related",
          "riskLevel": "High",
          "riskDescription": "This address seems to be connected to a malicious entity",
          "riskReason": [
            {
              "txhash": null,
              "related_addr": "0x36a0356d43ee4168ed24efa1cae3198708667ac0",
              "total_value": null,
              "type": "Hacker entity"
            }
          ]
        }
      ]
    }
    // Additional address data omitted for brevity
  ],
  "uuid": 1735179450259890200
}
```

This is a simplified markdown representation of the content. Depending on the specific requirements, additional formatting or details can be added.

# Returns the risk score of other addresses belonging to the same entity as this address

**GET** `https://api.0xscope.com/v2/kye/entityRisk`

Returns the risk score of other addresses belonging to the same entity as this address.

## Sample Request

```curl
curl --request GET \
     --url 'https://api.0xscope.com/v2/kye/entityRisk?address=0xedd650a1b2d7e7049e1228bb5e60bd4cd5f7d67b&chain=ethereum' \
     --header 'API-KEY: your-api-key' \
     --header 'accept: */*'
```

## Sample Response

```json
{
  "code": 0,
  "data": [
    {
      "address": "0xedd650a1b2d7e7049e1228bb5e60bd4cd5f7d67b",
      "certainty": 9,
      "riskScore": 99
    },
    {
      "address": "0x93a203cf171d5a6f83da1b84877d06aa0e8f57e1",
      "certainty": 9,
      "riskScore": 85
    }
  ],
  "uuid": 1668204852293668900
}
```

# Detect possible risk items in the contract

**GET** `https://api.0xscope.com/v2/kye/riskDetection`

Detect possible risk items in the contract.

## Sample Request

```curl
curl --request GET \
     --url 'https://api.0xscope.com/v2/kye/riskDetection?contract_address=0x118b0af0e8e8f926c40e361ca934bca37ed8d23a&chain=ethereum' \
     --header 'API-KEY: your-api-key' \
     --header 'accept: */*'
```

## Sample Response

```json
{
  "code": 0,
  "data": {
    "address": "0x118b0af0e8e8f926c40e361ca934bca37ed8d23a",
    "is_risk": "1",
    "risk_behavior": "honey_pot",
    "is_honeypot": "1",
    "is_audit": "0",
    "is_open_source": "0",
    "creator_address": "0x8453403fcbde811d2f20e895a74d1bc7956ce2ce",
    "deployment_time": "1593632841"
  },
  "uuid": 1668207448877826000
}
```

This markdown representation includes the endpoint, a sample request, and a sample response for detecting possible risk items in a contract using the 0xScope API.

# Simulate the execution results of a transaction and reveal associated risks

- **POST** `https://api.0xscope.com/v2/kye/riskInteractive`

Simulate the execution results of a transaction and reveal associated risks.

## Sample Request

```curl
curl --request POST \
     --url https://api.0xscope.com/v2/kye/riskInteractive \
     --header 'API-KEY: your api key' \
     --header 'accept: */*' \
     --header 'content-type: application/json' \
     --data '
{
  "chain": "ethereum",
  "blockNumber": 18724453,
  "transaction": {
    "from": "0x8447e981341dd44F7a6CAF26e6452d3fb12d8592",
    "to": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
    "data": "0x2e1a7d4d00000000000000000000000000000000000000000000000000793c81b6f5d000",
    "value": "0",
    "gasLimit": 36015
  }
}
'
```

## Sample Response

```json
{
  "code": 0,
  "data": {
    "simulationId": "ce87685c-5e62-49f2-bda8-7c55bc6ae1ef",
    "success": true,
    "gasUsed": 30404,
    "blockNumber": 18724453,
    "is_honeypot": false,
    "kye_score": 1,
    "activity": [
      {
        "action": "TRANSFER",
        "token_address": "0x0000000000000000000000000000000000000000",
        "is_fake_token": false,
        "from": "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2",
        "to": "0x8447e981341dd44f7a6caf26e6452d3fb12d8592",
        "kye_score_of_to": 30,
        "value": 0.034125
      }
    ]
  },
  "uuid": 1732234437015916500
}
```

# Returns Twitter Infos of a Project or User

**GET** `https://api.0xscope.com/v2/social/twitterInfo`

Returns Twitter infos of a project or user.

## Sample Request

```curl
curl --request GET \
     --url 'https://api.0xscope.com/v2/social/twitterInfo?address=0x934b510d4c9103e6a87aef13b816fb080286d649&chain=ethereum' \
     --header 'API-KEY: your-api-key' \
     --header 'accept: */*'
```

## Sample Response

```json
{
  "code": 0,
  "data": {
    "id": "635682749",
    "username": "suji_yan",
    "name": "Suji Yan - Mask is BUIDLing",
    "url": "https://t.co/sFQhte067x",
    "verified": true,
    "description": "founder of @realmasknetwork #Mask🐦\nMaintain some fediverse instances\nsujiyan.eth",
    "created_at": "2012-07-14T21:54:18Z",
    "pinned_tweet_id": null,
    "profile_image_url": "https://pbs.twimg.com/profile_images/1571030729605144577/Nxsva4Vq_normal.png",
    "followers_count": 20270,
    "following_count": 3695,
    "listed_count": 406,
    "tweet_count": 13134
  },
  "uuid": 1656899742753751000
}
```

This section provides a straightforward example of how to use the API to get Twitter information about a project or user, including the CURL command for making the request and a sample of the JSON response you can expect.

# (batch) Returns twitter infos of a project or user

**POST** `https://api.0xscope.com/v2/social/twitterInfo_batch`

(batch) Returns twitter infos of a project or user

## Sample Request

```curl
curl --request POST \
     --url https://api.0xscope.com/v2/social/twitterInfo_batch \
     --header 'API-KEY: your-api-key' \
     --header 'accept: */*' \
     --header 'content-type: application/json' \
     --data '
{
  "addresses": [
    "0x934b510d4c9103e6a87aef13b816fb080286d649",
    "0x00ede3b3a16ca0879c2791f940fbbc6008b6b73b",
    "0x08d65218f9ac9b69cc4b5c4ff9d1c6672cfe4b80"
  ],
  "chain": "ethereum"
}
'
```

## Sample Response

```json
{
  "code": 0,
  "data": [
    {
      "id": "635682749",
      "username": "suji_yan",
      "name": "Suji Yan - Mask is BUIDLing",
      "url": "https://t.co/sFQhte067x",
      "verified": true,
      "description": "founder of @realmasknetwork #Mask🐦\nMaintain some fediverse instances\nsujiyan.eth",
      "created_at": "2012-07-14T21:54:18Z",
      "pinned_tweet_id": null,
      "profile_image_url": "https://pbs.twimg.com/profile_images/1571030729605144577/Nxsva4Vq_normal.png",
      "followers_count": 20270,
      "following_count": 3695,
      "listed_count": 406,
      "tweet_count": 13134,
      "address": "0x934b510d4c9103e6a87aef13b816fb080286d649"
    },
    {
      "id": "1084993122927439872",
      "username": "huang1886",
      "name": "加密撸逼(💙,🧡)",
      "url": "https://t.co/ta8Cqm6RZa",
      "verified": false,
      "description": "-撸毛圣经：可能不值钱，但我必须有 \n-猪脚饭博主#zkApes\nhttps://t.co/MNQ03paFE2\n⏳@t2wrld",
      "created_at": "2019-01-15T01:58:13Z",
      "pinned_tweet_id": null,
      "profile_image_url": "https://pbs.twimg.com/profile_images/1646700675169124352/g5p5gou-_normal.jpg",
      "followers_count": 396,
      "following_count": 2721,
      "listed_count": 17,
      "tweet_count": 2703,
      "address": "0x00ede3b3a16ca0879c2791f940fbbc6008b6b73b"
    }
  ],
  "uuid": 1656900011105321000
}
```

# Returns twitter send count of this project in a certain period of time

- **Method**: GET
- **URL**: `https://api.0xscope.com/v2/social/twitterActivityChart`

## Sample Request

```curl
curl --request GET \
     --url 'https://api.0xscope.com/v2/social/twitterActivityChart?address=0xd533a949740bb3306d119cc777fa900ba034cd52&chain=ethereum' \
     --header 'API-KEY: your-api-key' \
     --header 'accept: */*'
```

## Sample Response

```json
{
  "code": 0,
  "data": {
    "date": [
      "2023-05-06",
      "2023-05-07",
      "2023-05-08",
      "2023-05-09",
      "2023-05-10",
      "2023-05-11",
      "2023-05-12"
    ],
    "official_count": [
      0,
      0,
      5,
      4,
      2,
      1,
      0
    ],
    "other_count": [
      4,
      4,
      8,
      7,
      4,
      3,
      1
    ]
  },
  "uuid": 1656900433727586300
}
```

This information provides details on how to make a request to the API to get the Twitter send count for a project over a specific period, including the sample request and response formats.

# twitter records from official twitter

**GET** `https://api.0xscope.com/v2/social/twitterRecordsOfficial`

twitter records from official twitter

## Sample Request

```curl
curl --request GET \
     --url 'https://api.0xscope.com/v2/social/twitterRecordsOfficial?address=0xd533a949740bb3306d119cc777fa900ba034cd52&chain=ethereum&limit=10&page=1' \
     --header 'API-KEY: your-api-key' \
     --header 'accept: */*'
```

## Sample Response

```json
{
  "code": 0,
  "data": {
    "total": 854,
    "page": 1,
    "limit": 10,
    "rows": [
      {
        "id": "1656726706617450539",
        "author_id": "1214050967986946051",
        "attachments": "[{\"media_key\": \"3_1653758406673727489\", \"type\": \"photo\", \"url\": \"https://pbs.twimg.com/media/FvNUgkYagAE0RwX.jpg\"}]",
        "source": null,
        "lang": "en",
        "tweets": "RT @stable_summit: Stable Summit. Paris. 15-16 July 2023. https://t.co/99mXvISYwS",
        "conversation_id": "1656726706617450539",
        "in_reply_to_user_id": null,
        "reply_settings": "everyone",
        "context_annotations": null,
        "public_metrics": "{\"retweet_count\": 12, \"reply_count\": 0, \"like_count\": 0, \"quote_count\": 0, \"impression_count\": 0}",
        "created_at": "2023-05-11T18:23:22Z",
        "possibly_sensitive": false,
        "referenced_tweets_id": "1653761338425102338",
        "referenced_tweets_type": "retweeted",
        "username": "curvefinance",
        "name": "Curve Finance",
        "profile_image_url": "https://pbs.twimg.com/profile_images/1220560374346461185/W1sQNVWo_normal.jpg",
        "verified": false,
        "referenced_tweets_username": "stable_summit",
        "retweeted_username": "stable_summit",
        "retweeted_name": "StableSummit",
        "retweeted_profile_image_url": "https://pbs.twimg.com/profile_images/1651806989146800128/eGY39gbl_normal.jpg",
        "retweeted_verified": false
      },
      ...additional tweets...
    ]
  },
  "uuid": 1656900671666258000
}
```

Please note that the sample response is truncated for brevity. The actual response contains more data rows.

# twitter records from non-official twitter

**GET** `https://api.0xscope.com/v2/social/twitterRecordsNotOfficial`

twitter records from non-official twitter

## Sample Request

```curl
curl --request GET \
     --url 'https://api.0xscope.com/v2/social/twitterRecordsNotOfficial?address=0xd533a949740bb3306d119cc777fa900ba034cd52&chain=ethereum&limit=10&page=1' \
     --header 'API-KEY: your-api-key' \
     --header 'accept: */*'
```

## Sample Response

```json
{
  "code": 0,
  "data": {
    "total": 30,
    "page": 1,
    "limit": 10,
    "rows": [
      {
        "id": "1656752889287569415",
        "author_id": "1364989021340983300",
        "tweets": "RT @chain_broker: 💎 GNOSIS TOTAL VALUE LOCKED OVERVIEW\n\n@CurveFinance and @Agave_lending are among the most value locked #TVL.\n\n$CRV $BAL $…",
        "created_at": "2023-05-11T20:07:24Z",
        "username": "agave_lending",
        "name": "Agave",
        "profile_image_url": "https://pbs.twimg.com/profile_images/1365032263902261250/Y0HAfGv7_normal.jpg",
        "verified": false
      },
      {
        "id": "1656625632699199488",
        "author_id": "963815487481303040",
        "tweets": "Web Traffic Spotlight in April: Decentralized Exchanges\n\nThe website viewership helps understand the website's popularity, website audience geography, and other valuable details.\n\n$CAKE $UNI $GMX #1INCH $GRAIL $SUSHI $OSMO $BSW $QUICK $JOE $CRV $DYDX #DEX https://t.co/itP79rt98p",
        "created_at": "2023-05-11T11:41:44Z",
        "username": "cryptodiffer",
        "name": "🇺🇦 CryptoDiffer - StandWithUkraine 🇺🇦",
        "profile_image_url": "https://pbs.twimg.com/profile_images/1019940002967556096/GDQ6KLDs_normal.jpg",
        "verified": true
      },
      ...
    ]
  },
  "uuid": 1656901727494209500
}
```

This response shows a sample of tweets from non-official Twitter accounts related to cryptocurrency, including details like the tweet's content, creation date, author's username, and verification status.

# Returns all NFTs we are tracking

- **Method:** GET
- **URL:** `https://api.0xscope.com/v2/nft/getSupportedNFTList`

## Sample Request

```bash
curl --request GET \
     --url 'https://api.0xscope.com/v2/nft/getSupportedNFTList?chain=ethereum&limit=10&page=1' \
     --header 'API-KEY: your-api-key' \
     --header 'accept: */*'
```

## Sample Response

```json
{
  "code": 0,
  "data": {
    "total": 214925,
    "page": 1,
    "limit": 10,
    "rows": [
      {
        "contract_address": "0xffffffffffc81e77d8cba73faeeae27439c7cb87",
        "name": "Firstclass Pass"
      },
      {
        "contract_address": "0xffffd4e17f2c7ef38ddcb0e9ebaef80a3baf5b17",
        "name": "Pengus Adventures"
      },
      {
        "contract_address": "0xffff630678622c534e1004c37e44229ac55d0d88",
        "name": "Melania Trump Digital Trading Cards"
      },
      {
        "contract_address": "0xffff2d93c83d4c613ed68ca887f057651135e089",
        "name": "stakefish validator"
      },
      {
        "contract_address": "0xfffeec08862bdbeb8eced845f6f7ce4402b39713",
        "name": "GOD DOES LOVE NFTS"
      },
      {
        "contract_address": "0xfffe55f5c8ee92eefa295a280689f1db0d249707",
        "name": "Saturnalia"
      },
      {
        "contract_address": "0xfffe0e955cad8e5154dc754c2ca083215761dafb",
        "name": "KAVASKI"
      },
      {
        "contract_address": "0xfffd93be8dc799cfb6a5025fb4731179219132c5",
        "name": "Full Send"
      },
      {
        "contract_address": "0xfffd676bffd8797f34c2adc3e808f374caee49d8",
        "name": "Gaia Protocol Stable DAO"
      },
      {
        "contract_address": "0xfffd0b40bd5e9fe69ead82e4fedfd405f96a9aaf",
        "name": "I will never know that I existed"
      }
    ]
  },
  "uuid": 1656902602862231600
}
```

# Returns Infos of this NFT

**GET** `https://api.0xscope.com/v2/nft/getInfo`

Returns information about a specific NFT.

## Sample Request

```curl
curl --request GET \
     --url 'https://api.0xscope.com/v2/nft/getInfo?contract_address=0xed5af388653567af2f388e6224dc7c4b3241c544&chain=ethereum' \
     --header 'API-KEY: your-api-key' \
     --header 'accept: */*'
```

## Sample Response

```json
{
  "code": 0,
  "data": {
    "symbol": "AZUKI",
    "total_volume": 607075.3774,
    "logo_url": "https://logo.nftscan.com/logo/0xed5af388653567af2f388e6224dc7c4b3241c544.png",
    "description": "Take the red bean to join the garden. View the collection at [azuki.com/gallery](https://azuki.com/gallery).\r\n\r\nAzuki starts with a collection of 10,000 avatars that give you membership access to The Garden: a corner of the internet where artists, builders, and web3 enthusiasts meet to create a decentralized future. Azuki holders receive access to exclusive drops, experiences, and more. Visit [azuki.com](https://azuki.com) for more details.\r\n\r\nWe rise together. We build together. We grow together.",
    "highest_price": 420.7,
    "instagram": "azuki",
    "royalty": "500",
    "contract_address": "0xed5af388653567af2f388e6224dc7c4b3241c544",
    "items_total": 10000,
    "deploy_block_number": "13975838",
    "lowest_price_24h": 13.09,
    "average_price_24h": 13.8962,
    "banner_url": "https://logo.nftscan.com/banner/0xed5af388653567af2f388e6224dc7c4b3241c544.png",
    "tag": [
      "AZUKI"
    ],
    "deployer": "0xd45058bf25bbd8f586124c479d384c8c708ce23a",
    "website": "http://www.azuki.com",
    "opensea_floor_price": 14.55,
    "owners_total": 4701,
    "discord": "https://discord.gg/azuki",
    "volume_24h": 819.877,
    "sales_24h": 59
  },
  "uuid": 1656902837441265700
}
```

This markdown format provides a concise overview of the API endpoint for retrieving information about a specific NFT, including how to make a sample request and what response to expect.

# Returns the market Statistics of this NFT

**GET** `https://api.0xscope.com/v2/nft/getMarketStatistics`

Returns the market Statistics of this NFT.

## Sample Request

```curl
curl --request GET \
     --url 'https://api.0xscope.com/v2/nft/getMarketStatistics?contract_address=0xed5af388653567af2f388e6224dc7c4b3241c544&chain=ethereum' \
     --header 'API-KEY: your-api-key' \
     --header 'accept: */*'
```

## Sample Response

```json
{
  "code": 0,
  "data": {
    "trades_count_24h": 59,
    "avg_price_24h": 13.8962,
    "highest_sale_24h": 35,
    "volume_24h": 819.877
  },
  "uuid": 1656903022657536000
}
```

This markdown format provides a concise summary of the API endpoint for retrieving market statistics of a specified NFT, including the sample request and response.

# Returns the floor price on every day

The API call returns the floor price of an NFT on every day.

**GET** `https://api.0xscope.com/v2/nft/getPriceChart`

## Sample Request

```curl
curl --request GET \
     --url 'https://api.0xscope.com/v2/nft/getPriceChart?contract_address=0xed5af388653567af2f388e6224dc7c4b3241c544&chain=ethereum&range=1d' \
     --header 'API-KEY: your-api-key' \
     --header 'accept: */*'
```

## Sample Response

```json
{
  "code": 0,
  "data": [
    {
      "price": 13.42,
      "date": 1683785040000
    },
    {
      "price": 15.88,
      "date": 1683788640000
    },
    {
      "price": 14.5,
      "date": 1683792240000
    },
    {
      "price": 13.3725,
      "date": 1683795840000
    },
    {
      "price": 13.3692,
      "date": 1683799440000
    },
    {
      "price": 13.335,
      "date": 1683806640000
    },
    {
      "price": 16.5,
      "date": 1683817440000
    },
    {
      "price": 15,
      "date": 1683821040000
    },
    {
      "price": 20.7633,
      "date": 1683824640000
    },
    {
      "price": 13.274,
      "date": 1683828240000
    },
    {
      "price": 13.1833,
      "date": 1683831840000
    },
    {
      "price": 13.16,
      "date": 1683839040000
    },
    {
      "price": 13.14,
      "date": 1683842640000
    },
    {
      "price": 13.18,
      "date": 1683849840000
    },
    {
      "price": 13.18,
      "date": 1683857040000
    },
    {
      "price": 13.17,
      "date": 1683860640000
    },
    {
      "price": 13.1425,
      "date": 1683864240000
    }
  ],
  "uuid": 1656903180770214000
}
```

This API call provides a straightforward way to fetch the floor price dynamics of a specific NFT by specifying the contract address, blockchain, and time range.

# Returns the volume on every day

**GET** `https://api.0xscope.com/v2/nft/getVolumeChart`

Returns the volume on every day.

## Sample Request

```curl
curl --request GET \
     --url 'https://api.0xscope.com/v2/nft/getVolumeChart?contract_address=0xed5af388653567af2f388e6224dc7c4b3241c544&chain=ethereum&range=1d' \
     --header 'API-KEY: your-api-key' \
     --header 'accept: */*'
```

## Sample Response

```json
{
  "code": 0,
  "data": [
    {
      "volume_eth": 13.42,
      "date": 1683785040000
    },
    {
      "volume_eth": 47.64,
      "date": 1683788640000
    },
    {
      "volume_eth": 14.5,
      "date": 1683792240000
    },
    {
      "volume_eth": 53.49,
      "date": 1683795840000
    },
    {
      "volume_eth": 173.8,
      "date": 1683799440000
    },
    {
      "volume_eth": 26.67,
      "date": 1683806640000
    },
    {
      "volume_eth": 16.5,
      "date": 1683817440000
    },
    {
      "volume_eth": 15,
      "date": 1683821040000
    },
    {
      "volume_eth": 62.29,
      "date": 1683824640000
    },
    {
      "volume_eth": 199.11,
      "date": 1683828240000
    },
    {
      "volume_eth": 39.55,
      "date": 1683831840000
    },
    {
      "volume_eth": 26.32,
      "date": 1683839040000
    },
    {
      "volume_eth": 13.14,
      "date": 1683842640000
    },
    {
      "volume_eth": 13.18,
      "date": 1683849840000
    },
    {
      "volume_eth": 26.36,
      "date": 1683857040000
    },
    {
      "volume_eth": 26.34,
      "date": 1683860640000
    },
    {
      "volume_eth": 52.57,
      "date": 1683864240000
    }
  ],
  "uuid": 1656903394897821700
}
```

# Returns Holders Statistics of this NFT

**GET** `https://api.0xscope.com/v2/nft/getHolderStatistics`

Returns Holders Statistics of this NFT.

## Sample Request

```curl
curl --request GET \
     --url 'https://api.0xscope.com/v2/nft/getHolderStatistics?contract_address=0xed5af388653567af2f388e6224dc7c4b3241c544&chain=ethereum' \
     --header 'API-KEY: your-api-key' \
     --header 'accept: */*'
```

## Sample Response

```json
{
  "code": 0,
  "data": {
    "holder_count": 4701,
    "entity_count": 4186
  },
  "uuid": 1656903577001918500
}
```

# Returns Holders Statistics of this NFT at one day

**GET** `https://api.0xscope.com/v2/nft/getHolderStatisticsDaily`

Returns Holders Statistics of this NFT at one day.

## Sample Request

```curl
curl --request GET \
     --url 'https://api.0xscope.com/v2/nft/getHolderStatisticsDaily?contract_address=0xed5af388653567af2f388e6224dc7c4b3241c544&chain=ethereum&date=2022-09-22' \
     --header 'API-KEY: your-api-key' \
     --header 'accept: */*'
```

## Sample Response

```json
{
  "code": 0,
  "data": {
    "daily_active_address_count": 144,
    "daily_active_entity_count": 119,
    "daily_new_address_count": 22,
    "daily_new_entity_count": 15
  },
  "uuid": 1656903749308121000
}
```

# Returns top Holders of this NFT

**GET** `https://api.0xscope.com/v2/nft/getTop100Holders`

This API endpoint returns the top holders of a specified NFT.

## Sample Request

```bash
curl --request GET \
     --url 'https://api.0xscope.com/v2/nft/getTop100Holders?contract_address=0xed5af388653567af2f388e6224dc7c4b3241c544&chain=ethereum' \
     --header 'API-KEY: your-api-key' \
     --header 'accept: */*'
```

## Sample Response

```json
{
  "code": 0,
  "data": [
    {
      "address": "0xd46c8648f2ac4ce1a1aace620460fbd24f640853",
      "balance": 378,
      "first_in": "1649892989"
    },
    {
      "address": "0xff3879b8a363aed92a6eaba8f61f1a96a9ec3c1e",
      "balance": 290,
      "first_in": "1643685199"
    },
    {
      "address": "0x29469395eaf6f95920e59f858042f0e28d98a20b",
      "balance": 271,
      "first_in": "1672241735"
    },
    // Additional records omitted for brevity
  ],
  "uuid": 1656904198794903600
}
```

This API call retrieves the top 100 holders of a specific NFT, providing details such as the address of the holder, their balance (number of tokens held), and the timestamp of their first acquisition (`first_in`) in UNIX format.

# Returns trades of this NFT in a certain period of time

**GET** `https://api.0xscope.com/v2/nft/getTrades`

Returns trades of this NFT in a certain period of time.

## Sample Request

```curl
curl --request GET \
     --url 'https://api.0xscope.com/v2/nft/getTrades?contract_address=0xed5af388653567af2f388e6224dc7c4b3241c544&chain=ethereum&begin_time=2022-07-05&end_time=2022-08-05&limit=10&page=1' \
     --header 'API-KEY: your-api-key' \
     --header 'accept: */*'
```

## Sample Response

```json
{
  "code": 0,
  "data": {
    "total": 473,
    "page": 1,
    "limit": 10,
    "rows": [
      {
        "timestamp": 1659734387,
        "tx_hash": "0xc244cd4fa21c2231c6a3be4a44a2d0fca4104d082e2787d1d4424f0ab9e36482",
        "platform": "LooksRare",
        "seller": "0x6b8df5e554f979dc93905ad42e0973349e4880c3",
        "buyer": "0xe4ae63c74cba2263842fb187bbac793fe60b2069",
        "price": "9.3500000000",
        "token_id": "1066"
      },
      {
        "timestamp": 1659720338,
        "tx_hash": "0x2766747af14eadcf8146ae93fa2342143472ccca0297bcadfa696095a3a995cc",
        "platform": "X2Y2",
        "seller": "0x82bbcac5a8b81368a4a96f0265cb40e46020a1e1",
        "buyer": "0x41bb70870e81291780493c13ae19cea81621bc69",
        "price": "8.6000000000",
        "token_id": "6680"
      },
      ...
    ]
  },
  "uuid": 1656904536402821000
}
```

# API Reference: the NFT Profit Leader Board

## Endpoint
**GET** `https://api.0xscope.com/v2/nft/profitLeaderBoard`

## Description
This endpoint retrieves the NFT profit leader board.

## Sample Request
```bash
curl --request GET \
     --url 'https://api.0xscope.com/v2/nft/profitLeaderBoard?contract_address=0xed5af388653567af2f388e6224dc7c4b3241c544&chain=ethereum&limit=10&page=1' \
     --header 'API-KEY: your-api-key' \
     --header 'accept: */*'
```

## Sample Response
```json
{
  "code": 0,
  "data": {
    "total": 200,
    "rows": [
      {
        "address": "0x866f1109fbef16beaaa46cf563e47c74f5c87ace",
        "total_profit": 1058.5574389978,
        "revenue": 1516.6774389978,
        "spent": 458.12,
        "roi": 231.07,
        "nft_purchased": 12,
        "nft_sold": 17,
        "first_in": 1643291534
      },
      {
        "address": "0x629fec46967250693bd2d0b259302c974d52a34a",
        "total_profit": 898.1681142663,
        "revenue": 913.1581142663,
        "spent": 14.99,
        "roi": 5991.78,
        "nft_purchased": 69,
        "nft_sold": 3,
        "first_in": 1683415259
      },
      {
        "address": "0xdb5fd0f533af3199eba21ee0d51642ed0ecfdf98",
        "total_profit": 627.8010602148,
        "revenue": 929.4210602148,
        "spent": 301.62,
        "roi": 208.14,
        "nft_purchased": 57,
        "nft_sold": 16,
        "first_in": 1673520983
      },
      ...
    ]
  },
  "uuid": 1656904836924702700
}
```

This response includes information about the top profit earners in the NFT market, such as the total profit, revenue, amount spent, return on investment (ROI), number of NFTs purchased and sold, and the first transaction timestamp.

# Returns the portfolio of the exchange on all chains

**GET** `https://api.0xscope.com/v2/exchange/getExchangePortfolio`

Returns the portfolio of the exchange on all chains.

## Sample Request

```curl
curl --request GET \
     --url 'https://api.0xscope.com/v2/exchange/getExchangePortfolio?exchange=binance' \
     --header 'API-KEY: your-api-key' \
     --header 'accept: */*'
```

## Sample Response

```json
{
  "code": 0,
  "data": [
    {
      "chain": "Metis",
      "value": "98691.08456664431200"
    },
    {
      "chain": "Flare",
      "value": "88.13888584068280"
    },
    {
      "chain": "HECO",
      "value": "84660.37457322696291"
    },
    {
      "chain": "Avalanche",
      "value": "742.66119824094567"
    },
    ...
    {
      "chain": "Shiden",
      "value": "0.00000000000000"
    }
  ],
  "uuid": 1656906822223003600
}
```

(Note: The response has been abbreviated for brevity, showing the beginning and end of the list.)
Below is the content from the URL in markdown format:

# Returns the inflow/outflow of the exchange in the past 24 hours

**GET** `https://api.0xscope.com/v2/exchange/getExchangeMoneyFlow`

Returns the inflow/outflow of the exchange in the past 24 hours.

## Sample Request

```curl
curl --request GET \
     --url 'https://api.0xscope.com/v2/exchange/getExchangeMoneyFlow?exchange=binance' \
     --header 'API-KEY: your-api-key' \
     --header 'accept: */*'
```

## Sample Response

```json
{
  "code": 0,
  "data": {
    "inflow": 679374409.4316931,
    "outflow": 705421811.0646318,
    "netflow": -26047401.6329388
  },
  "uuid": 1656907251262554000
}
```

This documentation provides information on how to use the API to get the inflow, outflow, and net flow of exchanges in the past 24 hours, with a sample request and response for better understanding.

请根据上面API Document的内容，用python实现一个API客户端。要求实现以上所有端点，并添加注释。