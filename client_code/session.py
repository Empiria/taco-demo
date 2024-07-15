from anvil_dapps import web3_onboard as w3o
import anvil

wallet = None
amoy = {
    "id": 0x13882,
    "token": "MATIC",
    "label": "Polygon Amoy Testnet",
    "rpcUrl": "https://rpc-amoy.polygon.technology/",
}
chains = [amoy]
wallets = [w3o.Metamask({"options": {"extensionOnly": False}}), w3o.InjectedWallets()]


def set_wallet():
    global wallet
    options = {"chains": chains, "wallets": wallets, "theme": "dark"}
    onboard = w3o.Onboard(options)
    wallet = onboard.connectWallet()[0]
    if wallet:
        onboard.setChain({"chainId": amoy["id"]})
    else:
        anvil.Notification(
            "You need to connect an ethereum wallet to encrypt or decrypt",
            title="Error",
            style="danger",
        ).show()
        set_wallet()
