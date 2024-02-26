from dotenv import load_dotenv
import os
from zero_scope import ZeroScopeAPI
from langchain.agents import AgentExecutor
from langchain_core.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    MessagesPlaceholder,
)
from langchain_community.tools.convert_to_openai import format_tool_to_openai_tool
from langchain.agents.format_scratchpad.openai_tools import (
    format_to_openai_tool_messages,
)
from langchain.agents.output_parsers.openai_tools import OpenAIToolsAgentOutputParser
from langchain_openai import ChatOpenAI

load_dotenv(".env")

zero_scope_api_key = os.getenv("ZERO_SCOPE_API_KEY")

zeroScopeAPI = ZeroScopeAPI(api_key=zero_scope_api_key)

from langchain.agents import tool


@tool
def get_supported_chains():
    """Returns the list of current supported chains."""
    return zeroScopeAPI.get_supported_chains()


@tool
def get_credits_remaining() -> str:
    """Returns the users' remaining credits."""
    return zeroScopeAPI.get_credits_remaining()


@tool
def get_address_portfolio(address: str) -> str:
    """Returns the portfolio of the address on all supported chains."""
    return zeroScopeAPI.get_address_portfolio(address)


@tool
def get_specific_token_balance(address: str, chain: str, token_address: str) -> str:
    """Returns the balance of the user in one specific token.
The chain passed in should be a string of result returned from `get_supported_chains`."""
    return zeroScopeAPI.get_specific_token_balance(address, chain, token_address)


@tool
def get_identity_tags(address: str, chain: str) -> str:
    """Get all the identity tag of an eoa/contract address.
The chain passed in should be a string of result returned from `get_supported_chains`."""
    return zeroScopeAPI.get_identity_tags(address, chain)


@tool
def get_ens_by_address(address: str, chain: str) -> str:
    """Get ENS by address, or get address by ENS.
The chain passed in should be a string of result returned from `get_supported_chains`."""
    return zeroScopeAPI.get_ens_by_address(address, chain)


@tool
def get_social_media_info(address: str, chain: str) -> str:
    """Get social media info of an address.
The chain passed in should be a string of result returned from `get_supported_chains`."""
    return zeroScopeAPI.get_social_media_info(address, chain)


@tool
def get_token_transfers(
    address: str, chain: str, token_address: str, limit: int = 10, page: int = 1
) -> str:
    """Get token transfers of an address.
The chain passed in should be a string of result returned from `get_supported_chains`."""
    return zeroScopeAPI.get_token_transfers(address, chain, token_address, limit, page)


@tool
def get_transactions(address: str, chain: str, limit: int = 10, page: int = 1) -> str:
    """Get transactions of an address.
The chain passed in should be a string of result returned from `get_supported_chains`."""
    return zeroScopeAPI.get_transactions(address, chain, limit, page)


@tool
def get_nft_transactions(
    address: str, chain: str, limit: int = 10, page: int = 1
) -> str:
    """Get NFT transactions of an address.
The chain passed in should be a string of result returned from `get_supported_chains`."""
    return zeroScopeAPI.get_nft_transactions(address, chain, limit, page)


@tool
def get_detail_of_the_token(token_address: str, chain: str) -> str:
    """Get detail of the token.
The chain passed in should be a string of result returned from `get_supported_chains`."""
    return zeroScopeAPI.get_detail_of_the_token(token_address, chain)


@tool
def get_holders_count_of_the_token(token_address: str, chain: str) -> str:
    """Retrieves the count of holders for a specified token.
The chain passed in should be a string of result returned from `get_supported_chains`."""
    return zeroScopeAPI.get_holders_count_of_the_token(token_address, chain)


@tool
def get_transfers_of_the_token(
    token_address: str, chain: str, limit: int = 10, page: int = 1
) -> str:
    """Get transfers of a specified token.
The chain passed in should be a string of result returned from `get_supported_chains`."""
    return zeroScopeAPI.get_transfers_of_the_token(token_address, chain, limit, page)


@tool
def get_top_1000_holders_of_the_token(token_address: str, chain: str) -> str:
    """Retrieves the top 1000 holders of a specific token.
The chain passed in should be a string of result returned from `get_supported_chains`."""
    return zeroScopeAPI.get_top_1000_holders_of_the_token(token_address, chain)


