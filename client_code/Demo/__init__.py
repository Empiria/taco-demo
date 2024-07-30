from ._anvil_designer import DemoTemplate
from anvil_dapps import taco
import anvil
from .. import session
from ..services.colours import switch_colour_scheme
import anvil.js


themes = {"dark": "Material Dark", "light": "Material Light"}


def on_message(event):
    try:
        switch_colour_scheme(themes[event.data.theme])
    except Exception:
        return


def within_iframe():
    return anvil.js.window != anvil.js.window.parent


encrypt_intro = """
### Encryption
Enter your plaintext and set the conditions which must be met in order for the decryption key to be made available.

When you try to encrypt, you'll be prompted to connect a wallet if you haven't already done so and then to sign a transaction.

If encryption is successful, you'll see your encrypted ciphertext appear.
"""

decrypt_intro = """
### Decryption
Enter the ciphertext you'd like to decrypt.

When you try to decrypt, you'll be prompted to connect a wallet if you haven't already done so and then to sign a transaction.

If the conditions are met and decryption is successful, you'll see the orginal plaintext appear.
"""


class Demo(DemoTemplate):
    def __init__(self, **properties):
        self.plaintext = None
        self.message_kit = None
        self.rich_text_1.content = encrypt_intro
        self.rich_text_2.content = decrypt_intro
        if within_iframe():
            anvil.js.window.addEventListener("message", on_message)
            anvil.js.window.parent.postMessage({"requestTheme": True}, "*")
        self.init_components(**properties)

    @property
    def ciphertext(self):
        return self.message_kit.toBytes().hex() if self.message_kit else None

    def encrypt_button_click(self, **event_args):
        if session.wallet is None:
            session.set_wallet()
        condition = self.taco_conditions.result
        try:
            self.message_kit = taco.encrypt(
                session.web3_provider,
                session.domain,
                self.plaintext.encode(),
                condition,
                session.ritual_id,
                session.signer,
            )
        except ValueError as e:
            anvil.Notification(
                str(e), title="Encryption failed", style="danger", timeout=None
            ).show()
        self.plaintext = None
        self.refresh_data_bindings()

    def decrypt_button_click(self, **event_args):
        if session.wallet is None:
            session.set_wallet()
        self.refresh_data_bindings()
        try:
            with anvil.Notification("Decrypting...", title="Please wait"):
                self.plaintext = taco.decrypt(
                    session.web3_provider, session.domain, self.message_kit, session.porter_uri, session.signer
                ).decode()
            self.message_kit = None
        except ValueError as e:
            anvil.Notification(
                str(e), title="Decryption failed", style="danger", timeout=None
            ).show()
        self.refresh_data_bindings()

    def textbox_change(self, **event_args):
        self.refresh_data_bindings()

    def plaintext_textbox_change(self, sender, **event_args):
        self.plaintext = sender.text
        self.refresh_data_bindings()
