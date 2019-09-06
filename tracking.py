##############################################
# This is a Flask APP with single GET endpoint
# Dotan Alter
##############################################
from flask import Flask, jsonify, request
from elasticsearch import Elasticsearch

es = Elasticsearch()
app = Flask(__name__)

@app.route('/tracking', methods=['GET'])
def sendJSONtoES():
	######################################
	# implementing variables from the URL:
	######################################
	type = request.args['type']
	product = request.args['product']
	usage = request.args['usage']
	price = request.args['price'] 
	currency = request.args['currency']

	########################################################
	# checks if the price entered by the user is an integer:
	########################################################
	try: 
		price = int(price)
	except:
		return "price parameter should be an integer"

	json_string={"type":type,"product":product,"usage":usage,"price":price,"currency":currency,'ip': request.remote_addr} #JSON object from parameters + user's ip address
	es.index(index='tracking', doc_type='tracking', body=json_string) #send the JSON object to elasticsearch index named "tracking"
	return ("JSON object sent to elasticsearch check out http://127.0.0.1:9200/tracking")		


@app.errorhandler(400) #incase user does not enter full URL
def invaild_url(e):
	return("Please enter all the parameters to the URL")

@app.errorhandler(404) #incase user enters vaild URL
def invaild_url(e):
        return("Please enter vaild URL with /tracking route")


