from flask_app.config.mysqlconnection import MySQLConnection,connectToMySQL
from flask_app import app
from flask import flash,session
from flask_app.models import user



class Show:
    DB='belt_exam_erd'

    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.network = data['network']
        self.date = data['date']
        self.description = data['description']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id=data['user_id']
        self.creator=None#this for create instance of user

    #READ____MODEL____SQL
    #get show by id
    @classmethod
    def get_show_by_id(cls,id):
        data={'id':id}
        query="""SELECT * FROM shows WHERE id=%(id)s
        ;"""
        result=connectToMySQL(cls.DB).query_db(query,data)
        if result:
            result=cls(result[0])
        return result


    #get all shows from db 
    @classmethod
    def get_all_shows(cls):
        query="""
        SELECT * FROM shows
        JOIN users
        ON shows.user_id=users.id
        ;"""
        result=connectToMySQL(cls.DB).query_db(query)
        print("//////////////////",result)#this will give me list of dictionary which has all users info and their adventurs
        shows_list=[]#create empty list to append all adventures and users info to it
        if not result:
            return result
        for this_show in result:
            new_show=cls(this_show)#create instance of reports and it will ignor user thats why we need to create dictionary for users table info
            user_data={
                'id':this_show['users.id'],
                'first_name':this_show['first_name'],
                'last_name':this_show['last_name'],
                'email':this_show['email'],
                'password':this_show['password'],
                'created_at':this_show['users.created_at'],
                'updated_at':this_show['users.updated_at'],
            }
            new_show.creator=user.User(user_data)#go to user class and pass users data to get instance of user and save it into new_show.creator
            shows_list.append(new_show)
        print(shows_list)
        return shows_list



    #CREATE____MODEL____SQL
    @classmethod
    def create_show(cls,data):
        if not cls.validate_show(data):
            return False
        else:
            query="""
            INSERT INTO shows (title,network,date,description,user_id)
            VALUES (%(title)s,%(network)s,%(date)s,%(description)s,%(user_id)s)
            ;"""
            result=connectToMySQL(cls.DB).query_db(query,data)
            print("############## create query result",result)
            return result


    #UPDATE____MODEL____SQL
    @classmethod
    def update_show_by_id(cls,data):
        if not cls.validate_show(data):
            return False
        query="""
        UPDATE shows SET title=%(title)s,network=%(network)s,date=%(date)s,description=%(description)s
        WHERE id=%(id)s
        ;"""
        result= connectToMySQL(cls.DB).query_db(query,data)
        print("5555555555555555",result)
        return result

    #DELETE____MODEL____SQL
    @classmethod
    def delete_show(cls,id):
        data={ 'id':id}
        query="""
        DELETE FROM shows WHERE id=%(id)s
        ;"""
        return connectToMySQL(cls.DB).query_db(query,data)


    #static method for VALIDATEING shows
    @staticmethod
    def validate_show(data):
        is_valid=True
        if len(data['title']) < 3:
            flash("title must be at least 3 or more characters.")
            is_valid = False
        if len(data['network']) <3:
            flash("Network must at least 3 or more characters")
            is_valid=False
        if len(data['description']) <3:
            flash("description feiled must at least 3 or more characters")
            is_valid=False
        if  data['date']=="":
            flash("You must select a date")
            is_valid=False
        return is_valid