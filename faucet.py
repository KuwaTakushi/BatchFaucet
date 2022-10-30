# w3 library
from gettext import find
from multiprocessing.sharedctypes import Value
from web3 import Web3, HTTPProvider
from web3.exceptions import TransactionNotFound

# eth library
from eth_abi import encoding
from eth_account import Account as EthAccount

import logging
from typing import (
    Any, AnyStr, Container, Dict, List, 
    TypeVar, Union, NewType, Tuple, Callable, Optional
)

Abi:        List[Dict] = ...
Keyword:    Union[str, None] = ...
Arg:        Union[AnyStr, None] = ...
HexStr:     NewType('HexStr', str) = ...

Addr:       NewType('Addr', HexStr) = ...
Func:       NewType('Function', str)  = ...
Encode:     NewType('Encode', HexStr) = ...
EthValue:   TypeVar('EthValue', int, float) = ...
EnsDomain:  NewType('EnsDomain', str) = ...

AlCHEMY_GOERLI  = "https://eth-goerli.g.alchemy.com/v2/8pjvTLWK2Cr0bCf04Ih4IlkLRq5o82UO"

w3 = Web3(HTTPProvider(AlCHEMY_GOERLI))

def send_ether_faucet(
    send: str, 
    to: list[Addr], 
    value: Union[int, float], 
    chain_id, 
    privatekey: str
) -> bool:
    if not any([send, to, value]): raise ValueError("The input data is wrong!")
    balacne = w3.fromWei(w3.eth.get_balance(send), 'ether') 
    
    if len(to) == 1:
        if value <= balacne:
            transaction = {
                'nonce':    w3.eth.getTransactionCount(send),
                'from':     send,
                'to':       to[0],
                'value':    w3.toWei(value, 'ether'),
                'gas':      210000,
                'gasPrice': w3.toWei('150', 'gwei'),
                'chainId':  chain_id
            }

            signed_transaction = w3.eth.account.sign_transaction(transaction, privatekey)
            tx_hash = w3.eth.sendRawTransaction(signed_transaction.rawTransaction)
            # Check transaction results immediately.
            event = recover_transaction_hash(pending_tx_hash=tx_hash)
            print("The wallet: {}".format(to[0]))
            print("The tx_hash: {} result: {}".format(w3.toHex(tx_hash), event[2]))
        else:
            raise ValueError("The number of transfers exceeds the balance.")

    else:
        if (value * len(to)) <= balacne:
            for i in range(0, len(to)):
                transaction = {
                    'nonce':    w3.eth.getTransactionCount(send),
                    'from':     send,
                    'to':       to[i],
                    'value':    w3.toWei(value, 'ether'),
                    'gas':      210000,
                    'gasPrice': w3.toWei('150', 'gwei'),
                    'chainId':  chain_id
                }
                signed_transaction = w3.eth.account.sign_transaction(transaction, privatekey)
                tx_hash = w3.eth.sendRawTransaction(signed_transaction.rawTransaction)
                # Check transaction results immediately.
                event = recover_transaction_hash(pending_tx_hash=tx_hash)
                print("The wallet: {}".format(to[i]))
                print("The tx_hash: {} result: {}\n".format(w3.toHex(tx_hash), event[2]))
        else:
            raise ValueError("The number of transfers exceeds the balance.")

def recover_transaction_hash(tx_hash: HexStr=None, pending_tx_hash: HexStr=None) -> Any:
    data = ...
    if tx_hash:
        data = w3.eth.getTransactionReceipt(tx_hash)
        return (
            data['from'],
            data['to'],
            'Success' if data['status'] == 1 else 'Failed',
            data['blockNumber'],
        )
    
    # A peeding transaction hash need to return confirmation results immediately.
    if pending_tx_hash:
        data = w3.eth.wait_for_transaction_receipt(pending_tx_hash, timeout=120, poll_latency=1)
        return (
            data['from'],
            data['to'],
            'Success' if data['status'] == 1 else 'Failed',
            data['blockNumber'],
        )

import os
def read_wallet():
    current = os.path.abspath(__file__)
    dir = str(os.path.abspath(os.path.dirname(current)))
    with open(str(dir+'\wallet.txt').replace('\\', '/')) as file:
        yield file.readlines()
             

if __name__ == '__main__':

    faucetSenderA = '0x6FE43f68f17024d41A5d0f774765c2B4f9d7F305'
    privateA = '9aad317f6edcb1db275a1b6412faaa9193776157ef80f3cc740ca7b2d570436e'


    faucetSenderB = '0x576833276D9C5878536613a9fA2b36290F56a2e1'
    privateB = '0x2ee828008669c2a1d5cb8d74aac66c5c4777a0e158c1ec7b5839954655cca8a5'

    faucetSenderC = '0x2797eD64486e2985BcbB71387601Aff96ad6e806'
    privateC = '0xedec71d3a8adda3b3cfa1ec25a08f431f29e35e666f0ba8d9f5ee84f218f16cc'

    print(
        '池编号"1"： \n0x6FE43f68f17024d41A5d0f774765c2B4f9d7F305 池当前余额：{}ETH\n'.format(
        w3.fromWei(w3.eth.get_balance('0x6FE43f68f17024d41A5d0f774765c2B4f9d7F305'), 'ether'))
        )

    print(
        '池编号"2"： \n0x576833276D9C5878536613a9fA2b36290F56a2e1 池当前余额：{}ETH\n'.format(
        w3.fromWei(w3.eth.get_balance('0x576833276D9C5878536613a9fA2b36290F56a2e1'), 'ether'))
        )

    print(
    '池编号"3"： \n0x2797eD64486e2985BcbB71387601Aff96ad6e806 池当前余额：{}ETH\n'.format(
    w3.fromWei(w3.eth.get_balance('0x2797eD64486e2985BcbB71387601Aff96ad6e806'), 'ether'))
    )


    toAddress = [addr.replace('\n', '') for addr in next(read_wallet())]
    
    print("请选择池编号进行发送:")
    scanner = str(input())
    if scanner:
        print("正在发送中.......")
        if "1" in scanner:
            send_ether_faucet(
                send=faucetSenderA,
                to=toAddress,
                privatekey=privateA,
                value=0.05,
                chain_id=5
            )
            print("所有ETH水龙发送完毕")

        elif "2" in scanner:
            send_ether_faucet(
                send=faucetSenderB,
                to=toAddress,
                privatekey=privateB,
                value=0.05,
                chain_id=5
            )
            print("所有ETH水龙发送完毕")

        elif "3" in scanner:
            send_ether_faucet(
                send=faucetSenderC,
                to=toAddress,
                privatekey=privateC,
                value=0.05,
                chain_id=5
            )
            print("所有ETH水龙发送完毕")
        
        else:
            raise ValueError("The input pool_id is wrong!")
            
    input('Press Enter to exit: \n')
