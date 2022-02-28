from flask_app.config.mysqlconnection import MySQLConnection, connectToMySQL
from flask import flash
from flask_app import app
import re, math
from datetime import datetime
from flask_app.models import user

class Message:
    db = 'users_and_messages'
    def __init__(self, data): 
        self.id = data['id']
        self.content = data['content']
        self.sender_id = data['sender_id']
        self.sender = data['sender']#should change to sender (it will have all the info)
        self.recipient_id = data['recipient_id']
        self.recipient = data['recipient']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

#notice that timestamp is an instance method, not a class
    def timestamp(self):
        now = datetime.now()
        delta = now - self.created_at
        print(delta.days)
        print(delta.total_seconds())
        if delta.days > 0:
            return f"{delta.days} days ago"
        elif (math.floor(delta.total_seconds() / 60)) >= 60:
            return f"{math.floor(math.floor(delta.total_seconds() / 60)/60)} hours ago"
        elif delta.total_seconds() >= 60:
            return f"{math.floor(delta.total_seconds() / 60)} minutes ago"
        else:
            return f"{math.floor(delta.total_seconds())} seconds ago"

    #CREATE
    @classmethod
    def create_message(cls, data):
        query='''
        INSERT INTO messages (content, sender_id, recipient_id)
        VALUES (%(content)s,%(sender_id)s,%(recipient_id)s);''' # will need hidden input with recipient id when sending message
        return connectToMySQL(cls.db).query_db(query,data)

    #READ
    @classmethod
    def get_all_messages(cls, id):
        data= {'id' : id}
        query='''SELECT users.first_name as recipient, users2.first_name as sender, messages.*
        FROM messages
        LEFT JOIN users ON users.id = messages.recipient_id
        LEFT JOIN users as users2 ON users2.id = messages.sender_id 
        WHERE users.id = %(id)s;'''  

        result= connectToMySQL(cls.db).query_db(query, data)
        if result:
            messages=[]
            for m in result:
                one_message = cls(m)
                messages.append(one_message)
            return messages
        return result
            # The below is not need because of how query is worded, ex users."first_names as sender"
        #     instance_of_recipient = {
        #         "id": m['users.id'],  #also just be users.id?
        #         "first_name": m['first_name'],
        #         "last_name": m['last_name'],
        #         "email" : m['email'],
        #         "password" : m['password'],
        #         "created_at": m['users.created_at'],
        #         "updated_at": m['users.updated_at'],
        #     }
        #     recipient = user.User(instance_of_recipient)
            
        #     one_message.recipient = recipient #set to recipient object
        #     one_message.sender =sender 
            #Instanse of user (recipient) and append message to them, set = to message.sender

    @classmethod
    def delete_message(cls, id):
        data ={ "id" : id}
        query= '''
        DELETE FROM messages
        WHERE id = %(id)s
        ;'''
        print('made ','it')
        return connectToMySQL(cls.db).query_db(query, data)