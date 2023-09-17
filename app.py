from flask import Flask, request
from flask_restful import Resource, Api,marshal_with_field,fields,marshal_with
from flask_sqlalchemy import SQLAlchemy

db=SQLAlchemy()
app = Flask(__name__)
api= Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:babs8562AAA@db.znfmdkenxszmnlmefzxw.supabase.co:5432/postgres'
db.init_app(app)

class Task(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, nullable =False)
    def __repr__(self):
        return self.name

with app.app_context():
    db.create_all()
    
# fakeDatabase={
#     1:{'name':'clean car'},
#     2:{'name':'write blog'},
#     3:{'name':'start stream'},
# }

taskFields = {
    'id':fields.Integer,
    'name':fields.String,
}

class Items(Resource):
    @marshal_with(taskFields)
    def get(self):
        tasks=Task.query.all()
        return tasks
    
    @marshal_with(taskFields)
    def post(self):
        data = request.json
        task =Task(name=data['name'])
        db.session.add(task)
        db.session.commit() 
        tasks=Task.query.all()       
        # itemId = len(fakeDatabase.keys())+1
        # fakeDatabase[itemId] = {'name':data['name']}
        return tasks
    


class Item(Resource):
    @marshal_with(taskFields)
    def get(self,pk):
        task =Task.query.filter_by(id=pk).first()
        return task
    
    @marshal_with(taskFields)
    def put(self,pk):
        data = request.json
        task =Task.query.filter_by(id=pk).first()
        task.name= data['name']
        db.session.commit()
        return task
    
    @marshal_with(taskFields)   
    def delete(self,pk):
        task =Task.query.filter_by(id=pk).first()
        db.session.delete(task)
        db.session.commit()
        tasks=Task.query.all()
        return tasks
    
api.add_resource(Items, '/')
api.add_resource(Item, '/<int:pk>')

if __name__=='__main__':
    app.run(debug=True)