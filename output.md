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

请根据上面API Document的内容，用python实现一个API客户端。要求实现以上所有端点。要求函数必须添加注释，注释中必须包含返回结果的例子。要求方法必须声明参数类型，返回类型必须是一个json字符串。