@tool
def get_volume_of_token_deposit_to_cex_hourly(token_address: str, chain: str) -> str:
    """Retrieves the volume of a specific token deposited to CEX on an hourly basis.
The chain passed in should be a string of result returned from `get_supported_chains`."""
    return zeroScopeAPI.get_volume_of_token_deposit_to_cex_hourly(token_address, chain)


@tool
def get_volume_of_token_withdraw_from_cex_hourly(token_address: str, chain: str) -> str:
    """Get volume of the token withdraw from CEX hourly.
The chain passed in should be a string of result returned from `get_supported_chains`."""
    return zeroScopeAPI.get_volume_of_token_withdraw_from_cex_hourly(
        token_address, chain
    )


@tool
def get_amount_of_token_held_by_cex_address(token_address: str, chain: str) -> str:
    """Get amount of the token held by CEX address.
The chain passed in should be a string of result returned from `get_supported_chains`."""
    return zeroScopeAPI.get_amount_of_token_held_by_cex_address(token_address, chain)


@tool
def get_supported_projects(chain: str, limit: int = 10, page: int = 1) -> str:
    """Get supported projects.
The chain passed in should be a string of result returned from `get_supported_chains`."""
    return zeroScopeAPI.get_supported_projects(chain, limit, page)


@tool
def get_detail_of_the_project(project_id: str, chain: str) -> str:
    """Get detail of the project.
The chain passed in should be a string of result returned from `get_supported_chains`.
The project_id passed in should be a project id of result returned from `get_supported_projects`."""
    return zeroScopeAPI.get_detail_of_the_project(project_id, chain)


@tool
def get_tvl_of_the_project(project_id: str, chain: str, date: str) -> str:
    """Get tvl of the project.
The chain passed in should be a string of result returned from `get_supported_chains`.
The project_id passed in should be a project id of result returned from `get_supported_projects`."""
    return zeroScopeAPI.get_tvl_of_the_project(project_id, chain, date)


@tool
def get_daily_active_address_of_the_project(
    project_id: str, chain: str, date: str
) -> str:
    """Get daily active address of the project.
The chain passed in should be a string of result returned from `get_supported_chains`.
The project_id passed in should be a project id of result returned from `get_supported_projects`."""
    return zeroScopeAPI.get_daily_active_address_of_the_project(project_id, chain, date)


@tool
def get_daily_active_entity_of_the_project(
    project_id: str, chain: str, date: str
) -> str:
    """Get daily active entity of the project.
The chain passed in should be a string of result returned from `get_supported_chains`.
The project_id passed in should be a project id of result returned from `get_supported_projects`."""
    return zeroScopeAPI.get_daily_active_entity_of_the_project(project_id, chain, date)


@tool
def get_daily_new_address_of_the_project(project_id: str, chain: str, date: str) -> str:
    """Get daily new address of the project.
The chain passed in should be a string of result returned from `get_supported_chains`.
The project_id passed in should be a project id of result returned from `get_supported_projects`."""
    return zeroScopeAPI.get_daily_new_address_of_the_project(project_id, chain, date)


@tool
def get_daily_new_entity_of_the_project(project_id: str, chain: str, date: str) -> str:
    """Get daily new entity of the project.
The chain passed in should be a string of result returned from `get_supported_chains`.
The project_id passed in should be a project id of result returned from `get_supported_projects`."""
    return zeroScopeAPI.get_daily_new_entity_of_the_project(project_id, chain, date)


@tool
def get_related_addresses(address: str, chain: str) -> str:
    """Returns a batch of addresses belonging to the same entity as the input address.
The chain passed in should be a string of result returned from `get_supported_chains`."""
    return zeroScopeAPI.get_related_addresses(address, chain)


@tool
def get_reasons_why_2_addresses_are_connected(
    address: str, related_address: str, chain: str
) -> str:
    """Returns the reason path why 2 addresses are connected.
The chain passed in should be a string of result returned from `get_supported_chains`."""
    return zeroScopeAPI.get_reasons_why_2_addresses_are_connected(
        address, related_address, chain
    )


@tool
def divide_addresses_into_entities(addresses: list, chain: str) -> str:
    """Divide input addresses into different entities.
The chain passed in should be a string of result returned from `get_supported_chains`."""
    return zeroScopeAPI.divide_addresses_into_entities(addresses, chain)


