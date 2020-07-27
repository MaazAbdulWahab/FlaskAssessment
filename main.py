from flask_sqlalchemy import SQLAlchemy
from flask import Flask, jsonify, request
from flask_restful import Resource, Api
app=Flask(__name__)
db=SQLAlchemy(app)
api=Api(app)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///onsite.db'


class user(db.Model):


    name=db.Column(db.String(30),nullable=False,unique=True, primary_key=True)
    email=db.Column(db.String(50),nullable=False,unique=True)
    password=db.Column(db.String(30),nullable=False,unique=True)

    def __repr__(self):
        return('USER '+str(self.name)+' '+str(self.email)+' '+str(self.password))



class SignIn(Resource):
    def post(self):
        data=request.get_json()
        name=data['name']
        passw=data['password']
        list_of_users=user.query.filter_by(name=name,password=passw).all()
        if(len(list_of_users)==1):
            return jsonify({'status':202,'message':f'Hello {name}'})
        return jsonify({'status':404,'message':'not found'})

api.add_resource(SignIn,'/login')

class SignUp(Resource):
    def post(self):
        data=request.get_json()
        name=data['name']
        email=data['email']
        passw=data['password']
        list_of_users=user.query.filter_by(name=name).all()
        if(len(list_of_users)>0):
            return jsonify({'status':403,'message':'Account with this name already exists'})
        elif(len(list_of_users)==0):
            us=user(name=name,email=email,password=passw)
            db.session.add(us)
            db.session.commit()
            return jsonify({'status':202,'message':f'Hello {name}, email {email}, account has been created'})

api.add_resource(SignUp,'/signup')

if __name__ == '__main__':
    app.run(debug=True,port=8080)