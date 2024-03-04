data = [
    # {"input": "What are the supported blockchain networks?"},
    # {"input": "How many API credits do I have left?"},
    {"input": "Can you show me the portfolio of Uniswap V3's main contract address?"},
    {"input": "What is the balance of token SWFTC on Ethereum for 0x6cC5F688a315f3dC28A7781717a9A798a59fDA7b?"},
    {
        "input": "Retrieve identity tags for address 0x6cC5F688a315f3dC28A7781717a9A798a59fDA7b on Ethereum."
    },
    {
        "input": "What is the ENS name for address 0x690b9a9e9aa1c9db991c7721a92d351db4fac990?"
    },
	{
        "input": "What is the address for ENS name builder0x69.eth?"
    },
    {
        "input": "Fetch social media information for address 0xb6f165a70e2a394f2981ab2f0fa953c03f1871d4 on Ethereum."
    },
    {
        "input": "List recent 0x0bb217e40f8a5cb79adf04e1aab60e5abd0dfc1e token transfers for address 0x6cC5F688a315f3dC28A7781717a9A798a59fDA7b on Ethereum."
    },
    {
        "input": "Get transaction history for address 0x53b3514091B7b90252e5478C041A66e086fcCa46 on Avalanche."
    },
    {
        "input": "Show NFT transactions for address 0x2E7573445B46A305f6b80f86ba56E788b2dB7e68 on Ethereum"
    },
    {
        "input": "Details of token 0x163f8c2467924be0ae7b5347228cabf260318753 on Ethereum."
    },
	{
        "input": "Details of token WLD on Ethereum."
    },
    {
        "input": "How many holders does token 0xe9e7cea3dedca5984780bafc599bd69add087d56 have on Binance Smart Chain?"
    },
	{
        "input": "How many holders does token wld have on Ethereum?"
    },
    {
        "input": "Token SWFTC transfer records for 0x6cC5F688a315f3dC28A7781717a9A798a59fDA7b on Ethereum."
    },
    {
        "input": "Who are the top 1000 holders of token WLD on Ethereum?"
    },
	{
        "input": "SWFTC's contract address on Ethereum"
    },
    {
        "input": "Volume of token SWFTC deposited to CEX hourly on Ethereum."
    },
    {
        "input": "Withdrawal volume of token SWFTC from CEX hourly on Ethereum."
    },
    {
        "input": "Amount of token SWFTC held by CEX addresses on Ethereum."
    },
    # {"input": "What projects are supported?"},
    {"input": "Project details for Curve."},
    {"input": "Total Value Locked (TVL) of Curve."},
    {"input": "Daily active addresses of Curve."},
    {"input": "Daily active entities of Curve"},
    {"input": "New addresses associated with Curve."},
    {"input": "New entities associated with Curve."},
    {"input": "Related addresses for address 0x172059839d80773ec8617c4cb33835175d364cee on Ethereum."},
    {
        "input": "Connection reasons between address 0x934b510d4c9103e6a87aef13b816fb080286d649 and address 0xaab900656d7f37ae675f35560f163e2681e38b8a on Ethereum."
    },
    # {"input": "Cluster addresses into entities on Ethereum."},
    {"input": "Risky score of address 0xd533a949740bb3306d119cc777fa900ba034cd52."},
    {"input": "What project is address 0xd533a949740bb3306d119cc777fa900ba034cd52 belong to?"},
    # {"input": "Batch risky scores for multiple addresses on Ethereum."},
    {
        "input": "Specific risk behavior of address 0xd533a949740bb3306d119cc777fa900ba034cd52."
    },
    # {"input": "Batch specific risk behaviors for addresses on Polygon."},
    {
        "input": "Entity risk score for address 0xd533a949740bb3306d119cc777fa900ba034cd52 on Ethereum."
    },
    {
        "input": "Detect risks in contract address 0xd533a949740bb3306d119cc777fa900ba034cd52 on Ethereum."
    },
    # {"input": "Simulate transaction risk on Ethereum for a given transaction."},
    {
        "input": "Twitter information for project or user address 0x934b510d4c9103e6a87aef13b816fb080286d649."
    },
    # {
    #     "input": "Batch Twitter information for multiple addresses on Binance Smart Chain."
    # },
    # {"input": "Twitter activity chart for address 0x123... on Ethereum."},
    {"input": "Official Twitter records for address 0x934b510d4c9103e6a87aef13b816fb080286d649 on Ethereum."},
    {"input": "Non-official Twitter records for address 0xd533a949740bb3306d119cc777fa900ba034cd52 on Ethereum."},
    # {"input": "List of NFTs supported on Ethereum."},
    {"input": "Information about NFT Cryptopunks."},
    {"input": "Market statistics for NFT Cryptopunks."},
    # {"input": "NFT price chart for Cryptopunks."},
    # {"input": "NFT volume chart for contract address 0xabc... on Avalanche."},
    {"input": "Holder statistics for NFT Cryptopunks."},
    {"input": "Daily holder statistics for NFT Cryptopunks."},
    {"input": "Top 100 holders of NFT Cryptopunks."},
    # {
    # "input": "NFT trades for Cryptopunks within a specific time frame on Polygon."
    # },
    {"input": "NFT profit leaderboard for Cryptopunks on Ethereum."},
    {"input": "Portfolio of exchange 'Binance' across all chains."},
    {"input": "Money flow of exchange 'Coinbase' in the past 24 hours."},
    # {"input": "Can I see the supported chains again?"},
    # {"input": "How do I check my remaining API credits?"},
    # {"input": "Details of the top 10 holders of token 0xabc... on Ethereum."},
    # {"input": "Latest transactions of address 0x123... on Binance Smart Chain."},
    # {"input": "NFT market trends for contract address 0xabc... on Avalanche."},
    # {"input": "Risk assessment for address 0x123... on Ethereum."},
    # {
    #     "input": "Who are the recent top buyers of NFT contract address 0xabc... on Polygon?"
    # },
    # {"input": "Exchange inflow and outflow for 'Kraken' in the last day."},
    # {
    #     "input": "Get a list of all risk detections for the contract address 0xabc... on Solana."
    # },
]

supported_chains = [
    {"chain": "eth", "chainName": "Ethereum"},
    {"chain": "bsc", "chainName": "BSC"},
    {"chain": "arb", "chainName": "Arbitrum"},
    {"chain": "polygon", "chainName": "Polygon"},
    {"chain": "base", "chainName": "Base"},
    {"chain": "op", "chainName": "Optimism"},
    {"chain": "avax", "chainName": "Avalanche"},
    {"chain": "mnt", "chainName": "Mantle"},
]
