from typing import Literal 
import os
from web3 import Web3
import numpy as np
import requests
import json
from bs4 import BeautifulSoup
from langchain_anthropic import ChatAnthropic
from langchain_cohere import ChatCohere
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import (
    PromptTemplate
)
from langchain_openai import ChatOpenAI
from langchain_core.runnables import ConfigurableField

from langchain_core.output_parsers import StrOutputParser


def get_token_symbol(contract_address):
    """
    Get the token symbol for a given Ethereum contract address using Web3.py.

    :param contract_address: Contract address of the token.
    :return: Token symbol or None if not found.
    """
    INFURA_API_KEY = os.getenv("INFURA_API_KEY")
    if not INFURA_API_KEY:
        raise Exception("There is no env INFURA_API_KEY")
    # 连接到Infura的以太坊节点
    infura_url = f"https://mainnet.infura.io/v3/{INFURA_API_KEY}"
    ethers = Web3(Web3.HTTPProvider(infura_url))
    erc20_abi = [
        {
            "constant": True,
            "inputs": [],
            "name": "symbol",
            "outputs": [{"name": "", "type": "string"}],
            "payable": False,
            "stateMutability": "view",
            "type": "function",
        }
    ]

    contract = ethers.eth.contract(
        address=Web3.to_checksum_address(contract_address), abi=erc20_abi
    )
    try:
        symbol = contract.functions.symbol().call()
        return symbol
    except Exception as e:
        print(f"Error: {e}")
        return None


def get_address_tag(address):
    url = f"https://etherscan.io/address/{address}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }

    # 发送HTTP GET请求到Etherscan地址页面
    response = requests.get(url, headers=headers)

    # 检查请求是否成功
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")

        # 查找包含标签的HTML元素
        tag_element = soup.find("span", {"class": "hash-tag text-truncate lh-sm my-n1"})

        if tag_element:
            return tag_element.text.strip()
        else:
            return "No tag found"
    else:
        return f"Failed to retrieve page, status code: {response.status_code}"

# If necessary, redis needs to be used here.
address_info_cache = {}


def get_funds_transfer_status_in_transaction_data(tx_hash: str) -> any:
    """
    Useful when you need get funds transfer status in a Ethereum's transaction. Input for this should be a complete transaction's hash.
    """

    result = {}

    INFURA_API_KEY = os.getenv("INFURA_API_KEY")
    if not INFURA_API_KEY:
        raise Exception("There is no env INFURA_API_KEY")
    # 连接到Infura的以太坊节点
    infura_url = f"https://mainnet.infura.io/v3/{INFURA_API_KEY}"
    ethers = Web3(Web3.HTTPProvider(infura_url))
    # transaction
    transaction = ethers.eth.get_transaction(tx_hash)
    # RPC请求获取交易的trace
    trace_call = {
        "jsonrpc": "2.0",
        "method": "trace_transaction",
        "params": [tx_hash],
        "id": 1,
    }

    response = ethers.manager.request_blocking(
        trace_call["method"], trace_call["params"]
    )
    data = json.loads(ethers.to_json(response))
    _action = [d["action"] for d in data if d["action"]["callType"] == "call"]
    eth_transfer_action = []
    for act in _action:
        act["value"] = int(act["value"], 16)
        act["gas"] = int(act["gas"], 16)
        act["inpu"] = ""  # 去掉input节省token
        if act["value"] > 0:
            act["value"] = Web3.from_wei(act["value"], "ether").to_eng_string()
            eth_transfer_action.append(act)
    # logs
    event_signature_hash = ethers.keccak(text="Transfer(address,address,uint256)").hex()
    receipt = ethers.eth.get_transaction_receipt(tx_hash)
    if receipt and receipt["logs"]:
        logs = [
            log
            for log in receipt["logs"]
            if log["topics"][0].hex() == event_signature_hash
        ]
        decoded_logs = []
        for log in logs:
            if log["topics"][0].hex() == event_signature_hash:
                # 解析 Transfer 事件
                from_address = Web3.to_checksum_address(
                    "0x" + log["topics"][1].hex()[-40:]
                )
                to_address = Web3.to_checksum_address(
                    "0x" + log["topics"][2].hex()[-40:]
                )
                value = int(log["data"].hex(), 16)
                decoded_logs.append(
                    {
                        "from": from_address,
                        "to": to_address,
                        "value": Web3.from_wei(value, "ether").to_eng_string(),
                        "token_contract_address": log["address"],
                        # "token_symbol": get_token_symbol(log["address"]),
                    }
                )
            transaction = json.loads(ethers.to_json(transaction))
            transaction["input"] = ""  # 节省token
            result = {
                "transaction": transaction,
                "eth_transfer_action": eth_transfer_action,
                "token_transfer_action": decoded_logs,
            }
    else:
        result = {
            "transaction": json.loads(ethers.to_json(transaction)),
            "eth_transfer_action": eth_transfer_action,
        }
    address_list = (
        [result["transaction"]["from"]]
        + [result["transaction"]["to"]]
        + [t["from"] for t in result["eth_transfer_action"]]
        + [t["to"] for t in result["eth_transfer_action"]]
        + [t["from"] for t in result["token_transfer_action"]]
        + [t["to"] for t in result["token_transfer_action"]]
    )
    unique_addresses = np.unique(address_list)
    no_cached_address = [ad for ad in unique_addresses if ad not in address_info_cache]
    for ad in no_cached_address:
        ad_info = {
            "address": ad,
            "symbol": get_token_symbol(ad),
            "tag": get_address_tag(ad),
        }
        address_info_cache[ad] = ad_info
    ad_info = [address_info_cache[ad] for ad in unique_addresses]
    result["address_info"] = ad_info
    return result


