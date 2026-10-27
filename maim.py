import requests
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional


@dataclass
class InitialPaymentResponse:
    success: bool
    message: str
    code: str
    authority: Optional[str] = None


@dataclass
class VerifyPaymentResponse:
    success: bool
    message: str
    code: str
    ref_id: Optional[str] = None
    trans_id: Optional[str] = None


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
    success_status_codes = [100, 101]

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

        try:
            response = requests.post(
                url=self.payment_init_url, json=payload, headers=headers
            ).json()
            if int(response["status"]) in self.success_status_codes:
                return InitialPaymentResponse(
                    success=True,
                    message=response["message"],
                    code=response["status"],
                    authority=response["data"]["authority"],
                )
            else:
                return InitialPaymentResponse(
                    success=False,
                    message=response["message"],
                    code=response["status"],
                    authority=None,
                )
        except:
            return {
                "success": False,
                "message": "connection error",
                "code": "-1000",
            }

    def generate_payment_url(self, authority):
        return self.payment_gateway_url + str(authority)

    def verify_payment(self, amount, authority):
        payload = {
            "merchant_id": self.merchant_id,
            "amount": amount,
            "authority": authority,
        }
        headers = {"content-type": "application/json"}

        try:
            response = requests.post(
                url=self.payment_verify_url, json=payload, headers=headers
            ).json()
            if int(response["status"]) in self.success_status_codes:
                return VerifyPaymentResponse(
                    success=True,
                    message=response["message"],
                    code=response["status"],
                    ref_id=response["data"]["ref_id"],
                    trans_id=response["data"]["trans_id"],
                )
            else:
                return VerifyPaymentResponse(
                    success=True,
                    message=response["message"],
                    code=response["status"],
                )
        except:
            return {
                "success": False,
                "message": "connection error",
                "code": "-1000",
            }

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

    authority = result_initiate.authority

    payment_url = payment_client.generate_payment_url(authority)
    print("payment url : ", payment_url)

    input("enter something to start verifying...")
    result_verify = payment_client.verify_payment(amount, authority)
    print("verify resuly : ", result_verify)
