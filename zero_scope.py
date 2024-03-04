import requests
import json


class ZeroScopeAPI:
    def __init__(self, api_key):
        self.base_url = "https://api.0xscope.com/v2"
        self.headers = {"API-KEY": api_key, "accept": "*/*"}

    def get_supported_chains(self) -> str:
        """
        Returns the list of current support chains.

        Sample Response:
        {
            "code": 0,
            "data": [
                "ethereum",
                "bsc"
            ],
            "uuid": 1631546627552874500
        }
        """
        url = f"{self.base_url}/basic/chains"
        response = requests.get(url, headers=self.headers)
        return json.dumps(response.json())

    def get_credits_remaining(self) -> str:
        """
        Returns the user's remaining credits.

        Sample Response:
        {
            "code": 0,
            "data": 2999671,
            "uuid": 1631549254684545000
        }
        """
        url = f"{self.base_url}/basic/credits"
        response = requests.get(url, headers=self.headers)
        return json.dumps(response.json())

    def get_address_portfolio(self, address: str) -> str:
        """
        Returns the portfolio of the address on all supported chains.

        Sample Response:
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
                ...
            ]
        }
        """
        url = f"{self.base_url}/address/portfolio?address={address}"
        response = requests.get(url, headers=self.headers)
        return json.dumps(response.json())

    def get_specific_token_balance(
        self, address: str, chain: str, token_address: str
    ) -> str:
        """
        Returns the balance of the user in one specific token.

        Sample Response:
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
        """
        url = f"{self.base_url}/address/tokenBalance?address={address}&chain={chain}&token_address={token_address}"
        response = requests.get(url, headers=self.headers)
        return json.dumps(response.json())

    def get_identity_tags(self, address: str, chain: str) -> str:
        """
        Get all the identity tag of an eoa/contract address.

        Sample Response:
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
        """
        url = f"{self.base_url}/address/identityTag?address={address}&chain={chain}"
        response = requests.get(url, headers=self.headers)
        return json.dumps(response.json())

    def get_ens_by_address(self, address: str, chain: str) -> str:
        """
        Get ENS by address, or get address by ENS.

        Sample Response:
        {
            "code": 0,
            "data": "builder0x69.eth",
            "uuid": 1656857255674773500
        }
        """
        url = f"{self.base_url}/address/ENS?address={address}&chain={chain}"
        response = requests.get(url, headers=self.headers)
        return json.dumps(response.json())

    def get_social_media_info(self, address: str, chain: str) -> str:
        """
        Get social media info of an address.

        Sample Response:
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
        """
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
        """
        Get token transfers of an address.

        Sample Response:
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
        """
        url = f"{self.base_url}/address/tokenTransfers?address={address}&chain={chain}&token_address={token_address}&limit={limit}&page={page}"
        response = requests.get(url, headers=self.headers)
        return json.dumps(response.json())

    def get_transactions(
        self, address: str, chain: str, limit: int = 10, page: int = 1
    ) -> str:
        """
        Get transactions of an address.

        Sample Response:
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
        """
        url = f"{self.base_url}/address/transactions?address={address}&chain={chain}&limit={limit}&page={page}"
        response = requests.get(url, headers=self.headers)
        return json.dumps(response.json())

    def get_nft_transactions(
        self, address: str, chain: str, limit: int = 10, page: int = 1
    ) -> str:
        """
        Get NFT transactions of an address.

        Sample Response:
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
                    ...
                ]
            },
            "uuid": 1656858656798802000
        }
        """
        url = f"{self.base_url}/address/NFTtransactions?address={address}&chain={chain}&limit={limit}&page={page}"
        response = requests.get(url, headers=self.headers)
        return json.dumps(response.json())

    def get_detail_of_the_token(self, token_address: str, chain: str) -> str:
        """
        Get detail of the token.

        Sample Response:
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
        """
        url = (
            f"{self.base_url}/token/detail?token_address={token_address}&chain={chain}"
        )
        response = requests.get(url, headers=self.headers)
        return json.dumps(response.json())

    def get_holders_count_of_the_token(self, token_address: str, chain: str) -> str:
        """
        Retrieves the count of holders for a specified token.

        Sample Response:
        {
            "code": 0,
            "data": 1690552,
            "uuid": 1656860114080366600
        }
        """
        url = f"{self.base_url}/token/holdersCount?token_address={token_address}&chain={chain}"
        response = requests.get(url, headers=self.headers)
        return json.dumps(response.json())

    def get_transfers_of_the_token(
        self, token_address: str, chain: str, limit: int = 10, page: int = 1
    ) -> str:
        """
        Get transfers of a specified token.

        Sample Response:
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
                ...
            ],
            "uuid": 1656861356454183000
        }
        """
        url = f"{self.base_url}/token/transfers?token_address={token_address}&chain={chain}&limit={limit}&page={page}"
        response = requests.get(url, headers=self.headers)
        return json.dumps(response.json())

    def get_top_1000_holders_of_the_token(self, token_address: str, chain: str) -> str:
        """
        Retrieves the top 1000 holders of a specific token.

        Sample Response:
        {
            "code": 0,
            "data": [
                {
                    "address": "0x0a59649758aa4d66e25f08dd01271e891fe52199",
                    "balance": 1664321254.005198,
                    "percentage": 5.549526383572078
                },
                ...
            ]
        }
        """
        url = f"{self.base_url}/token/topHolders?token_address={token_address}&chain={chain}"
        response = requests.get(url, headers=self.headers)
        return json.dumps(response.json())

    def get_volume_of_token_deposit_to_cex_hourly(
        self, token_address: str, chain: str
    ) -> str:
        """
        Retrieves the volume of a specific token deposited to CEX on an hourly basis.

        Sample Response:
        {
            "code": 0,
            "data": [
                {
                    "timestamp": "2023-05-11 14:00:00",
                    "volume": 3000,
                    "cex_name": "AscendEX"
                },
                ...
            ],
            "uuid": 1656862678247145500
        }
        """
        url = f"{self.base_url}/token/cexDeposit?token_address={token_address}&chain={chain}"
        response = requests.get(url, headers=self.headers)
        return json.dumps(response.json())

    def get_volume_of_token_withdraw_from_cex_hourly(
        self, token_address: str, chain: str
    ) -> str:
        """
        Get volume of the token withdraw from CEX hourly.

        Sample Response:
        {
            "code": 0,
            "data": [
                {
                    "timestamp": "2023-05-11 03:00:00",
                    "volume": 1034.9234,
                    "cex_name": "AscendEX"
                },
                ...
            ],
            "uuid": 1656863004404613000
        }
        """
        url = f"{self.base_url}/token/cexWithdraw?token_address={token_address}&chain={chain}"
        response = requests.get(url, headers=self.headers)
        return json.dumps(response.json())

    def get_amount_of_token_held_by_cex_address(
        self, token_address: str, chain: str
    ) -> str:
        """
        Get amount of the token held by CEX address.

        Sample Response:
        {
            "code": 0,
            "data": [
                {
                    "timestamp": "2023-05-11",
                    "holding": 913175381.854418,
                    "cex_name": "Binance"
                },
                ...
            ],
            "uuid": 1656863210965696500
        }
        """
        url = f"{self.base_url}/token/cexHolding?token_address={token_address}&chain={chain}"
        response = requests.get(url, headers=self.headers)
        return json.dumps(response.json())

    def get_supported_projects(self, chain: str, limit: int = 10, page: int = 1) -> str:
        """
        Get supported projects.

        Sample Response:
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
                    ...
                ]
            },
            "uuid": 1656863852572573700
        }
        """
        url = (
            f"{self.base_url}/project/supported?chain={chain}&limit={limit}&page={page}"
        )
        response = requests.get(url, headers=self.headers)
        return json.dumps(response.json())

    def get_detail_of_the_project(self, project_id: str, chain: str) -> str:
        """
        Get detail of the project.

        Sample Response:
        {
            "code": 0,
            "data": {
                "website": "https://anyswap.exchange/",
                ...
                "contracts": [
                    "0xf99d58e463a2e07e5692127302c20a191861b4d6",
                    ...
                ]
            },
            "uuid": 1735180060044583000
        }
        """
        url = f"{self.base_url}/project/detail?project_id={project_id}&chain={chain}"
        response = requests.get(url, headers=self.headers)
        return json.dumps(response.json())

    def get_tvl_of_the_project(self, project_id: str, chain: str, date: str) -> str:
        """
        Get tvl of the project.

        Sample Response:
        {
            "code": 0,
            "data": "1167465179.00000000",
            "uuid": 1656864202490773500
        }
        """
        url = f"{self.base_url}/project/tvl?project_id={project_id}&chain={chain}&date={date}"
        response = requests.get(url, headers=self.headers)
        return json.dumps(response.json())

    def get_daily_active_address_of_the_project(
        self, project_id: str, chain: str, date: str
    ) -> str:
        """
        Get daily active address of the project.

        Sample Response:
        {
            "code": 0,
            "data": 7073,
            "uuid": 1656864362826432500
        }
        """
        url = f"{self.base_url}/project/activeAddress?project_id={project_id}&chain={chain}&date={date}"
        response = requests.get(url, headers=self.headers)
        return json.dumps(response.json())

    def get_daily_active_entity_of_the_project(
        self, project_id: str, chain: str, date: str
    ) -> str:
        """
        Get daily active entity of the project.

        Sample Response:
        {
            "code": 0,
            "data": 6247,
            "uuid": 1656864485019091000
        }
        """
        url = f"{self.base_url}/project/activeEntity?project_id={project_id}&chain={chain}&date={date}"
        response = requests.get(url, headers=self.headers)
        return json.dumps(response.json())

    def get_daily_new_address_of_the_project(
        self, project_id: str, chain: str, date: str
    ) -> str:
        """
        Get daily new address of the project.

        Sample Response:
        {
            "code": 0,
            "data": 1621,
            "uuid": 1656864618259546000
        }
        """
        url = f"{self.base_url}/project/newAddress?project_id={project_id}&chain={chain}&date={date}"
        response = requests.get(url, headers=self.headers)
        return json.dumps(response.json())

    def get_daily_new_entity_of_the_project(
        self, project_id: str, chain: str, date: str
    ) -> str:
        """
        Get daily new entity of the project.

        Sample Response:
        {
            "code": 0,
            "data": 1534,
            "uuid": 1656864758437380000
        }
        """
        url = f"{self.base_url}/project/newEntity?project_id={project_id}&chain={chain}&date={date}"
        response = requests.get(url, headers=self.headers)
        return json.dumps(response.json())

    def get_related_addresses(self, address: str, chain: str) -> str:
        """
        Returns a batch of addresses belonging to the same entity as the input address.

        Sample Response:
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
                ...
            ],
            "uuid": 1656866963588513800
        }
        """
        url = f"{self.base_url}/entity/relatedAddress?address={address}&chain={chain}"
        response = requests.get(url, headers=self.headers)
        return json.dumps(response.json())

    def get_reasons_why_2_addresses_are_connected(
        self, address: str, related_address: str, chain: str
    ) -> str:
        """
        Returns the reason path why 2 addresses are connected.

        Sample Response:
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
                            ...
                        ]
                    },
                    ...
                ]
            },
            "uuid": 1656867198138187800
        }
        """
        url = f"{self.base_url}/entity/relatedReason?address={address}&related_address={related_address}&chain={chain}"
        response = requests.get(url, headers=self.headers)
        return json.dumps(response.json())

    def divide_addresses_into_entities(self, addresses: list[str], chain: str) -> str:
        """
        Divide input addresses into different entities.

        Sample Response:
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
        """
        url = f"{self.base_url}/entity/clusters"
        payload = {"addresses": addresses, "chain": chain}
        response = requests.post(url, json=payload, headers=self.headers)
        return json.dumps(response.json())

    def get_risky_score(self, address: str, chain: str) -> str:
        """
        Returns risky score of the address.

        Sample Response:
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
        """
        url = f"{self.base_url}/kye/riskyScore?address={address}&chain={chain}"
        response = requests.get(url, headers=self.headers)
        return json.dumps(response.json())

    def get_batch_risky_scores(self, addresses: list[str], chain: str) -> str:
        """
        Returns risky scores of a batch of addresses.

        Sample Response:
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
                ...
            ],
            "uuid": 1735178942656831500
        }
        """
        url = f"{self.base_url}/kye/batchRiskyScores"
        payload = {"addresses": addresses, "chain": chain}
        response = requests.post(url, json=payload, headers=self.headers)
        return json.dumps(response.json())

    def get_specific_risk_behavior(self, address: str, chain: str) -> str:
        """
        Returns specific risk behavior of the address.

        Sample Response:
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
                ...
            ],
            "uuid": 1668204706705182700
        }
        """
        url = (
            f"{self.base_url}/kye/specificRiskBehavior?address={address}&chain={chain}"
        )
        response = requests.get(url, headers=self.headers)
        return json.dumps(response.json())

    def get_batch_specific_risk_behavior(self, addresses: list[str], chain: str) -> str:
        """
        Returns specific risk behavior of a batch of addresses.

        Sample Response:
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
                            ...
                        },
                        ...
                    ]
                },
                ...
            ],
            "uuid": 1735179450259890200
        }
        """
        url = f"{self.base_url}/kye/batchSpecificRiskBehavior"
        payload = {"addresses": addresses, "chain": chain}
        response = requests.post(url, json=payload, headers=self.headers)
        return json.dumps(response.json())

    def get_entity_risk_score(self, address: str, chain: str) -> str:
        """
        Returns the risk score of other addresses belonging to the same entity as this address.

        Sample Response:
        {
            "code": 0,
            "data": [
                {
                    "address": "0xedd650a1b2d7e7049e1228bb5e60bd4cd5f7d67b",
                    "certainty": 9,
                    "riskScore": 99
                },
                ...
            ],
            "uuid": 1668204852293668900
        }
        """
        url = f"{self.base_url}/kye/entityRisk?address={address}&chain={chain}"
        response = requests.get(url, headers=self.headers)
        return json.dumps(response.json())

    def risk_detection_in_contract(self, contract_address: str, chain: str) -> str:
        """
        Detect possible risk items in the contract.

        Sample Response:
        {
            "code": 0,
            "data": {
                "address": "0x118b0af0e8e8f926c40e361ca934bca37ed8d23a",
                "is_risk": "1",
                "risk_behavior": "honey_pot",
                ...
            },
            "uuid": 1668207448877826000
        }
        """
        url = f"{self.base_url}/kye/riskDetection?contract_address={contract_address}&chain={chain}"
        response = requests.get(url, headers=self.headers)
        return json.dumps(response.json())

    def simulate_transaction_risk(
        self, chain: str, block_number: int, transaction: dict
    ) -> str:
        """
        Simulate the execution results of a transaction and reveal associated risks.

        Sample Response:
        {
            "code": 0,
            "data": {
                "simulationId": "ce87685c-5e62-49f2-bda8-7c55bc6ae1ef",
                "success": true,
                "gasUsed": 30404,
                ...
            },
            "uuid": 1732234437015916500
        }
        """
        url = f"{self.base_url}/kye/simulateTransactionRisk"
        payload = {
            "chain": chain,
            "block_number": block_number,
            "transaction": transaction,
        }
        response = requests.post(url, json=payload, headers=self.headers)
        return json.dumps(response.json())

    def get_twitter_info(self, address: str, chain: str) -> str:
        """
        Returns Twitter Infos of a Project or User.

        Sample Response:
        {
            "code": 0,
            "data": {
                "id": "635682749",
                "username": "suji_yan",
                "name": "Suji Yan - Mask is BUIDLing",
                ...
            },
            "uuid": 1656899742753751000
        }
        """
        url = f"{self.base_url}/social/twitterInfo?address={address}&chain={chain}"
        response = requests.get(url, headers=self.headers)
        return json.dumps(response.json())

    def get_batch_twitter_info(self, addresses: list[str], chain: str) -> str:
        """
        (batch) Returns twitter infos of a project or user in batch.

        Sample Response:
        {
            "code": 0,
            "data": [
                {
                    "id": "635682749",
                    "username": "suji_yan",
                    "name": "Suji Yan - Mask is BUIDLing",
                    ...
                },
                ...
            ],
            "uuid": 1656900011105321000
        }
        """
        url = f"{self.base_url}/social/twitterInfo_batch"
        payload = {"addresses": addresses, "chain": chain}
        response = requests.post(url, json=payload, headers=self.headers)
        return json.dumps(response.json())

    def get_twitter_activity_chart(self, address: str, chain: str) -> str:
        """
        Returns twitter send count of this project in a certain period of time.

        Sample Response:
        {
            "code": 0,
            "data": {
                "date": ["2023-05-06", "2023-05-07", ...],
                "official_count": [0, 0, ...],
                "other_count": [4, 4, ...]
            },
            "uuid": 1656900433727586300
        }
        """
        url = f"{self.base_url}/social/twitterActivityChart?address={address}&chain={chain}"
        response = requests.get(url, headers=self.headers)
        return json.dumps(response.json())

    def get_twitter_records_official(
        self, address: str, chain: str, limit: int = 10, page: int = 1
    ) -> str:
        """
        Twitter records from official twitter.

        Sample Response:
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
                        ...
                    },
                    ...
                ]
            },
            "uuid": 1656900671666258000
        }
        """
        url = f"{self.base_url}/social/twitterRecordsOfficial?address={address}&chain={chain}&limit={limit}&page={page}"
        response = requests.get(url, headers=self.headers)
        return json.dumps(response.json())

    def get_twitter_records_not_official(
        self, address: str, chain: str, limit: int = 10, page: int = 1
    ) -> str:
        """
        Twitter records from non-official twitter.

        Sample Response:
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
                        ...
                    },
                    ...
                ]
            },
            "uuid": 1656901727494209500
        }
        """
        url = f"{self.base_url}/social/twitterRecordsNotOfficial?address={address}&chain={chain}&limit={limit}&page={page}"
        response = requests.get(url, headers=self.headers)
        return json.dumps(response.json())

    def get_supported_nft_list(self, chain: str, limit: int = 10, page: int = 1) -> str:
        """
        Returns all NFTs currently being tracked.

        Sample Response:
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
                    ...
                ]
            },
            "uuid": 1656902602862231600
        }
        """
        url = f"{self.base_url}/nft/getSupportedNFTList?chain={chain}&limit={limit}&page={page}"
        response = requests.get(url, headers=self.headers)
        return json.dumps(response.json())

    def get_nft_info(self, contract_address: str, chain: str) -> str:
        """
        Returns information about a specific NFT.

        Sample Response:
        {
            "code": 0,
            "data": {
                "symbol": "AZUKI",
                ...
            },
            "uuid": 1656902837441265700
        }
        """
        url = f"{self.base_url}/nft/getInfo?contract_address={contract_address}&chain={chain}"
        response = requests.get(url, headers=self.headers)
        return json.dumps(response.json())

    def get_nft_market_statistics(self, contract_address: str, chain: str) -> str:
        """
        Returns the market statistics of a specific NFT.

        Sample Response:
        {
            "code": 0,
            "data": {
                "trades_count_24h": 59,
                ...
            },
            "uuid": 1656903022657536000
        }
        """
        url = f"{self.base_url}/nft/getMarketStatistics?contract_address={contract_address}&chain={chain}"
        response = requests.get(url, headers=self.headers)
        return json.dumps(response.json())

    def get_nft_price_chart(
        self, contract_address: str, chain: str, range: str = "1d"
    ) -> str:
        """
        Returns the floor price on every day for a specific NFT.

        Sample Response:
        {
            "code": 0,
            "data": [
                {"price": 13.42, "date": 1683785040000},
                {"price": 15.88, "date": 1683788640000},
                ...
            ],
            "uuid": 1656903180770214000
        }
        """
        url = f"{self.base_url}/nft/getPriceChart?contract_address={contract_address}&chain={chain}&range={range}"
        response = requests.get(url, headers=self.headers)
        return json.dumps(response.json())

    def get_nft_volume_chart(
        self, contract_address: str, chain: str, range: str = "1d"
    ) -> str:
        """
        Returns the volume on every day for a specific NFT.

        Sample Response:
        {
            "code": 0,
            "data": [
                {"volume_eth": 13.42, "date": 1683785040000},
                {"volume_eth": 47.64, "date": 1683788640000},
                ...
            ],
            "uuid": 1656903394897821700
        }
        """
        url = f"{self.base_url}/nft/getVolumeChart?contract_address={contract_address}&chain={chain}&range={range}"
        response = requests.get(url, headers=self.headers)
        return json.dumps(response.json())

    def get_nft_holder_statistics(self, contract_address: str, chain: str) -> str:
        """
        Returns holders statistics of a specific NFT.

        Sample Response:
        {
            "code": 0,
            "data": {
                "holder_count": 4701,
                "entity_count": 4186
            },
            "uuid": 1656903577001918500
        }
        """
        url = f"{self.base_url}/nft/getHolderStatistics?contract_address={contract_address}&chain={chain}"
        response = requests.get(url, headers=self.headers)
        return json.dumps(response.json())

    def get_nft_holder_statistics_daily(
        self, contract_address: str, chain: str, date: str
    ) -> str:
        """
        Returns holders statistics of a specific NFT at one day.

        Sample Response:
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
        """
        url = f"{self.base_url}/nft/getHolderStatisticsDaily?contract_address={contract_address}&chain={chain}&date={date}"
        response = requests.get(url, headers=self.headers)
        return json.dumps(response.json())

    def get_nft_top_100_holders(self, contract_address: str, chain: str) -> str:
        """
        Returns top 100 holders of a specific NFT.

        Sample Response:
        {
            "code": 0,
            "data": [
                {
                    "address": "0xd46c8648f2ac4ce1a1aace620460fbd24f640853",
                    "balance": 378
                },
                ...
            ],
            "uuid": 1656904198794903600
        }
        """
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
        """
        Returns trades of a specific NFT in a certain period of time.

        Sample Response:
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
                    ...
                ]
            },
            "uuid": 1656904536402821000
        }
        """
        url = f"{self.base_url}/nft/getTrades?contract_address={contract_address}&chain={chain}&begin_time={begin_time}&end_time={end_time}&limit={limit}&page={page}"
        response = requests.get(url, headers=self.headers)
        return json.dumps(response.json())

    def get_nft_profit_leader_board(
        self, contract_address: str, chain: str, limit: int = 10, page: int = 1
    ) -> str:
        """
        Returns the NFT Profit Leader Board.

        Sample Response:
        {
            "code": 0,
            "data": {
                "total": 200,
                "rows": [
                    {
                        "address": "0x866f1109fbef16beaaa46cf563e47c74f5c87ace",
                        "total_profit": 1058.5574389978,
                        ...
                    },
                    ...
                ]
            },
            "uuid": 1656904836924702700
        }
        """
        url = f"{self.base_url}/nft/profitLeaderBoard?contract_address={contract_address}&chain={chain}&limit={limit}&page={page}"
        response = requests.get(url, headers=self.headers)
        return json.dumps(response.json())

    def get_exchange_portfolio(self, exchange: str) -> str:
        """
        Returns the portfolio of the exchange on all chains.

        Parameters:
        - exchange (str): The name of the exchange (e.g., 'binance').

        Returns example:
        {
            "code": 0,
            "data": [
                {"chain": "Metis", "value": "98691.08456664431200"},
                ...
            ],
            "uuid": 1656906822223003600
        }
        """
        params = {"exchange": exchange}
        response = requests.get(
            f"{self.base_url}/exchange/getExchangePortfolio",
            headers=self.headers,
            params=params,
        )
        return json.dumps(response.json())

    def get_exchange_money_flow(self, exchange: str) -> str:
        """
        Returns the inflow/outflow of the exchange in the past 24 hours.

        Parameters:
        - exchange (str): The name of the exchange (e.g., 'binance').

        Returns example:
        {
            "code": 0,
            "data": {
                "inflow": 679374409.4316931,
                "outflow": 705421811.0646318,
                "netflow": -26047401.6329388
            },
            "uuid": 1656907251262554000
        }
        """
        params = {"exchange": exchange.lower()}
        response = requests.get(
            f"{self.base_url}/exchange/getExchangeMoneyFlow",
            headers=self.headers,
            params=params,
        )
        return json.dumps(response.json())

    def get_project_id_by_name(self, project_name: str, chain: str) -> str:
        """
        Retrieves the project ID by project name from all supported chains.

        :param project_name: The name of the project to search for.
        :param chain: The blockchain chain to search in.
        :return: The project ID as a string if found, else an empty string.
        """
        page = 1
        while True:
            projects_response = self.get_supported_projects(
                chain, limit=2000, page=page
            )
            projects_response_data = json.loads(projects_response)
            if projects_response_data["code"] != 0:
                print(f"Failed to retrieve projects for chain {chain}")
                break

            projects_data = projects_response_data["data"]
            total_projects = projects_data["total"]
            projects_per_page = projects_data["limit"]
            projects = projects_data["rows"]

            for project in projects:
                if project["project_name"].lower() == project_name.lower():
                    return json.dumps({"project_id": project["project_id"]})

            total_pages = (total_projects + projects_per_page - 1) // projects_per_page
            if page >= total_pages:
                break
            page += 1

        print(f"Project {project_name} not found in chain {chain}.")
        return json.dumps({})

    def get_project_detail_by_name(self, project_name: str, chain: str) -> str:
        """
        Get project details by project name.
        """
        project_id_response = self.get_project_id_by_name(project_name, chain)
        project_id_data = json.loads(project_id_response)
        if "project_id" in project_id_data:
            project_id = project_id_data["project_id"]
            return self.get_detail_of_the_project(project_id, chain)
        else:
            return json.dumps({"error": "Project not found"})

    def get_project_tvl_by_name(self, project_name: str, chain: str, date: str) -> str:
        """
        Get project TVL by project name for a specific date.
        """
        project_id_response = self.get_project_id_by_name(project_name, chain)
        project_id_data = json.loads(project_id_response)
        if "project_id" in project_id_data:
            project_id = project_id_data["project_id"]
            return self.get_tvl_of_the_project(project_id, chain, date)
        else:
            return json.dumps({"error": "Project not found"})

    def get_daily_active_address_by_name(
        self, project_name: str, chain: str, date: str
    ) -> str:
        """
        Get daily active address count of a project by project name for a specific date.
        """
        project_id_response = self.get_project_id_by_name(project_name, chain)
        project_id_data = json.loads(project_id_response)
        if "project_id" in project_id_data:
            project_id = project_id_data["project_id"]
            return self.get_daily_active_address_of_the_project(project_id, chain, date)
        else:
            return json.dumps({"error": "Project not found"})

    def get_daily_active_entity_by_name(
        self, project_name: str, chain: str, date: str
    ) -> str:
        """
        Get daily active entity count of a project by project name for a specific date.
        """
        project_id_response = self.get_project_id_by_name(project_name, chain)
        project_id_data = json.loads(project_id_response)
        if "project_id" in project_id_data:
            project_id = project_id_data["project_id"]
            return self.get_daily_active_entity_of_the_project(project_id, chain, date)
        else:
            return json.dumps({"error": "Project not found"})

    def get_daily_new_address_by_name(
        self, project_name: str, chain: str, date: str
    ) -> str:
        """
        Get daily new address count of a project by project name for a specific date.
        """
        project_id_response = self.get_project_id_by_name(project_name, chain)
        project_id_data = json.loads(project_id_response)
        if "project_id" in project_id_data:
            project_id = project_id_data["project_id"]
            return self.get_daily_new_address_of_the_project(project_id, chain, date)
        else:
            return json.dumps({"error": "Project not found"})

    def get_daily_new_entity_by_name(
        self, project_name: str, chain: str, date: str
    ) -> str:
        """
        Get daily new entity count of a project by project name for a specific date.
        """
        project_id_response = self.get_project_id_by_name(project_name, chain)
        project_id_data = json.loads(project_id_response)
        if "project_id" in project_id_data:
            project_id = project_id_data["project_id"]
            return self.get_daily_new_entity_of_the_project(project_id, chain, date)
        else:
            return json.dumps({"error": "Project not found"})

    def find_nft_by_name(self, nft_name: str) -> str:
        """
        Find NFT's contract address and chain by name.

        :param nft_name: The name of the NFT to search for.
        :return: JSON string containing the contract address and chain of the found NFT, or an error message if not found.
        """
        supported_chains_response = self.get_supported_chains()
        supported_chains_data = json.loads(supported_chains_response)

        if supported_chains_data["code"] == 0:
            for chain in supported_chains_data["data"]:
                page = 1
                while True:
                    nft_list_response = self.get_supported_nft_list(
                        chain, page=page
                    )
                    nft_list_data = json.loads(nft_list_response)

                    if nft_list_data["code"] == 0 and nft_list_data["data"]["rows"]:
                        for nft in nft_list_data["data"]["rows"]:
                            if nft["name"].lower() == nft_name.lower():
                                return json.dumps(
                                    {
                                        "contract_address": nft["contract_address"],
                                        "chain": chain,
                                    }
                                )
                        page += 1
                    else:
                        break
        return json.dumps({"error": "NFT not found"})
