# Get supported chains

## GET /basic/chains

Returns the list of current support chains

### Sample Request

```bash
curl --request GET \
     --url https://api.0xscope.com/v2/basic/chains \
     --header 'API-KEY: your_api_key' \
     --header 'accept: */*'
```

### Sample Response

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

This endpoint does not require any parameters and returns a list of blockchain chains currently supported by the 0xScope API.

# Get credits remaining

## GET /basic/credits

Returns the users' remaining credits.

### Sample Request

```bash
curl --request GET \
     --url https://api.0xscope.com/v2/basic/credits \
     --header 'API-KEY: your_api_key' \
     --header 'accept: */*'
```

### Sample Response

```json
{
  "code": 0,
  "data": 2999671,
  "uuid": 1631549254684545000
}
```

This endpoint does not require any parameters and returns the number of credits remaining for the user's API key.

# Get Address Portfolio on All Supported Chains

## GET /address/portfolio

Returns the portfolio of the address on all supported chains.

### Sample Request

```bash
curl --request GET \
     --url 'https://api.0xscope.com/v2/address/portfolio?address=0x690b9a9e9aa1c9db991c7721a92d351db4fac990' \
     --header 'API-KEY: your_api_key' \
     --header 'accept: */*'
```

### Sample Response

```json
{
    "code": 0,
    "message": "ok",
    "data": [
        {
            "chain": "eth",
            "time_at": 1615386222,
            "token_id": "0xb3863e02d6930762933f672ca134c1ccecd0d413",
            "name": "Dog Token",
            "symbol": "DOG",
            "price": 0.0000000027610551384550184,
            "amount": 96.90407247305971,
            "value": 0.0000000027
        },
        {
            "chain": "bsc",
            "time_at": 1615386222,
            "token_id": "0xdf574c24545e5ffecb9a659c229253d4111d87e1",
            "name": "HUSD",
            "symbol": "HUSD",
            "price": 0.15,
            "amount": 100,
            "value": 15
        }
        ...
    ]
}
```

This endpoint provides detailed information about an address's holdings across different blockchain networks that 0xScope supports. It includes the chain, token IDs, the names and symbols of the tokens, their prices, amounts, and the total value of each holding.

# Get One Specific Token Balance of an Address

## GET /address/tokenBalance

Returns the balance of the user in one specific token.

### Sample Request

```bash
curl --request GET \
     --url 'https://api.0xscope.com/v2/address/tokenBalance?address=0x690b9a9e9aa1c9db991c7721a92d351db4fac990&chain=ethereum&token_address=0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48' \
     --header 'API-KEY: YOUR-API_KEY' \
     --header 'accept: */*'
```

### Sample Response

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

This endpoint does not require any parameters besides the ones in the request URL and returns detailed information about the balance of a specified token for a given address, including the blockchain chain, token ID, name, symbol, price, amount, and total value.

# Get Identity Tags of an Ethereum Address

## GET /address/identityTag

Fetches all identity tags associated with an Ethereum address or contract.

### Sample Request

```bash
curl --request GET \
     --url 'https://api.0xscope.com/v2/address/identityTag?address=0x690b9a9e9aa1c9db991c7721a92d351db4fac990' \
     --header 'API-KEY: YOUR_API_KEY' \
     --header 'accept: */*'
```

### Sample Response

```json
{
  "code": 0,
  "data": [
    {
      "address": "0x690b9a9e9aa1c9db991c7721a92d351db4fac990",
      "tags": [
        {
          "tag": "Exchange",
          "source": "Manual"
        },
        {
          "tag": "Known Scammer",
          "source": "Community"
        }
      ]
    }
  ],
  "uuid": 1656856457926541300
}
```

This endpoint provides an array of identity tags associated with the specified Ethereum address, including tags such as "Exchange" or "Known Scammer," along with the source of these tags (e.g., "Manual" or "Community"). This information can be useful for identifying the nature of transactions or the reputation of addresses in the Ethereum network.

# Get ENS by Address or Get Address by ENS

## GET /address/ENS

Get ENS by address, or get address by ENS.

### Sample Request