def get_funds_transfer_status_in_transaction_with_chain(
    tx_hash: str,
    llm_key: Literal[
        "openai_gpt_3_5_turbo_1106",
        "openai_gpt_4_turbo_preview",
        "openai_gpt_4o",
        "mistral_large",
        "command_r_plus",
    ] = "openai_gpt_4o",
) -> str:
    """
    Useful when you need get funds transfer status in a Ethereum's transaction. Input for this should be a complete transaction's hash.
    """
    llm = ChatAnthropic(
        model="claude-3-opus-20240229",
        # max_tokens=,
        temperature=0.9,
        # anthropic_api_key=os.environ.get("ANTHROPIC_API_KEY", "not_provided"),
        streaming=True,
        verbose=True,
    ).configurable_alternatives(  # This gives this field an id
        # When configuring the end runnable, we can then use this id to configure this field
        ConfigurableField(id="llm"),
        # default_key="openai_gpt_4_turbo_preview",
        default_key="anthropic_claude_3_opus",
        openai_gpt_3_5_turbo_1106=ChatOpenAI(
            model="gpt-3.5-turbo-1106",
            verbose=True,
            streaming=True,
            temperature=0.9,
        ),
        openai_gpt_4_turbo_preview=ChatOpenAI(
            temperature=0.9,
            model="gpt-4-turbo-preview",
            verbose=True,
            streaming=True,
        ),
        openai_gpt_4o=ChatOpenAI(
            temperature=0.9,
            model="gpt-4o",
            verbose=True,
            streaming=True,
        ),
        mistral_large=ChatMistralAI(
            model="mistral-large-latest", temperature=0.1, verbose=True, streaming=True
        ),
        command_r_plus=ChatCohere(
            model="command-r-plus", temperature=0.9, verbose=True, streaming=True
        ),
    )
    llm_chain = llm.with_config({"configurable": {"llm": llm_key}})
    data=get_funds_transfer_status_in_transaction_data(tx_hash=tx_hash)
    prompt_template="""
Answer questions based on transaction data.
When answering the question, please inform the symbol of the token corresponding to the contract address.
The from and to addresses of token transfer need to indicate their tags.

If there are burn tokens and mint tokens in the data, do not use transfer to describe these data. The data examples of burn tokens and mint tokens are as follows:
Burn token example:
```json
{{
			"from": "0x3AA228a80F50763045BDfc45012dA124Bd0a6809",
			"to": "0x0000000000000000000000000000000000000000",
			"value": "0.6",
			"token_contract_address": "0x7f39C581F595B53c5cb19bD0b3f8dA6c935E2Ca0",
			"token_symbol": "wstETH"
		}}
```
This data shows that the address 0x3AA228a80F50763045BDfc45012dA124Bd0a6809 destroyed 0.6 wstETH belonging to him.

Mint token example:
```json
{{
			"from": "0x0000000000000000000000000000000000000000",
			"to": "0x3AA228a80F50763045BDfc45012dA124Bd0a6809",
			"value": "0.693330246138990696",
			"token_contract_address": "0xD9A442856C234a39a81a089C06451EBAa4306a72",
			"token_symbol": "pufETH"
		}}
```
This data indicates that the address 0x3AA228a80F50763045BDfc45012dA124Bd0a6809 minted 0.693330246138990696 pufETH.

Question: What is the transfer status of tokens and eth in the following transaction?

Transaction data: 
```json
{tx_data}
```

Answer:
"""
    _chain=PromptTemplate.from_template(prompt_template)|llm_chain|StrOutputParser()
    return _chain.invoke({"tx_data":json.dumps(data)}) 
