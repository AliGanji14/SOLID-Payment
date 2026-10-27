import requests
from abc import ABC, abstractmethod


class AbstractPaymentGateway(ABC):
    @abstractmethod
    def initiate_payment():
        pass

    @abstractmethod
    def generate_payment_url():
        pass

    @abstractmethod
    def verify_payment():
        pass

    @abstractmethod
    def activate_sandbox():
        pass


class NovinoPayGateway(AbstractPaymentGateway):

    payment_init_url = "https://api.novinopay.com/payment/ipg/v2/request"
    payment_verify_url = "https://api.novinopay.com/payment/ipg/v2/verification"
    payment_gateway_url = "https://ipg.novinopay.com/StartPay/"

    def __init__(self, merchant_id, callback_url, sandbox=True):
        self.merchant_id = merchant_id
        self.callback_url = callback_url
        if sandbox:
            self.activate_sandbox()

    def initiate_payment(self, amount, invoice_id="", **kwargs):
        payload = {
            "merchant_id": self.merchant_id,
            "amount": amount,
            "callback_url": self.callback_url,
            "invoice_id": invoice_id,
        }
        if name := kwargs.get("name"):
            payload.update({"name": name})

        headers = {"content-type": "application/json"}
        response = requests.post(
            url=self.payment_init_url, json=payload, headers=headers
        )
        return response.json()

    def generate_payment_url(self, authority):
        return self.payment_gateway_url + str(authority)

    def verify_payment(self, amount, authority):
        payload = {
            "merchant_id": self.merchant_id,
            "amount": amount,
            "authority": authority,
        }
        headers = {"content-type": "application/json"}
        response = requests.post(
            url=self.payment_verify_url, json=payload, headers=headers
        )
        return response.json()

    def activate_sandbox(self):
        self.payment_init_url = "https://api.novinopay.com/payment/ipg/v2/request"
        self.payment_verify_url = (
            "https://api.novinopay.com/payment/ipg/v2/verification"
        )
        self.payment_gateway_url = "https://ipg.novinopay.com/StartPay/Sandbox/"
        self.merchant_id = "test"


if __name__ == "__main__":
    amount = 200000
    invoice_id = "14286594"

    payment_client = NovinoPayGateway("test", "https://localhost/callback")

    result_initiate = payment_client.initiate_payment(
        amount, invoice_id, name="ali ganji"
    )
    authority = result_initiate["data"]["authority"]

    payment_url = payment_client.generate_payment_url(authority)
    print("payment url : ", payment_url)

    input("enter something to start verifying...")
    result_verify = payment_client.verify_payment(amount, authority)
    print("verify resuly : ", result_verify)
