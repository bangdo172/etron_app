from elasticsearch import Elasticsearch


es = Elasticsearch()

res = es.search(index='messages', body = {})

print(res)