@tool
def get_risky_score(address: str, chain: str) -> str:
    """Returns risky score of the address.
The chain passed in should be a string of result returned from `get_supported_chains`."""
    return zeroScopeAPI.get_risky_score(address, chain)


@tool
def get_batch_risky_scores(addresses: list, chain: str) -> str:
    """Returns risky scores of a batch of addresses.
The chain passed in should be a string of result returned from `get_supported_chains`."""
    return zeroScopeAPI.get_batch_risky_scores(addresses, chain)


@tool
def get_specific_risk_behavior(address: str, chain: str) -> str:
    """Returns specific risk behavior of the address.
The chain passed in should be a string of result returned from `get_supported_chains`."""
    return zeroScopeAPI.get_specific_risk_behavior(address, chain)


@tool
def get_batch_specific_risk_behavior(addresses: list, chain: str) -> str:
    """Returns specific risk behavior of a batch of addresses.
The chain passed in should be a string of result returned from `get_supported_chains`."""
    return zeroScopeAPI.get_batch_specific_risk_behavior(addresses, chain)


@tool
def get_entity_risk_score(address: str, chain: str) -> str:
    """Returns the risk score of other addresses belonging to the same entity as this address.
The chain passed in should be a string of result returned from `get_supported_chains`."""
    return zeroScopeAPI.get_entity_risk_score(address, chain)


@tool
def risk_detection_in_contract(contract_address: str, chain: str) -> str:
    """Detect possible risk items in the contract.
The chain passed in should be a string of result returned from `get_supported_chains`."""
    return zeroScopeAPI.risk_detection_in_contract(contract_address, chain)


@tool
def simulate_transaction_risk(chain: str, block_number: int, transaction: dict) -> str:
    """Simulate the execution results of a transaction and reveal associated risks.
The chain passed in should be a string of result returned from `get_supported_chains`."""
    return zeroScopeAPI.simulate_transaction_risk(chain, block_number, transaction)


@tool
def get_twitter_info(address: str, chain: str) -> str:
    """Returns Twitter Infos of a Project or User.
The chain passed in should be a string of result returned from `get_supported_chains`."""
    return zeroScopeAPI.get_twitter_info(address, chain)


@tool
def get_batch_twitter_info(addresses: list, chain: str) -> str:
    """Returns twitter infos of a project or user in batch.
The chain passed in should be a string of result returned from `get_supported_chains`."""
    return zeroScopeAPI.get_batch_twitter_info(addresses, chain)


@tool
def get_twitter_activity_chart(address: str, chain: str) -> str:
    """Returns twitter send count of this project in a certain period of time."""
    return zeroScopeAPI.get_twitter_activity_chart(address, chain)


@tool
def get_twitter_records_official(
    address: str, chain: str, limit: int = 10, page: int = 1
) -> str:
    """Twitter records from official twitter.
The chain passed in should be a string of result returned from `get_supported_chains`."""
    return zeroScopeAPI.get_twitter_records_official(address, chain, limit, page)


@tool
def get_twitter_records_not_official(
    address: str, chain: str, limit: int = 10, page: int = 1
) -> str:
    """Twitter records from non-official twitter.
The chain passed in should be a string of result returned from `get_supported_chains`."""
    return zeroScopeAPI.get_twitter_records_not_official(address, chain, limit, page)


@tool
def get_supported_nft_list(chain: str, limit: int = 10, page: int = 1) -> str:
    """Returns all NFTs currently being tracked.
The chain passed in should be a string of result returned from `get_supported_chains`."""
    return zeroScopeAPI.get_supported_nft_list(chain, limit, page)


@tool
def get_nft_info(contract_address: str, chain: str) -> str:
    """Returns information about a specific NFT.
The chain passed in should be a string of result returned from `get_supported_chains`."""
    return zeroScopeAPI.get_nft_info(contract_address, chain)


@tool
def get_nft_market_statistics(contract_address: str, chain: str) -> str:
    """Returns the market statistics of a specific NFT.
The chain passed in should be a string of result returned from `get_supported_chains`."""
    return zeroScopeAPI.get_nft_market_statistics(contract_address, chain)


@tool
def get_nft_price_chart(contract_address: str, chain: str, range: str = "1d") -> str:
    """Returns the floor price on every day.
The chain passed in should be a string of result returned from `get_supported_chains`."""
    return zeroScopeAPI.get_nft_price_chart(contract_address, chain, range)


