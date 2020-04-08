#################################################
# import necessary libraries
#################################################
import os
import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy import create_engine, inspect, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import exc  # THIS IMPORT LINE CATCHES ALL ALCHEMY ERRORS
from flask import (  Flask,    render_template,    jsonify,    request,    redirect)
from flask_sqlalchemy import SQLAlchemy
 
app = Flask(__name__)


Bases = declarative_base()
###################################################
## ???? WHAT IS DECLARITIVE BASE VS AUTOMAP BASE ???
###################################################
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

#import build_db_insert_block

###########################################
# INSPECT DB
###########################################
inspector = inspect(engine)
inspector.get_table_names()  
print("view names.",   inspector.get_view_names(schema=None))# give me a list of all views stored in db
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
# stmt = db.session.query(customers).statement

########################################################################################################
#         R  O  U  T  E  S                                                                            ##
########################################################################################################


def insert_data():
    data = [( 888, "xxx", "03-01-2020",  ) , ( 666, "fff", "03-02-2020")  ]
    package = ""
    ct = 1 
    for i in data :
        if (ct < len(data)):
            package = package +str(i)+ ","
        else:
            package = package +str(i)
        ct+=1
   
    pack = f'''INSERT INTO test_a(col1, col2, col3) VALUES {package} ;'''
     ##################################################
    ##// OUR SQL COMMAND ABOVE MEANS BELOW 
    # INSERT INTO 
    # TABLE_NAME_HERE(NAMES_OF COLUMNS RECEIVING DATA, COL NAME,COL NAME) 
    # VALUES {OUR STUCTORED STRING FROM ORIG LIST}
     ###################################################
    print("this is our pack", pack)
    ####################################
    ## BELOW IS  METHOD TO INSERT OUR DATA AS A TRANSACTION 
    ## IF AN EXCEPTION IS RAISED THEN THE TRANSACTION WILL AUTO ROLLBACL
    ## THERE IS NO NEED TO MANUALLY WRITE BEGIN TRANSACTION; END TRANSACTION IN OUR PACK ABOVE
    ## FYI TRANSACTION ARE MUCH FASTER FOR BULK INSERT 
    
    # try:
    #     with engine.begin() as connection:
    #         connection.execute(pack)

    # except exc.SQLAlchemyError as e:
    #     error = str(e.__dict__['orig'])
    #     print( "THE SQL ERROR WAS: ",error)
    #     pass 

##################################################################################
## TRY below to force data type on insert - this reque
# https://docs.sqlalchemy.org/en/13/core/connections.html
# with engine.begin() as connection:
#     r1 = connection.execute(table1.select())
#     connection.execute(table1.insert(), {"col1": 7, "col2": "this is some data"})
# or 
#conn.execute(
#     "INSERT INTO table (id, value) VALUES (?, ?)",
#     (1, "v1"), (2, "v2")
# )

# conn.execute(
#     "INSERT INTO table (id, value) VALUES (?, ?)",
#     1, "v1"
# )
    try:
        with engine.begin() as connection:
            connection.execute(
                "INSERT INTO test_a(col1, col2, col3) VALUES(?,?,?)",
                 data     
            )

    except exc.SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        print( "THE SQL ERROR WAS: ",error)
        pass 
    session.close()
##################################################################################
insert_data()
##################################################################################

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


@app.route("/views")
def view_displayer():
    views = []
    view_names =   inspector.get_view_names(schema=None)
    views.append([view_names])
    return jsonify(views)


@app.route("/view_result/<the_sql>")
def render_this(the_sql):
    list_one =[]
    list_two =[]
    # WE ONLY WANT VALID QUERYS NOT HTML TITLES SELECT A VIEW IS FIRST OPTION IN OUR HTML DROP DOWN LIST
    if the_sql != "Select A View" :

        # print("this is view results your resquest is :", the_sql)
        results = engine.execute(the_sql).fetchall()
        print("these are results from DB", results)
         
        # return render_template("index.html", f_data = results) 

        for i in results :  # TWO STEP PROCESS TO UNPACK AND REBUILD AS A LIST WITHOUT TUPLES OR PARENTHESIS SO JSON WILL BE HAPPY BELOW
            print("results i :", i)
            list_one = []
            for x in i :
                list_one.append(x)
            list_two.append(list_one)
        session.close()
        return jsonify(list_two) ### SEND THIS BACK TO JAVASCRIPT AS A LIST OF LISTS  


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
            # custom_query = eval_split
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
    print("the Custom Query being sent to DB is:", custom_query)
    query_message = "Your Query Input Was:"
    db_results_msg = "Database Query Results Will Appear Below:"
    ####################################################
      ## THIS CATCHES ALL ALCHEMY ERRORS/ try except prevents total app failure
    ####################################################
    from sqlalchemy import exc  # THIS IMPORT LINE CATCHES ALL ALCHEMY ERRORS
    try:
        results =engine.execute(custom_query).fetchall()
        
        #############################################
        ### BELOW WILL GENERATE A DICTIONARY OF OUR QUERY WITH KEYS AND VALUES 
        result_list = []
        result_list.append( [{column:value for column, value in result.items()} for result in results])
        print("this is new results list", result_list)
        # print("this is one line code", [{column:value for column, value in result.items()} for result in results])

        #############################################
        ### BELOW WILL DO THE SAME THING GENERATE A DICTIONARY OF OUR QUERY WITH KEYS AND VALUES   
        # for v in results:
        #     for column, value in v.items():
        #         print('{0}: {1}'.format(column, value))

        #############################################
        ### THIS WILL SIMPLY GIVE US OUR COLUMNS FROM THE QUERY
        columns_list = []
        h = 0
        for v in results:
            if (h == 0 ):
                print("these are the columns from the query")
                for column in v.items():
                    print('{0[0]}'.format(column))
                    columns_list.append( ('{0[0]}'.format(column)))
            h +=1
        print("this is our new columns list", columns_list)
        #########################################################

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
                                query_msg= query_message, db_results_msg =db_results_msg, columns = columns_list)

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

