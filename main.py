from pprint import pprint
from flask import Flask, jsonify, request,make_response,redirect,send_file
import json
from Catalog import Catalog, Product
from Login import Login
from SignUp import Signup
import os

from account import accountdetails

#declared an empty variable for reassignment
response = ''

#creating the instance of our flask application
app = Flask(__name__)
app.config["IMAGE_UPLOADS"]="images"
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
            img = login.account.img
            ph = login.account.ph
            response = jsonify({"error":"Logged in","account":{"email":email,"username":username,"image":img,"phone_num":ph}})
            return make_response(response,200)
        except Exception as e:
            
            response = jsonify({"error":str(e),"account":'None'})
            return make_response(response,400)
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
        ph = request_data["phone_num"]
        try:
            signup = Signup(name,address,gender,email,username,password,acc_type="Member",phone_num=ph)
            response = jsonify({"error":"None"})
            print(response.data)
            signup.Print_Account_Details()
            return make_response(response,200)
        except Exception as e:
            response = jsonify({"error":str(e)})
            return make_response(response,400)
    else:

        return response

@app.route('/getimages')
def get_image():
    img = request.args.get('img')
    filename = f"images/{img}"
    return send_file(filename, mimetype='image/gif')
    
@app.route('/account',methods=["POST"])
def accountload():
    request_data = request.data
    request_data = json.loads(request_data.decode('utf-8'))
    name = request_data["username"]
    response = jsonify(accountdetails(name)[0])
    return response
@app.route("/images",methods=["GET","POST"])
def upload_file():
    username = request.args.get("username")
    image = request.files['image']
    image.save(os.path.join(app.config["IMAGE_UPLOADS"],image.filename))
    print("saved")    

    return make_response({"hello":"lol"},200)
@app.route('/products/new',methods =['POST'])
def ProductsAdd():
    request_data = request.data
    request_data = json.loads(request_data.decode('utf-8'))
    name = request_data["name"]
    price = request_data["price"]
    amount = request_data["amount"]
    tags = request_data["tags"]
    image = request_data["image"]
    Catalog().Add(Product(name,amount,price,image,tags))
    return make_response(None,200)
        
    
@app.route('/product/search',methods=["GET",'POST'])
def Productsearch():
    if request.method=="POST":
        request_data = request.data
        request_data = json.loads(request_data.decode('utf-8'))

@app.route('/products',methods=["GET"])
def ProductView():
    data = Catalog().Show()
    response = jsonify({"products":data})
    return response

    



if __name__ == "__main__":
    app.run(debug=True,host="0.0.0.0")