@tool
def get_nft_volume_chart(contract_address: str, chain: str, range: str = "1d") -> str:
    """Returns the volume on every day for a specific NFT.
The chain passed in should be a string of result returned from `get_supported_chains`."""
    return zeroScopeAPI.get_nft_volume_chart(contract_address, chain, range)


@tool
def get_nft_holder_statistics(contract_address: str, chain: str) -> str:
    """Returns holders statistics of a specific NFT.
The chain passed in should be a string of result returned from `get_supported_chains`."""
    return zeroScopeAPI.get_nft_holder_statistics(contract_address, chain)


@tool
def get_nft_holder_statistics_daily(
    contract_address: str, chain: str, date: str
) -> str:
    """Returns holders statistics of a specific NFT at one day.
The chain passed in should be a string of result returned from `get_supported_chains`."""
    return zeroScopeAPI.get_nft_holder_statistics_daily(contract_address, chain, date)


@tool
def get_nft_top_100_holders(contract_address: str, chain: str) -> str:
    """Returns top 100 holders of a specific NFT.
The chain passed in should be a string of result returned from `get_supported_chains`."""
    return zeroScopeAPI.get_nft_top_100_holders(contract_address, chain)


@tool
def get_nft_trades(
    contract_address: str,
    chain: str,
    begin_time: str,
    end_time: str,
    limit: int = 10,
    page: int = 1,
) -> str:
    """Returns trades of a specific NFT in a certain period of time.
The chain passed in should be a string of result returned from `get_supported_chains`."""
    return zeroScopeAPI.get_nft_trades(
        contract_address, chain, begin_time, end_time, limit, page
    )


@tool
def get_nft_profit_leader_board(
    contract_address: str, chain: str, limit: int = 10, page: int = 1
) -> str:
    """Returns the NFT Profit Leader Board.
The chain passed in should be a string of result returned from `get_supported_chains`."""
    return zeroScopeAPI.get_nft_profit_leader_board(
        contract_address, chain, limit, page
    )


@tool
def get_exchange_portfolio(exchange: str) -> str:
    """Returns the portfolio of the exchange on all chains."""
    return zeroScopeAPI.get_exchange_portfolio(exchange)


@tool
def get_exchange_money_flow(exchange: str) -> str:
    """Returns the inflow/outflow of the exchange in the past 24 hours."""
    return zeroScopeAPI.get_exchange_money_flow(exchange)


zero_scope_tools = [
    get_supported_chains,
    get_credits_remaining,
    get_address_portfolio,
    get_specific_token_balance,
    get_identity_tags,
    get_ens_by_address,
    get_social_media_info,
    get_token_transfers,
    get_transactions,
    get_nft_transactions,
    get_detail_of_the_token,
    get_holders_count_of_the_token,
    get_transfers_of_the_token,
    get_top_1000_holders_of_the_token,
    get_volume_of_token_deposit_to_cex_hourly,
    get_volume_of_token_withdraw_from_cex_hourly,
    get_amount_of_token_held_by_cex_address,
    get_supported_projects,
    get_detail_of_the_project,
    get_tvl_of_the_project,
    get_daily_active_address_of_the_project,
    get_daily_active_entity_of_the_project,
    get_daily_new_address_of_the_project,
    get_daily_new_entity_of_the_project,
    get_related_addresses,
    get_reasons_why_2_addresses_are_connected,
    divide_addresses_into_entities,
    get_risky_score,
    get_batch_risky_scores,
    get_specific_risk_behavior,
    get_batch_specific_risk_behavior,
    get_entity_risk_score,
    risk_detection_in_contract,
    simulate_transaction_risk,
    get_twitter_info,
    get_batch_twitter_info,
    get_twitter_activity_chart,
    get_twitter_records_official,
    get_twitter_records_not_official,
    get_supported_nft_list,
    get_nft_info,
    get_nft_market_statistics,
    get_nft_price_chart,
    get_nft_volume_chart,
    get_nft_holder_statistics,
    get_nft_holder_statistics_daily,
    get_nft_top_100_holders,
    get_nft_trades,
    get_nft_profit_leader_board,
    get_exchange_portfolio,
    get_exchange_money_flow,
]
