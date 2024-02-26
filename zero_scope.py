import requests
import json


class ZeroScopeAPI:
    def __init__(self, api_key):
        self.base_url = "https://api.0xscope.com/v2"
        self.headers = {"API-KEY": api_key, "accept": "*/*"}

    def get_supported_chains(self):
        """Returns the list of current supported chains."""
        url = f"{self.base_url}/basic/chains"
        response = requests.get(url, headers=self.headers)
        return response.json()

    def get_credits_remaining(self):
        """Returns the users' remaining credits."""
        url = f"{self.base_url}/basic/credits"
        response = requests.get(url, headers=self.headers)
        return json.dumps(response.json())

    def get_address_portfolio(self, address: str) -> str:
        """Returns the portfolio of the address on all supported chains."""
        url = f"{self.base_url}/address/portfolio?address={address}"
        response = requests.get(url, headers=self.headers)
        return json.dumps(response.json())

    def get_specific_token_balance(
        self, address: str, chain: str, token_address: str
    ) -> str:
        """Returns the balance of the user in one specific token."""
        url = f"{self.base_url}/address/tokenBalance?address={address}&chain={chain}&token_address={token_address}"
        response = requests.get(url, headers=self.headers)
        return json.dumps(response.json())

    def get_identity_tags(self, address: str, chain: str) -> str:
        """Get all the identity tag of an eoa/contract address."""
        url = f"{self.base_url}/address/identityTag?address={address}&chain={chain}"
        response = requests.get(url, headers=self.headers)
        return json.dumps(response.json())

    def get_ens_by_address(self, address: str, chain: str) -> str:
        """Get ENS by address, or get address by ENS."""
        url = f"{self.base_url}/address/ENS?address={address}&chain={chain}"
        response = requests.get(url, headers=self.headers)
        return json.dumps(response.json())

    def get_social_media_info(self, address: str, chain: str) -> str:
        """Get social media info of an address."""
        url = f"{self.base_url}/address/socialMedia?address={address}&chain={chain}"
        response = requests.get(url, headers=self.headers)
        return json.dumps(response.json())

    def get_token_transfers(
        self,
        address: str,
        chain: str,
        token_address: str,
        limit: int = 10,
        page: int = 1,
    ) -> str:
        """Get token transfers of an address."""
        url = f"{self.base_url}/address/tokenTransfers?address={address}&chain={chain}&token_address={token_address}&limit={limit}&page={page}"
        response = requests.get(url, headers=self.headers)
        return json.dumps(response.json())

    def get_transactions(
        self, address: str, chain: str, limit: int = 10, page: int = 1
    ) -> str:
        """Get transactions of an address."""
        url = f"{self.base_url}/address/transactions?address={address}&chain={chain}&limit={limit}&page={page}"
        response = requests.get(url, headers=self.headers)
        return json.dumps(response.json())

    def get_nft_transactions(
        self, address: str, chain: str, limit: int = 10, page: int = 1
    ) -> str:
        """Get NFT transactions of an address."""
        url = f"{self.base_url}/address/NFTtransactions?address={address}&chain={chain}&limit={limit}&page={page}"
        response = requests.get(url, headers=self.headers)
        return json.dumps(response.json())

    def get_detail_of_the_token(self, token_address: str, chain: str) -> str:
        """Get detail of the token."""
        url = (
            f"{self.base_url}/token/detail?token_address={token_address}&chain={chain}"
        )
        response = requests.get(url, headers=self.headers)
        return json.dumps(response.json())

    def get_holders_count_of_the_token(self, token_address: str, chain: str) -> str:
        """Retrieves the count of holders for a specified token."""
        url = f"{self.base_url}/token/holdersCount?token_address={token_address}&chain={chain}"
        response = requests.get(url, headers=self.headers)
        return json.dumps(response.json())

    def get_transfers_of_the_token(
        self, token_address: str, chain: str, limit: int = 10, page: int = 1
    ) -> str:
        """Get transfers of a specified token."""
        url = f"{self.base_url}/token/transfers?token_address={token_address}&chain={chain}&limit={limit}&page={page}"
        response = requests.get(url, headers=self.headers)
        return json.dumps(response.json())

    def get_top_1000_holders_of_the_token(self, token_address: str, chain: str) -> str:
        """Retrieves the top 1000 holders of a specific token."""
        url = f"{self.base_url}/token/topHolders?token_address={token_address}&chain={chain}"
        response = requests.get(url, headers=self.headers)
        return json.dumps(response.json())

    def get_volume_of_token_deposit_to_cex_hourly(
        self, token_address: str, chain: str
    ) -> str:
        """Retrieves the volume of a specific token deposited to CEX on an hourly basis."""
        url = f"{self.base_url}/token/cexDeposit?token_address={token_address}&chain={chain}"
        response = requests.get(url, headers=self.headers)
        return json.dumps(response.json())

    def get_volume_of_token_withdraw_from_cex_hourly(
        self, token_address: str, chain: str
    ) -> str:
        """Get volume of the token withdraw from CEX hourly."""
        url = f"{self.base_url}/token/cexWithdraw?token_address={token_address}&chain={chain}"
        response = requests.get(url, headers=self.headers)
        return json.dumps(response.json())

    def get_amount_of_token_held_by_cex_address(
        self, token_address: str, chain: str
    ) -> str:
        """Get amount of the token held by CEX address."""
        url = f"{self.base_url}/token/cexHolding?token_address={token_address}&chain={chain}"
        response = requests.get(url, headers=self.headers)
        return json.dumps(response.json())

    def get_supported_projects(self, chain: str, limit: int = 10, page: int = 1) -> str:
        """Get supported projects."""
        url = (
            f"{self.base_url}/project/supported?chain={chain}&limit={limit}&page={page}"
        )
        response = requests.get(url, headers=self.headers)
        return json.dumps(response.json())

    def get_detail_of_the_project(self, project_id: str, chain: str) -> str:
        """Get detail of the project."""
        url = f"{self.base_url}/project/detail?project_id={project_id}&chain={chain}"
        response = requests.get(url, headers=self.headers)
        return json.dumps(response.json())

    def get_tvl_of_the_project(self, project_id: str, chain: str, date: str) -> str:
        """Get tvl of the project."""
        url = f"{self.base_url}/project/tvl?project_id={project_id}&chain={chain}&date={date}"
        response = requests.get(url, headers=self.headers)
        return json.dumps(response.json())

    def get_daily_active_address_of_the_project(
        self, project_id: str, chain: str, date: str
    ) -> str:
        """Get daily active address of the project."""
        url = f"{self.base_url}/project/activeAddress?project_id={project_id}&chain={chain}&date={date}"
        response = requests.get(url, headers=self.headers)
        return json.dumps(response.json())

    def get_daily_active_entity_of_the_project(
        self, project_id: str, chain: str, date: str
    ) -> str:
        """Get daily active entity of the project."""
        url = f"{self.base_url}/project/activeEntity?project_id={project_id}&chain={chain}&date={date}"
        response = requests.get(url, headers=self.headers)
        return json.dumps(response.json())

    def get_daily_new_address_of_the_project(
        self, project_id: str, chain: str, date: str
    ) -> str:
        """Get daily new address of the project."""
        url = f"{self.base_url}/project/newAddress?project_id={project_id}&chain={chain}&date={date}"
        response = requests.get(url, headers=self.headers)
        return json.dumps(response.json())

    def get_daily_new_entity_of_the_project(
        self, project_id: str, chain: str, date: str
    ) -> str:
        """Get daily new entity of the project."""
        url = f"{self.base_url}/project/newEntity?project_id={project_id}&chain={chain}&date={date}"
        response = requests.get(url, headers=self.headers)
        return json.dumps(response.json())

    def get_related_addresses(self, address: str, chain: str) -> str:
        """Returns a batch of addresses belonging to the same entity as the input address."""
        url = f"{self.base_url}/entity/relatedAddress?address={address}&chain={chain}"
        response = requests.get(url, headers=self.headers)
        return json.dumps(response.json())

    def get_reasons_why_2_addresses_are_connected(
        self, address: str, related_address: str, chain: str
    ) -> str:
        """Returns the reason path why 2 addresses are connected."""
        url = f"{self.base_url}/entity/relatedReason?address={address}&relatedAddress={related_address}&chain={chain}"
        response = requests.get(url, headers=self.headers)
        return json.dumps(response.json())

    def divide_addresses_into_entities(self, addresses: list, chain: str) -> str:
        """Divide input addresses into different entities."""
        url = f"{self.base_url}/entity/clusters"
        data = {"addresses": addresses, "chain": chain}
        response = requests.post(url, headers=self.headers, json=data)
        return json.dumps(response.json())

    def get_risky_score(self, address: str, chain: str) -> str:
        """Returns risky score of the address."""
        url = f"{self.base_url}/kye/riskyScore?address={address}&chain={chain}"
        response = requests.get(url, headers=self.headers)
        return json.dumps(response.json())

    def get_batch_risky_scores(self, addresses: list, chain: str) -> str:
        """Returns risky scores of a batch of addresses."""
        url = f"{self.base_url}/kye/riskyScoreBatch"
        data = {"addresses": addresses, "chain": chain}
        response = requests.post(url, headers=self.headers, json=data)
        return json.dumps(response.json())

    def get_specific_risk_behavior(self, address: str, chain: str) -> str:
        """Returns specific risk behavior of the address."""
        url = f"{self.base_url}/kye/riskyDetail?address={address}&chain={chain}"
        response = requests.get(url, headers=self.headers)
        return json.dumps(response.json())

    def get_batch_specific_risk_behavior(self, addresses: list, chain: str) -> str:
        """Returns specific risk behavior of a batch of addresses."""
        url = f"{self.base_url}/kye/riskyDetailBatch"
        data = {"addresses": addresses, "chain": chain}
        response = requests.post(url, headers=self.headers, json=data)
        return json.dumps(response.json())

    def get_entity_risk_score(self, address: str, chain: str) -> str:
        """Returns the risk score of other addresses belonging to the same entity as this address."""
        url = f"{self.base_url}/kye/entityRisk?address={address}&chain={chain}"
        response = requests.get(url, headers=self.headers)
        return json.dumps(response.json())

    def risk_detection_in_contract(self, contract_address: str, chain: str) -> str:
        """Detect possible risk items in the contract."""
        url = f"{self.base_url}/kye/riskDetection?contract_address={contract_address}&chain={chain}"
        response = requests.get(url, headers=self.headers)
        return json.dumps(response.json())

    def simulate_transaction_risk(
        self, chain: str, block_number: int, transaction: dict
    ) -> str:
        """Simulate the execution results of a transaction and reveal associated risks."""
        url = f"{self.base_url}/kye/riskInteractive"
        data = {"chain": chain, "blockNumber": block_number, "transaction": transaction}
        response = requests.post(url, headers=self.headers, json=data)
        return json.dumps(response.json())

    def get_twitter_info(self, address: str, chain: str) -> str:
        """Returns Twitter Infos of a Project or User."""
        url = f"{self.base_url}/social/twitterInfo?address={address}&chain={chain}"
        response = requests.get(url, headers=self.headers)
        return json.dumps(response.json())

    def get_batch_twitter_info(self, addresses: list, chain: str) -> str:
        """Returns twitter infos of a project or user in batch."""
        url = f"{self.base_url}/social/twitterInfo_batch"
        data = {"addresses": addresses, "chain": chain}
        response = requests.post(url, headers=self.headers, json=data)
        return json.dumps(response.json())

    def get_twitter_activity_chart(self, address: str, chain: str) -> str:
        """Returns twitter send count of this project in a certain period of time."""
        url = f"{self.base_url}/social/twitterActivityChart?address={address}&chain={chain}"
        response = requests.get(url, headers=self.headers)
        return json.dumps(response.json())

    def get_twitter_records_official(
        self, address: str, chain: str, limit: int = 10, page: int = 1
    ) -> str:
        """Twitter records from official twitter."""
        url = f"{self.base_url}/social/twitterRecordsOfficial?address={address}&chain={chain}&limit={limit}&page={page}"
        response = requests.get(url, headers=self.headers)
        return json.dumps(response.json())

    def get_twitter_records_not_official(
        self, address: str, chain: str, limit: int = 10, page: int = 1
    ) -> str:
        """Twitter records from non-official twitter."""
        url = f"{self.base_url}/social/twitterRecordsNotOfficial?address={address}&chain={chain}&limit={limit}&page={page}"
        response = requests.get(url, headers=self.headers)
        return json.dumps(response.json())

    def get_supported_nft_list(self, chain: str, limit: int = 10, page: int = 1) -> str:
        """Returns all NFTs currently being tracked."""
        url = f"{self.base_url}/nft/getSupportedNFTList?chain={chain}&limit={limit}&page={page}"
        response = requests.get(url, headers=self.headers)
        return json.dumps(response.json())

    def get_nft_info(self, contract_address: str, chain: str) -> str:
        """Returns information about a specific NFT."""
        url = f"{self.base_url}/nft/getInfo?contract_address={contract_address}&chain={chain}"
        response = requests.get(url, headers=self.headers)
        return json.dumps(response.json())

    def get_nft_market_statistics(self, contract_address: str, chain: str) -> str:
        """Returns the market statistics of a specific NFT."""
        url = f"{self.base_url}/nft/getMarketStatistics?contract_address={contract_address}&chain={chain}"
        response = requests.get(url, headers=self.headers)
        return json.dumps(response.json())

    def get_nft_price_chart(
        self, contract_address: str, chain: str, range: str = "1d"
    ) -> str:
        """Returns the floor price on every day."""
        url = f"{self.base_url}/nft/getPriceChart?contract_address={contract_address}&chain={chain}&range={range}"
        response = requests.get(url, headers=self.headers)
        return json.dumps(response.json())

    def get_nft_volume_chart(
        self, contract_address: str, chain: str, range: str = "1d"
    ) -> str:
        """Returns the volume on every day for a specific NFT."""
        url = f"{self.base_url}/nft/getVolumeChart?contract_address={contract_address}&chain={chain}&range={range}"
        response = requests.get(url, headers=self.headers)
        return json.dumps(response.json())

    def get_nft_holder_statistics(self, contract_address: str, chain: str) -> str:
        """Returns holders statistics of a specific NFT."""
        url = f"{self.base_url}/nft/getHolderStatistics?contract_address={contract_address}&chain={chain}"
        response = requests.get(url, headers=self.headers)
        return json.dumps(response.json())

    def get_nft_holder_statistics_daily(
        self, contract_address: str, chain: str, date: str
    ) -> str:
        """Returns holders statistics of a specific NFT at one day."""
        url = f"{self.base_url}/nft/getHolderStatisticsDaily?contract_address={contract_address}&chain={chain}&date={date}"
        response = requests.get(url, headers=self.headers)
        return json.dumps(response.json())

    def get_nft_top_100_holders(self, contract_address: str, chain: str) -> str:
        """Returns top 100 holders of a specific NFT."""
        url = f"{self.base_url}/nft/getTop100Holders?contract_address={contract_address}&chain={chain}"
        response = requests.get(url, headers=self.headers)
        return json.dumps(response.json())

    def get_nft_trades(
        self,
        contract_address: str,
        chain: str,
        begin_time: str,
        end_time: str,
        limit: int = 10,
        page: int = 1,
    ) -> str:
        """Returns trades of a specific NFT in a certain period of time."""
        url = f"{self.base_url}/nft/getTrades?contract_address={contract_address}&chain={chain}&begin_time={begin_time}&end_time={end_time}&limit={limit}&page={page}"
        response = requests.get(url, headers=self.headers)
        return json.dumps(response.json())

    def get_nft_profit_leader_board(
        self, contract_address: str, chain: str, limit: int = 10, page: int = 1
    ) -> str:
        """Returns the NFT Profit Leader Board."""
        url = f"{self.base_url}/nft/profitLeaderBoard?contract_address={contract_address}&chain={chain}&limit={limit}&page={page}"
        response = requests.get(url, headers=self.headers)
        return json.dumps(response.json())

    def get_exchange_portfolio(self, exchange: str) -> str:
        """Returns the portfolio of the exchange on all chains."""
        url = f"{self.base_url}/exchange/getExchangePortfolio?exchange={exchange}"
        response = requests.get(url, headers=self.headers)
        return json.dumps(response.json())

    def get_exchange_money_flow(self, exchange: str) -> str:
        """Returns the inflow/outflow of the exchange in the past 24 hours."""
        url = f"{self.base_url}/exchange/getExchangeMoneyFlow?exchange={exchange}"
        response = requests.get(url, headers=self.headers)
        return json.dumps(response.json())
