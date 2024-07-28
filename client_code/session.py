from anvil_dapps import taco, web3_onboard as w3o
from anvil_dapps import ethers
import anvil

wallet = None
web3_provider = None
signer = None
domain = taco.domains.TESTNET
ritual_id = 0
porter_uri = taco.get_porter_uri(domain)
taco.initialize()

_amoy = {
    "id": 0x13882,
    "token": "MATIC",
    "label": "Polygon Amoy Testnet",
    "rpcUrl": "https://rpc-amoy.polygon.technology/",
}
_chains = [_amoy]
_wallets = [w3o.Metamask({"options": {"extensionOnly": False}}), w3o.InjectedWallets()]


def set_wallet():
    global wallet, web3_provider, signer
    options = {"chains": _chains, "wallets": _wallets, "theme": "dark"}
    onboard = w3o.Onboard(options)
    wallet = onboard.connectWallet()[0]
    if wallet:
        onboard.setChain({"chainId": _amoy["id"]})
        web3_provider = ethers.providers.Web3Provider(wallet.provider, "any")
        signer = web3_provider.getSigner()
    else:
        anvil.Notification(
            "You need to connect an ethereum wallet to encrypt or decrypt",
            title="Error",
            style="danger",
        ).show()
        set_wallet()
