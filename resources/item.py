from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help="This field cannot be left blank"
    )
    parser.add_argument('store_id',
        type=int,
        required=True,
        help="Every item needs a store id"
    )

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        else:
            return {'message': 'Item not found'}, 404

    
    def post(self, name):
        if ItemModel.find_by_name(name): # same as Item.find_by_name(name)
            return {'message': "An item with name '{} already exists".format(name)}, 400
        
        data = Item.parser.parse_args()

        item = ItemModel(name, **data) # (name, data['price'], data['store_id'])
        
        try:
            item.save_to_db()
        except:
            return {'message': 'An error occured inserting the item'}, 500

        return item.json(), 201

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()

        # query = "DELETE FROM items WHERE name=?"
        # cursor.execute(query, (name,))

        # connection.commit()
        # connection.close()

        return {'messge':"Item deleted"}

    def put(self, name):
        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)
        # updated_item = ItemModel(name, data['price'])

        if item is None:
            item = ItemModel(name, data['price'], data['store_id'])
            # try:
            #     updated_item.insert()
            # except:
            #     return {'message': "An error occurred inserting the item"}, 500          
        else:
            item.price = data['price']
            # try:
            #     updated_item.update()
            # except:
            #     return {'message': "An error occurred updating the item"}, 500  
        item.save_to_db()
        return item.json()  #updated_item.json()


class ItemList(Resource):
    def get(self):
        return {'items': [item.json() for item in ItemModel.query.all()]}
        # same as return {'items': list(map(lambda x: x.json(), ItemModel.query.all()))}

        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()

        # query = "SELECT * FROM items"
        # result = cursor.execute(query)

        # items = []
        # for row in result:
        #     items.append({'name': row[1], 'price': row[2]})

        # connection.close()
        # return {'items': items}
