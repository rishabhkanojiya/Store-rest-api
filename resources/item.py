import sqlite3
from flask_restful import Resource,reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

class Items(Resource):

	parser = reqparse.RequestParser()
	parser.add_argument('price',
			type=float,
			required = True,
			help = "This field cannto be accepted"
		)

	parser.add_argument('store_id',
			type=int,
			required = True,
			help = "Every item requires a store id"
		)
	
	def get(self,name):
		item = ItemModel.find_by_name(name)

		if item:
			return item.json()
		return {'message':'item not found'},404

	def post(self,name):
		
		if ItemModel.find_by_name(name):
			return {'Message':'item already exist'},400

		data = Items.parser.parse_args()
		item = ItemModel(name,data['price'],data['store_id'])

		try:
			item.save_to_db()
		except:
			return {'message':'an error occured inserting the item'},500

		return item.json() , 201
	

	@jwt_required()
	def delete(self,name):
		
		item =ItemModel.find_by_name(name)

		if item:
			item.delete_from_db()

		return {'Message':'item deleted'}

	def put(self,name):
		
		data = Items.parser.parse_args()
		
		item  = ItemModel.find_by_name(name)

		if item is None:
			
			item = ItemModel(name,data['price'],data['store_id'])
		else:
			item.price = data['price']
			item.store_id = data['store_id']

		item.save_to_db()
		return item.json()


class itemlist(Resource):
	
	def get(self):  	
		
		return {'Item':list(map(lambda x : x.json(),ItemModel.query.all()))}
