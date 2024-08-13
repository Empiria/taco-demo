from anvil_dapps import taco, web3_onboard as w3o
from anvil_dapps import ethers
import anvil


AMOY = {
    "id": 0x13882,
    "token": "MATIC",
    "label": "Polygon Amoy Testnet",
    "rpcUrl": "https://rpc-amoy.polygon.technology/",
}
CHAINS = [AMOY]
WALLETS = [w3o.Metamask({"options": {"extensionOnly": False}}), w3o.InjectedWallets()]


class Session:
    def __init__(self):
        self.wallet = None
        self.web3_provider = None
        self.signer = None
        self.domain = taco.domains.TESTNET
        self.ritual_id = 0
        self.porter_uri = taco.get_porter_uri(self.domain)
        taco.initialize()

    def set_wallet(self):
        options = {"chains": CHAINS, "wallets": WALLETS, "theme": "dark"}
        onboard = w3o.Onboard(options)
        self.wallet = onboard.connectWallet()[0]
        if self.wallet:
            onboard.setChain({"chainId": AMOY["id"]})
            self.web3_provider = ethers.providers.Web3Provider(self.wallet.provider, "any")
            self.signer = self.web3_provider.getSigner()
        else:
            anvil.Notification(
                "You need to connect an ethereum wallet to encrypt or decrypt",
                title="Error",
                style="danger",
            ).show()
            self.set_wallet()


session = Session()
