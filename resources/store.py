from flask_restful import Resource,reqparse
from models.store import StoreModel

class Store(Resource):

	def get(slef,name):
		store = StoreModel.find_by_name(name)

		if store:
			return store.json()
		return {'Message':'Store Not found'},404

	def post(self,name):
		store = StoreModel.find_by_name(name)
		if store:
			return {'Message':'Store already exist'},400

		store = StoreModel(name)
		try:
			store.save_to_db()
		except:
			return {'Message':'An error accoured while inserting an Store'},500

		return store.json(),201


	def delete(self,name):
		
		store = StoreModel.find_by_name(name)
		if store:
			store.delete_from_db()
		return {'Message':'Item Deleted'}


class StoreList(Resource):

	def get(self):
		
		return {'item':list(map(lambda x : x.json(),StoreModel.query.all()))}
		return {'Item':list(map(lambda x : x.json(),ItemModel.query.all()))}