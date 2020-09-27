from wit import Wit

token = "RRVGH4Z5DP57IDPJ2NXQPEBHJH6UWRUT"
text = "hẹn họp với Bằng chiều chủ nhật tuần này"

client = Wit(access_token=token)
wit_resp = client.message(text)

query_text = wit_resp["text"]
query_intent = wit_resp["intents"][0]["name"]
query_entities = wit_resp["entities"]

class NLP:
    def __init__(self):
        token = "RRVGH4Z5DP57IDPJ2NXQPEBHJH6UWRUT"
        self.wit_client = Wit(access_token=token)
    
    def remind(self):
        pass 

    def query(self):
        pass

    def update(self):
        pass 

    def processing(self, request):
        request_processing 

