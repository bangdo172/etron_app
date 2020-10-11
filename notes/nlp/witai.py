from .wit import Wit

class WitEndpoint:
    def __init__(self):
        token = "RRVGH4Z5DP57IDPJ2NXQPEBHJH6UWRUT"
        self.wit_client = Wit(access_token=token)

    def processing(self, text):
        return self.wit_client.message(text)
        pass
