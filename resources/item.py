import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item_model import ItemModel
items = []


class Item(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="This field cannot be left blank.")
    parser.add_argument('store_id',
                        type=int,
                        required=True,
                        help="Every item needs a Store ID.")

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'Item not found.'}, 404


    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': "An item with name '{}' already exists.".format(name)}, 400

        data = Item.parser.parse_args()
        itemNew = ItemModel(name, data['price'], data['store_id'])
        try:
            itemNew.save_to_db()
        except:
            return {"message": "An error occurred inserting the item."}, 500

        return itemNew.json(), 201


    def put(self, name):
        data = Item.parser.parse_args()
        Newitem = ItemModel.find_by_name(name)
        if Newitem is None:
            Newitem = ItemModel(name, data['price'], data['store_id'])
        else:
            Newitem.price = data['price']
            Newitem.store_id = data['store_id']
        print(Newitem.price)
        Newitem.save_to_db()
        return Newitem.json()

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            return {'message': 'Item {} Deleted'.format(name)}
        else:
            return {'message': 'Item {} Not Found'.format(name)}


class ItemList(Resource):
    def get(self):
        return {'items': [item.json() for item in ItemModel.query.all()]}, 201
