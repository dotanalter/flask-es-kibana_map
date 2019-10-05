##############################################
# This is a Flask APP with single GET endpoint
# Dotan Alter
##############################################
from flask import Flask, jsonify, request
from elasticsearch import Elasticsearch
import requests
import geocoder

es = Elasticsearch(['elasticsearch'])
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
	ip = request.remote_addr

	########################################################
	# checks if the price entered by the user is an integer:
	########################################################
	try: 
		price = int(price)
	except:
		return "price parameter should be an integer"
	requests.put('http://localhost:9200/tracking')
	headers = {'Content-Type': 'application/json'}
	data = '\n{\n  "properties": {\n        "location": {\n          "type": "geo_point"\n        }\n      }\n   }'
	requests.put('http://localhost:9200/tracking/_mapping',headers=headers, data=data)
	g = geocoder.ip(ip)
	location = g.latlng
	if not location:
		g = geocoder.ip('me')
		location = g.latlng
	json_string= {
		"type":type,
		"product":product,
		"usage":usage,
		"price":price,
		"currency":currency,
		'ip': ip,
		"location": { 
    		"lat": location[0],
    		"lon": location[1]
  		}
	} #JSON object from parameters + user's ip address
	es.index(index='tracking', body=json_string) #send the JSON object to elasticsearch index named "tracking"
	return ("JSON object sent to elasticsearch check out http://127.0.0.1:9200/tracking")		


@app.errorhandler(400) #incase user does not enter full URL
def invaild_url(e):
	return("Please enter all the parameters to the URL")

@app.errorhandler(404) #incase user enters vaild URL
def invaild_url(e):
        return("Please enter vaild URL with /tracking route")

