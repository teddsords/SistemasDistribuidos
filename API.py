from flask import Flask
from flask_restful import Resource, Api, reqparse
import pandas as pd
import ast

app = Flask(__name__)
api = Api(app)

# /users
users_path = 'users.csv'

# /locations
location_path = 'locations.csv'

class Users(Resource):
    def get(self):
        data = pd.read_csv(users_path)
        data = data.to_dict()
        return {'data': data}, 200


    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('userId', required=True, type=int)
        parser.add_argument('name', required=True, type=str)
        parser.add_argument('city', required=True, type=str)
        args = parser.parse_args()

        data = pd.read_csv(users_path)

        if args['userId'] in data['userId']:
            return {
                'message' : f"{args['userId']} already exists"
            }, 409
        else:
            data = data.append({
                'userId' : str(args['userId']),
                'name' : args['name'],
                'city' : args['city'],
                'locations' : []
            }, ignore_index=True)
            data.to_csv(users_path, index=False)

            return {'data': data.to_dict()}, 201
 
 
    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('userId', required=True)
        parser.add_argument('location', required=True)
        args = parser.parse_args()

        data = pd.read_csv(users_path)
        
        if args['userId'] in list(data['userId']):
            data['locations'] = data['locations'].apply(
                lambda x: ast.literal_eval(x)
            )

            user_data = data[data['userId'] == args['userId']]

            user_data['locations'] = user_data['locations'].values[0].append(args['location'])
            data.to_csv(users_path, index=False)

            return {'data': data.to_dict()}, 201

        else:
            return{
                'message': f"{args['userId']} user not found"
            }, 404


    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('userId', required=True)
        args = parser.parse_args()

        data = pd.read_csv(users_path)

        if args['userId'] in list(data['userId']):
            data = data[data['userId'] != str(args['userId'])]
            data.to_csv(users_path, index=False)
            return{'data': data.to_dict()}, 201

        else:
            return{'message': f"{args['userId']} doesn't exist!"}, 404
          

class Locations(Resource):
    
    def get(self):
        data = pd.read_csv(location_path)
        data = data.to_dict()
        return {'data': data}, 200

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('locationId', required=True, type=int)
        parser.add_argument('name', required=True, type=str)
        parser.add_argument('rating', required=True)
        args = parser.parse_args()

        data = pd.read_csv(location_path)

        if args['locationId'] in data['locationId']:
            return{
                'message': f"{args['locationId']} already exists"
            }, 409

        else:
            data = data.append({
                'locationId': args['locationId'],
                'name': args['name'],
                'rating': args['rating']
            }, ignore_index=True)
            data.to_csv(location_path, index=False)

            return{'data': data.to_dict()}, 200
   
    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('locationId', required=True, type=int)
        parser.add_argument('name', required=True)
        parser.add_argument('rating', required=True)
        args = parser.parse_args()

        data = pd.read_csv(location_path)
        
        if args['locationId'] in list(data['locationId']):
            location_data = data[data['locationId'] == args['locationId']]
            
            if 'name' in args:
                location_data['name'] = args['name']
            if 'rating' in args:
                location_data['rating'] = args['rating']


            data[data['locationId'] == args['locationId']] = location_data

            data.to_csv(location_path, index=False)

            return {'data': data.to_dict()}, 200

        else:
            return{
                'message': f"location {args['locationId']} not found"
            }, 404


    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('locationId', required=True, type=int)
        args = parser.parse_args()

        data = pd.read_csv(location_path)

        if args['locationId'] in list(data['locationId']):
            data = data[data['locationId'] != args['locationId']]
            data.to_csv(location_path, index=False)

            return {'data': data.to_dict()}, 200

        else:
            return {
                "message": f"{args['locationId']} doesn't exist"
            }, 404

api.add_resource(Users, '/users')   # '/users' is our entry point for Users
api.add_resource(Locations, '/locations')   # '/locations' is our entry for Locations


if __name__ == '__main__':
    app.run(debug=True)   # run our Flask app