```bash
curl --request GET \
     --url 'https://api.0xscope.com/v2/address/ENS?address=0x690b9a9e9aa1c9db991c7721a92d351db4fac990&chain=ethereum' \
     --header 'API-KEY: your-api-key' \
     --header 'accept: */*'
```

### Sample Response

```json
{
  "code": 0,
  "data": "builder0x69.eth",
  "uuid": 1656857255674773500
}
```

This endpoint provides either the ENS associated with a given Ethereum address or the address associated with a given ENS. It requires the Ethereum address as a parameter in the request URL.

# Get Social Media by Address

## GET /address/socialMedia

Retrieves social media links associated with a given blockchain address.

### Path Parameters

- `address` (required): The blockchain address for which to retrieve social media links.
- `chain` (optional): The blockchain chain of the address. Defaults to `ethereum` if not specified.

### Sample Request

```bash
curl --request GET \
     --url 'https://api.0xscope.com/v2/address/socialMedia?address=0x123456789abcdef&chain=ethereum' \
     --header 'API-KEY: YOUR_API_KEY' \
     --header 'accept: application/json'
```

### Sample Response

```json
{
  "code": 0,
  "data": {
    "address": "0x123456789abcdef",
    "socialMedia": [
      {
        "platform": "Twitter",
        "link": "https://twitter.com/example_user"
      },
      {
        "platform": "LinkedIn",
        "link": "https://www.linkedin.com/in/example_user"
      }
      // Additional social media platforms and links may follow
    ]
  },
  "uuid": "unique_identifier_for_request"
}
```

This endpoint provides a list of social media links associated with the specified blockchain address. It can include various platforms such as Twitter, LinkedIn, and others, depending on the information available. This can be especially useful for getting to know more about the entity behind a blockchain address.

Remember, this is a hypothetical example, and the actual API documentation for "Get Social Media by Address" on 0xScope might differ in terms of endpoint paths, parameters, and response structure.

# Get Token Transfers of an Address

## GET /address/tokenTransfers

Get token transfers of an address.

### Sample Request

```bash
curl --request GET \
     --url 'https://api.0xscope.com/v2/address/tokenTransfers?address=0x690b9a9e9aa1c9db991c7721a92d351db4fac990&chain=ethereum&token_address=0xdac17f958d2ee523a2206206994597c13d831ec7&limit=10&page=1' \
     --header 'API-KEY: your-api-key' \
     --header 'accept: */*'
```

### Sample Response

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
      ...
    ]
  },
  "uuid": 1656857724413411300
}
```

This endpoint provides detailed information about token transfers for a specified address, including the transaction hash, timestamp, from and to addresses, token address, token name, symbol, decimal, and the value in USD.

# Get transactions of an address

Endpoint to retrieve transactions for a specified address.

## Method: GET

## URL
```
https://api.0xscope.com/v2/address/transactions
```

## Headers
- **API-KEY:** Your API key
- **Accept:** */*

## Parameters
- **address:** The address for which transactions are to be retrieved.
- **chain:** The blockchain network (e.g., ethereum).
- **limit:** Number of transactions to retrieve per page.
- **page:** Page number for pagination.

## Sample Request
```shell
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
      ...
    ]
  },
  "uuid": 1656858124629704700
}
```

Please replace `'your-api-key'` with your actual API key when making the request.

# Get NFT transactions of an address

Endpoint for retrieving NFT transactions associated with a specific address.

## Method: GET

## URL
```
https://api.0xscope.com/v2/address/NFTtransactions
```

## Headers
- **API-KEY:** Your API key
- **Accept:** */*

## Parameters
- **address:** The address for which NFT transactions are to be retrieved.
- **chain:** The blockchain network (e.g., ethereum).
- **limit:** Number of transactions to retrieve per page.
- **page:** Page number for pagination.

## Sample Request
```curl
curl --request GET \
     --url 'https://api.0xscope.com/v2/address/NFTtransactions?address=0x097703c488ecc613b6b6bfd419893be1625d28ba&chain=ethereum&limit=10&page=1' \
     --header 'API-KEY: your-api-key' \
     --header 'accept: */*'
```

## Sample Response
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

Replace `'your-api-key'` with your actual API key when making the request.