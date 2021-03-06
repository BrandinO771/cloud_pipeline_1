#################################################
# import necessary libraries
#################################################
import os
import pandas as pd
import numpy as np
from flask_sqlalchemy import SQLAlchemy 
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy import create_engine, inspect, func
from sqlalchemy.ext.declarative import declarative_base
from flask import (  Flask,    render_template,    jsonify,    request,    redirect)
Bases = declarative_base()
###################################################
## ???? WHAT IS DECLARITIVE BASE VS AUTOMAP BASE ???
###################################################
app = Flask(__name__)
###################################################
# CONFIG :
###################################################
# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', '') or "sqlite:///data/furniture_store_db.sqlite"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data/acme_furniture.sqlite"
engine = create_engine("sqlite:///data/acme_furniture.sqlite", echo=False)
conn = engine.connect()
db = SQLAlchemy(app)
Base = automap_base()# reflect an existing database into a new model
print("THis is the base", Base )
Base.prepare(db.engine, reflect=True)# reflect the tables

###########################################
# INSPECT DB
###########################################
inspector = inspect(engine)
inspector.get_table_names()
print( "inspector.get_table_names()", inspector.get_table_names())
columns = inspector.get_columns("customer_list")
# print("these are the columns", columns)
for c in columns:
    print(c['name'], c["type"])

columns = inspector.get_columns("orders_list")
# print("these are the columns", columns)
for c in columns:
    print(c['name'], c["type"])

# # Print all of the classes mapped to the Base
# v = Base.classes.keys()
# print( "THESE ARE THE KEYS", Base.classes.keys())
# print("this is class 0", v[0])
# our_var_for_table = Base.classes.THE_REAL_TABLE_NAME
customers = Base.classes.customer_list
# order =  Base.classes.orders_list
session = Session(engine)                 
# order =  Base.classes.orders

########################################################################################################
#         R  O  U  T  E  S                                                                            ##
########################################################################################################

@app.route("/")
def index():
    """Return the homepage."""
    return render_template("index.html")


######################################################
#            JOIN QUERY HARDCODED ROUTE             ##
######################################################
@app.route("/x")
def home():
    print("The home route is being called")
    results =engine.execute('SELECT * FROM customer_list, orders_list WHERE customer_list.Customer_id = orders_list.Customer_id').fetchall() 
    print("this data from database", results)
    session.close()
    return render_template("index.html", fill_data = results)
    # return jsonify(results)


#####################################################
#            CUSTOM QUERY METHOD                   ##
#####################################################
@app.route('/query_admin/', methods=['GET', 'POST']  )
def custom_query_admin():
    print(">>>>>>--The request.method is:", request.method )
    if request.method =="GET":
        print(">>>>>>--The request form get:", request.form.get)
        print(">>>>>>--The request form get:", request.form.get('submit'))
        print(">>>>>>--The request form get GET query_ab:", request.form.get('query_ab'))
        print(">>>>>>--The request form get file:", request.form.get('name'))
        print(">>>>>>--The request form get GET:", request.form.get('GET'))
        print(">>>>>>--The request form get file:", request.form.get('file'))

    if request.method =="POST":
        print(">>>>>>--The request form get:", request.form.get)
        print(">>>>>>--The request form get submit:", request.form.get('submit'))
        print(">>>>>>--The request form get name:", request.form.get('name'))
        print(">>>>>>--The request form get file:", request.form.get('file'))
        print(">>>>>>--The request form get GET POST:", request.form.get('POST'))
        ### IMPORTANT --> THE POST WILL GET THE TEXT USER INPUTS IF YOU CALL GET THE 
        ### CUSTOM NAME YOU GAVE THE "NAME" IN THIS LINE BELOW  "query_ab"
        ### <input type="text" id="query_a" name="query_ab"><br>
        print(">>>>>>--The request form get GET query_ab:", request.form.get('query_ab'))
        custom_query = request.form.get('query_ab')
        print(">>>>>>--The request form  :", request.form )
        print(">>>>>>--The request   :", request )
        ##################################################################
        ### CHECK FOR RESTRICTED WORDS --- KEEP IT READ ONLY FOR NOW ###
        #################################################################
        eval_query =""
        eval_query =custom_query
        query_harmful = False 

        if eval_query != "":
            eval_split = eval_query.split(" ")
           
            print("THIS IS THE QUERY SPLIT", eval_split)
            string_list = []
            string_list = eval_split
            for t in range(len(string_list)):
                string_list[t] = string_list[t].lower()

            restricted_words =["create", "drop", "dog", "transaction","delete", "trigger", "rollback"]     

            for i in restricted_words:
                if i in string_list:
                    print("ERROR your not supposed to type this word", i)
                    query_harmful = True

        if query_harmful:
            print("Your query is not harmful to our Database, HOW DARE YOU !! HOW DO YOU SLEEP AT NIGHT!! ")

    ####################################################
    print("The custom query route is being called")
    query_message = "Your Query Input Was:"
    db_results_msg = "Database Query Results Will Appear Below:"
    ####################################################
      ## THIS CATCHES ALL ALCHEMY ERRORS/ try except prevents total app failure
    ####################################################
    from sqlalchemy import exc  # THIS IMPORT LINE CATCHES ALL ALCHEMY ERRORS
    try:
        results =engine.execute(custom_query).fetchall()
        # results =engine.execute("""SELECT * FROM orders_list""").fetchall()
        # print (" results.keys ",  results.keys())
        # BELOW WE ARE JUST PULLING THE WHOLE DATABASE INTO A DATAFRAME FROM THERE YOU CAN SORT SELECT THE DATAFRAME 
        #########################################################
        # stmt = db.session.query(customers).statement
        # df = pd.read_sql_query(stmt, db.session.bind)
        # print("this is statement from query", stmt)
        # print("(list(df.columns)[1:]) ",(list(df.columns)[1:]) )
        #########################################################

        print("this data from database", results)
        session.close()
        return render_template("index.html", fill_data = results, user_query = custom_query, 
                                query_msg= query_message, db_results_msg =db_results_msg)

    except exc.SQLAlchemyError:
        pass 
        results = ("There was an error in your query, try again")
        return render_template("index.html", error_query = results, user_query = custom_query,query_msg= query_message)
    # return jsonify(results)

