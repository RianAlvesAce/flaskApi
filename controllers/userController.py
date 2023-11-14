from app import app
from flask import request, jsonify, g, send_file
from models import UserModel, ContactModel
from utils import JWT

import os

# Request token JWT
@app.after_request
def after(response):
    path = request.path
    method = request.method

    if path == '/user' and method == 'GET':
        body = request.args.to_dict()

        if 'token' in body:
            decode_token = JWT.decode_token(body.get('token'))

            if not decode_token:
                return jsonify({"status": 406, "message": 'Token expirado'})
            else:
                return jsonify({'status': 202, 'token': body.get('token')})
            
        else: 
            return response
    
    return response

# Register User
@app.route("/user", methods=['POST'])
def userPost():
    data = {'name': request.form['name'], 
            'nick': request.form['nick'],
            'email': request.form['email'],
            'pass': request.form['pass']}

    file = request.files['img']
    newUser = UserModel.User(data, file)
    status = newUser.insert_user()

    if not status:
        return jsonify({'status': 406, 'message': 'E-mail já existente'})

    return jsonify({'status': 200})


# Login User
@app.route("/user", methods=['GET'])
def userGet():
   user = request.args.to_dict()
   res = UserModel.User(user, None).login()
   
   if res['status'] == 202:
       return jsonify(res)
   else: 
       return jsonify(res)

# Pegar usuário
@app.route("/getUser", methods=['GET'])
def getUser():
    contactEmail = request.args.to_dict()
    contact = UserModel.User.get_user(contactEmail.get('email'))

    return jsonify({
        'name': contact.get('name'),
        'nick': contact.get('nick'),
        'userImg': contact.get('userImg'),
        'id': str(contact.get('_id'))
    })


# Criar contato
@app.route("/newContact", methods=['POST'])
def newContact():
    data = request.get_json()
    contactModel = ContactModel.Contact({'userId': data.get('userId'), 
                                         'contactId': data.get('contactId')})
    contactModel.insert_contact()
    
    # UserModel.User.insert_contact(user.get('email'), user.get('id'))

    return jsonify({'status': 202})
   

@app.route('/getImg', methods=['GET'])
def getImg():
    return send_file(path_or_file=request.args.get('src'))