from flask import Flask, jsonify, request
import json
from Login import Login
from SignUp import Signup

#declared an empty variable for reassignment
response = ''

#creating the instance of our flask application
app = Flask(__name__)
@app.route('/')
def Test():
    return "<H1>Hello</H1>"
#route to entertain our post and get request from flutter app
@app.route('/login', methods = ['GET', 'POST'])
def LoginRoute():

    #fetching the global response variable to manipulate inside the function
    global response
    

    if(request.method == 'POST'):
        request_data = request.data
        request_data = json.loads(request_data.decode('utf-8'))
        username = request_data['username']
        password = request_data['password']
        
        try:
            login = Login(username,password)
            username = login.account.username
            email = login.account.email
            response = jsonify({"error":"Logged in","account":{"email":email,"username":username}})
            return response
        except Exception as e:
            
            response = jsonify({"error":str(e),"account":'None'})
            return response
    else:
        return response
    #checking the request type we get from the app
    # if(request.method == 'POST'):
    #     request_data = request.data #getting the response data
    #     request_data = json.loads(request_data.decode('utf-8')) #converting it from json to key value pair
    #     name = request_data['name'] #assigning it to name
    #     response = f'Hi {name}! this is Python' #re-assigning response with the name we got from the user
    #     return " " #to avoid a type error 
    # else:
    #     return jsonify({'name' : response}) #sending data back to your frontend app

@app.route('/signup',methods = ['GET','POST'])
def SignUpRoute():
    global response

    if(request.method == 'POST'):
        request_data = request.data
        request_data = json.loads(request_data.decode('utf-8'))
        username = request_data["username"]
        password = request_data["password"]
        gender = request_data["gender"]
        email = request_data["email"]
        name = request_data["name"]
        address = request_data["address"]
        try:
            signup = Signup(name,address,gender,email,username,password,acc_type="Member")
            response = jsonify({"error":"None"})
            print(response.data)
            signup.Print_Account_Details()
            return response
        except Exception as e:
            response = jsonify({"error":str(e)})
            return response
    else:

        return response


if __name__ == "__main__":
    app.run(debug=True,host="0.0.0.0")