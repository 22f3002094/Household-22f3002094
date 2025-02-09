from flask_restful import Api, Resource ,request
from backend.models import db, ServiceCategory
api = Api()


class serviceCategory(Resource):

    def get(self):
        return "hello"
    def post(self):
        cn =request.json.get("cat_n")
        cp =request.json.get("cat_p")
        check_cat =db.session.query(ServiceCategory).filter_by(name =cn).first()
        if not check_cat:
            cat = ServiceCategory(name=cn,base_price=cp)
            db.session.add(cat)
            db.session.commit()
            return {"message": "Category object is creted"} , 200
        
        else:

            
            return {"message":"categoy already exist"} , 201
        
    def put(self,cat_id):
        cat_change_name =request.json.get("cat_c_n")
        cat_change_price =request.json.get("cat_c_p")
    
        cat= db.session.query(ServiceCategory).filter_by(id = cat_id).first()
        if cat_change_name:
            cat.name = cat_change_name
        elif cat_change_price:
            cat.base_price = cat_change_price
        db.session.commit()
        return {"message":"category details updated"} , 200
    def delete(self):
        return "delete"



api.add_resource(serviceCategory,"/api/servicecategory","/api/servicecategory/<cat_id>")