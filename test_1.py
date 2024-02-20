import agent_batch
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env")

data_input = [
    {
        "input": "把下面的URL地址的内容提取出来，并整理成markdown格式。https://0xscope.readme.io/reference/basic_chains-1"
    },
    {
        "input": "把下面的URL地址的内容提取出来，并整理成markdown格式。https://0xscope.readme.io/reference/basic_credits-1"
    },
    {
        "input": "把下面的URL地址的内容提取出来，并整理成markdown格式。https://0xscope.readme.io/reference/address_portfolio"
    },
    {
        "input": "把下面的URL地址的内容提取出来，并整理成markdown格式。https://0xscope.readme.io/reference/address_tokenbalance-1"
    },
    {
        "input": "把下面的URL地址的内容提取出来，并整理成markdown格式。https://0xscope.readme.io/reference/address_identity_tag-1"
    },
    {
        "input": "把下面的URL地址的内容提取出来，并整理成markdown格式。https://0xscope.readme.io/reference/address_ens-1"
    },
    {
        "input": "把下面的URL地址的内容提取出来，并整理成markdown格式。https://0xscope.readme.io/reference/address_social_media-1"
    },
    {
        "input": "把下面的URL地址的内容提取出来，并整理成markdown格式。https://0xscope.readme.io/reference/address_token_transfers-1"
    },
    {
        "input": "把下面的URL地址的内容提取出来，并整理成markdown格式。https://0xscope.readme.io/reference/address_transactions-1"
    },
    {
        "input": "把下面的URL地址的内容提取出来，并整理成markdown格式。https://0xscope.readme.io/reference/address_nft_transactions-1"
    },
    {
        "input": "把下面的URL地址的内容提取出来，并整理成markdown格式。https://0xscope.readme.io/reference/token_detail-1"
    },
    {
        "input": "把下面的URL地址的内容提取出来，并整理成markdown格式。https://0xscope.readme.io/reference/token_holder_count-1"
    },
    {
        "input": "把下面的URL地址的内容提取出来，并整理成markdown格式。https://0xscope.readme.io/reference/token_transfers-2"
    },
    {
        "input": "把下面的URL地址的内容提取出来，并整理成markdown格式。https://0xscope.readme.io/reference/token_top_holders-1"
    },
    {
        "input": "把下面的URL地址的内容提取出来，并整理成markdown格式。https://0xscope.readme.io/reference/token_cex_deposit-1"
    },
    {
        "input": "把下面的URL地址的内容提取出来，并整理成markdown格式。https://0xscope.readme.io/reference/token_cex_withdraw-1"
    },
    {
        "input": "把下面的URL地址的内容提取出来，并整理成markdown格式。https://0xscope.readme.io/reference/token_cex_holding-1"
    },
    {
        "input": "把下面的URL地址的内容提取出来，并整理成markdown格式。https://0xscope.readme.io/reference/project_supported-1"
    },
    {
        "input": "把下面的URL地址的内容提取出来，并整理成markdown格式。https://0xscope.readme.io/reference/project_detail-1"
    },
    {
        "input": "把下面的URL地址的内容提取出来，并整理成markdown格式。https://0xscope.readme.io/reference/project_tvl-1"
    },
    {
        "input": "把下面的URL地址的内容提取出来，并整理成markdown格式。https://0xscope.readme.io/reference/project_active_address-1"
    },
    {
        "input": "把下面的URL地址的内容提取出来，并整理成markdown格式。https://0xscope.readme.io/reference/project_active_entity-1"
    },
    {
        "input": "把下面的URL地址的内容提取出来，并整理成markdown格式。https://0xscope.readme.io/reference/project_new_address-1"
    },
    {
        "input": "把下面的URL地址的内容提取出来，并整理成markdown格式。https://0xscope.readme.io/reference/project_new_entity-1"
    },
    {
        "input": "把下面的URL地址的内容提取出来，并整理成markdown格式。https://0xscope.readme.io/reference/entity_related_address"
    },
    {
        "input": "把下面的URL地址的内容提取出来，并整理成markdown格式。https://0xscope.readme.io/reference/entity_related_reason"
    },
    {
        "input": "把下面的URL地址的内容提取出来，并整理成markdown格式。https://0xscope.readme.io/reference/entity_clusters"
    },
    {
        "input": "把下面的URL地址的内容提取出来，并整理成markdown格式。https://0xscope.readme.io/reference/kye_riskyscore"
    },
    {
        "input": "把下面的URL地址的内容提取出来，并整理成markdown格式。https://0xscope.readme.io/reference/kye_riskyscorebatch"
    },
    {
        "input": "把下面的URL地址的内容提取出来，并整理成markdown格式。https://0xscope.readme.io/reference/kye_riskydetail"
    },
    {
        "input": "把下面的URL地址的内容提取出来，并整理成markdown格式。https://0xscope.readme.io/reference/kye_riskydetailbatch"
    },
    {
        "input": "把下面的URL地址的内容提取出来，并整理成markdown格式。https://0xscope.readme.io/reference/kye_entityrisk"
    },
    {
        "input": "把下面的URL地址的内容提取出来，并整理成markdown格式。https://0xscope.readme.io/reference/kye_riskdetection"
    },
    {
        "input": "把下面的URL地址的内容提取出来，并整理成markdown格式。https://0xscope.readme.io/reference/kye_riskinteractive"
    },
    {
        "input": "把下面的URL地址的内容提取出来，并整理成markdown格式。https://0xscope.readme.io/reference/social_twitterinfo"
    },
    {
        "input": "把下面的URL地址的内容提取出来，并整理成markdown格式。https://0xscope.readme.io/reference/social_twitterinfo_batch"
    },
    {
        "input": "把下面的URL地址的内容提取出来，并整理成markdown格式。https://0xscope.readme.io/reference/social_twitteractivitychart"
    },
    {
        "input": "把下面的URL地址的内容提取出来，并整理成markdown格式。https://0xscope.readme.io/reference/social_twitterrecordsofficial-1"
    },
    {
        "input": "把下面的URL地址的内容提取出来，并整理成markdown格式。https://0xscope.readme.io/reference/social_twitterrecordsnotofficial"
    },
    {
        "input": "把下面的URL地址的内容提取出来，并整理成markdown格式。https://0xscope.readme.io/reference/nft_getsupportednftlist-1"
    },
    {
        "input": "把下面的URL地址的内容提取出来，并整理成markdown格式。https://0xscope.readme.io/reference/nft_getinfo-1"
    },
    {
        "input": "把下面的URL地址的内容提取出来，并整理成markdown格式。https://0xscope.readme.io/reference/nft_getmarketstatistics-1"
    },
    {
        "input": "把下面的URL地址的内容提取出来，并整理成markdown格式。https://0xscope.readme.io/reference/nft_getpricechart-1"
    },
    {
        "input": "把下面的URL地址的内容提取出来，并整理成markdown格式。https://0xscope.readme.io/reference/nft_getvolumechart-1"
    },
    {
        "input": "把下面的URL地址的内容提取出来，并整理成markdown格式。https://0xscope.readme.io/reference/nft_getholderstatistics-1"
    },
    {
        "input": "把下面的URL地址的内容提取出来，并整理成markdown格式。https://0xscope.readme.io/reference/nft_getholderstatisticsdaily-1"
    },
    {
        "input": "把下面的URL地址的内容提取出来，并整理成markdown格式。https://0xscope.readme.io/reference/nft_gettop100holders-1"
    },
    {
        "input": "把下面的URL地址的内容提取出来，并整理成markdown格式。https://0xscope.readme.io/reference/nft_gettrades-1"
    },
    {
        "input": "把下面的URL地址的内容提取出来，并整理成markdown格式。https://0xscope.readme.io/reference/nft_profitleaderboard-1"
    },
    {
        "input": "把下面的URL地址的内容提取出来，并整理成markdown格式。https://0xscope.readme.io/reference/exchange_getexchangeportfolio"
    },
    {
        "input": "把下面的URL地址的内容提取出来，并整理成markdown格式。https://0xscope.readme.io/reference/exchange_getexchangemoneyflow"
    },
]
result = agent_batch.agent_executor.batch(data_input)
# print(result[0])
with open("output.md", "a") as file:
    # 遍历字符串数组
    for r in result:
        # 将每个字符串写入文件，每个字符串占一行
        file.write(r["output"] + "\n")