#################################################################################################################
#          END CUSTOM QUERY METHOD :     ########################################################################
#################################################################################################################




#################################################################################################################
if __name__ == "__main__":     ### DO NOT DELETE ###
    app.run()
#################################################################################################################
#
#
#
#
#
#
#
#





######################################################
    # query code samples below
######################################################

    # sel =   [
    #         econ_1_.country_name_a,
    #         query_var
    #         ]
    # #   TAKE THE SELECTION FROM WEBPAGE QUERY , GRAB THE COUNTRY NAMES AND THE SELECTION VALUES GRAP TOP 5 THEN BOTTOM 5 
    # if (sort_method == 2) :
    # results = db.session.query(*sel).filter(query_var>0).order_by(sel[1].desc()).limit(10).all()
    # results = db.session.query(customers.First_Name).all()
    # results = db.session.query(order.Item_Name).all()
    # results =engine.execute('SELECT * FROM orders_list LIMIT 5').fetchall()
    # results =engine.execute('SELECT * FROM customer_list LIMIT 5').fetchall()
        # results = db.session.query(customers.First_Name).all()
    # results = db.session.query(customers).all()
    # results = session.query(orders_list.Item_Name).all()
    # return render_template("index.html")
    # fill_data = jsonify(results)
        # fill_data = results

##############################################
####### TYPE CUSTOM QUERY INTO SEARCH BAR
# @app.route("/query/<querys>")
# def custom_query(querys):  
#     custom_query = querys
#     print("The custom query route is being called")
#     ####################################################
#     # THIS IS QUICKEST WAY TO RETURN CUSTOM QUERY WITHOUT COLUMN NAMES
#     # PROBABLY HAVE TO USE PANDAS DATAFRAME TO GET COLUMN NAMES 
#     ####################################################
#     results =engine.execute(custom_query).fetchall()
#     print("this data from database", results)
#     session.close()
#     return render_template("index.html", fill_data = results)
#     # return jsonify(results)


############################################################
# PET PALS CODE BELOW 
############################################################
# # Query the database and send the jsonified results
# @app.route("/send", methods=["GET", "POST"])
# def send():
#     if request.method == "POST":
#         name = request.form["petName"]
#         lat = request.form["petLat"]
#         lon = request.form["petLon"]

#         pet = Pet(name=name, lat=lat, lon=lon)
#         db.session.add(pet)
#         db.session.commit()
#         return redirect("/", code=302)

#     return render_template("form.html")


# @app.route("/api/pals")  
# def pals():
#     results = db.session.query(Pet.name, Pet.lat, Pet.lon).all()

#     hover_text = [result[0] for result in results]
#     lat = [result[1] for result in results]
#     lon = [result[2] for result in results]

#     pet_data = [{
#         "type": "scattergeo",
#         "locationmode": "USA-states",
#         "lat": lat,
#         "lon": lon,
#         "text": hover_text,
#         "hoverinfo": "text",
#         "marker": {
#             "size": 50,
#             "line": {
#                 "color": "rgb(8,8,8)",
#                 "width": 1
#             },
#         }
#     }]

#     return jsonify(pet_data)

