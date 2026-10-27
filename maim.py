import requests

MERCHANT_ID = "test"
CALLBACK_URL = "https://localhost/callback"


def initiate_payment(amount, invoice_id="", **kwargs):
    url = "https://api.novinopay.com/payment/ipg/v2/request"
    payload = {
        "merchant_id": MERCHANT_ID,
        "amount": amount,
        "callback_url": CALLBACK_URL,
        "invoice_id": invoice_id,
    }
    if name := kwargs.get("name"):
        payload.update({"name": name})

    headers = {"content-type": "application/json"}
    response = requests.post(url=url, json=payload, headers=headers)
    return response.json()


def generate_payment_url(authority):
    return f"https://ipg.novinopay.com/StartPay/Sandbox/{authority}"


def verify_payment(amount, authority):
    url = "https://api.novinopay.com/payment/ipg/v2/verification"
    payload = {
        "merchant_id": MERCHANT_ID,
        "amount": amount,
        "authority": authority,
    }
    headers = {"content-type": "application/json"}
    response = requests.post(url=url, json=payload, headers=headers)
    return response.json()


if __name__ == "__main__":
    amount = 200000
    invoice_id = "14286594"
    
    result_initiate = initiate_payment(amount, invoice_id, name = "ali ganji")
    authority = result_initiate["data"]["authority"]

    payment_url = generate_payment_url(authority)
    print("payment url : ", payment_url)

    input("enter something to start verifying...")
    result_verify = verify_payment(amount, authority)
    print("verify resuly : ", result_verify)
