import findRecipes
import os
import re

import webbrowser
import pandas as pd
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

from flask import Flask, jsonify, render_template, redirect,  url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask import send_from_directory


import numpy as np
import matplotlib.pyplot as plt

import tensorflow as tf


app = Flask(__name__)


sess = tf.InteractiveSession()
sess.close()
#==================================================================================================
#        THIS IS THE LOCATION OF OUR IMAGES 
#==================================================================================================

UPLOAD_FOLDER = 'images'
# ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

final_list = [] 
# 3. Define what to do when a user hits the index route
@app.route("/")
def home():
    print("Server received request for 'Home' page...")
    # return "Welcome to my 'Home' page!"
    return render_template("index.html")

#==================================================================================================
#                  - EXTERNAL API CAL - 
#==================================================================================================
@app.route("/recipes/<ingredientlist>")
def recipe_search(ingredientlist):
    # Call API
    recipe_data = findRecipes.find_recipes(ingredientlist)
    # Redirect back to home page
    print('this is the recipe_data from api call', recipe_data)
    return jsonify(recipe_data)


@app.route("/model/<image_file_name>")
def eval_image(image_file_name):
    #==================================================================================================
    #                  - SET MODEL VARIABLES - 
    #==================================================================================================
    # evaluated_image_source = '/uploads/detect_result2.jpg' # THIS FOR TESTING SETTING EXACT IMAGE
    sess = tf.InteractiveSession()
    sess.run(tf.global_variables_initializer())

    truncate_file_name = image_file_name.split('.')
    img_name = truncate_file_name[0]
    evaluated_image_source = f'/uploads/{img_name}_detect_result.jpg'

    orig_image=f'/uploads/{image_file_name}'
    input_image=f'images/{image_file_name}'

    print('>>>>>>>>>>>-----The evaluated image route for flask is  ', evaluated_image_source )
    print('>>>>>>>>>>>-----The Path to |  orig_image | is',  orig_image)
    print('>>>>>>>>>>>-----The Path to | input_image | is', input_image)
    print('>>>>>>>>>>>----->HELLO I am eval_image funciton the image name is :', image_file_name)
    #==================================================================================================
    #            - RUN MODEL -           - RUN MODEL-
    #==================================================================================================
    from imageai.Detection.Custom import CustomObjectDetection

    detector = CustomObjectDetection()
    detector.setModelTypeAsYOLOv3()
    detector.setModelPath("model/pat_yolo2.h5")
    detector.setJsonPath("json/detection_config.json")
    detector.loadModel()

    final_list = []

    # ########### MODEL IMAGE INPUT / OUTPUT :
    detections = detector.detectObjectsFromImage(
        input_image= input_image, output_image_path=f'images/{img_name}_detect_result.jpg', minimum_percentage_probability=65)

    # ########## MODEL OUTPUT LISTS: PROBABILTY AND NAMES OF ITEMS DETECTED:
    for detection in detections:
        print(detection["name"], " : ", detection["percentage_probability"],
            " : ", detection["box_points"])
    #     final_list = [ detection["name"], detection["percentage_probability"], detection["box_points"] ]
    
    for d in detections:
        # final_list.append( (d["name"], d["percentage_probability"])  )
        final_list.append( d["name"] )

    print("----------->The final List from  model is", final_list)
    print("----------->The final List is object type", type(final_list))

    sess.close()
    #==================================================================================================
    #   TAKE MODEL DETECTION LIST:   CLEANING    # REMOVE DUPLICATES-- MAKE A FINAL LIST OF UNIQUES 
    #==================================================================================================
   #===== THE LINE BELOW IS FOR TESTING - USE LIST BELOW AND COMMENT OUT MODEL CODE ABOVE 
    # final_list = ['hamburger', 'buns', 'cheese', 'onion', 'lettuce', 'tomato'] # TEST LIST
    # print("----------->The final List from testing ", final_list)
    # print("----------->The final List from testing is object type", type(final_list))
    list_prepped =[]
    for words in final_list :
        clean_words = words.replace("_", " ")
        list_prepped.append(clean_words)

    print("the cleaned list without underscores is", list_prepped)

    final_ingres = []
    for i in list_prepped:
        print('this is the final dec List', i)
        if i not in final_ingres :
            final_ingres.append(i)

        # if ( float(i[1]) > 80 ):
        #     final_ingres.append(i[0])
        #     print(i[0])
    print('THIS DETECTION LIST NO DUPES',final_ingres)   
    #==================================================================================================
    #    CONVERST FINAL LIST FROM MODEL TO A STRING TO POPULATE HIDDEN FEILD IN INDEX.HTML FOR D3 TO FIND
    #==================================================================================================
    transit_list =''
    for i in final_ingres:
        transit_list+=i+','
    #==================================================================================================
    #    GET RID OF THE LAST COMMA IN THE STRING 
    #==================================================================================================
    length_of_string = len(transit_list)
    final_transit_list =''
    final_transit_list = transit_list[:(length_of_string-1)]
  
    print('<<<<<<---THE TRANSIT LIST IS--->>>>>' , transit_list)
    print('<<<<<<---THE TRANSIT LIST IS--->>>>>' , final_transit_list)
    print("----------->The final_trainsit List is object type", type(final_transit_list))
   
    user_noticez ='BELOW: Your Original is Above the Evaluated Image'
    notice = 'We found these food items in your picture.'
    # api_trigger= 'run_api'
    # value_trigger =  api_trigger,
    #==================================================================================================
    #    PUSH ALL THIS INTO THE HTML.INDEX , IMAGES AND THEN LIST ITEMS FOR JAVA D3 TO SNIFF OUT  
    #==================================================================================================

    return render_template('index.html', 
                            image_sourceB = orig_image, 
                            image_sourceA =evaluated_image_source, 
                            photoIn = 'Your Original Image:',
                            photoOut = 'Your Evaluated Image :',
                            # yourImageComplete = "Your Image Is Complete",
                            we_found = notice, 
                            user_notice = user_noticez,
                            detected_list = final_transit_list
                            )




# CALL IMAGE BY FILE NAME TO RENDER IN WEBPAGE 
# 'WORKS BELOW JUST TYPE IN /show/robot1.jpg'  
# '---and the image will appear' 

#===================================================================================
# METHODS BELOW FOR LOADING IMAGES - RECEIVING FORM POSTS FROM INDEX.HTML
#===================================================================================

@app.route('/show/<filename>')
def uploaded_file(filename):
    print('Hello I am the --UPLOADED_FILE FUNCTION-- : this is the file name' , filename)
    print('from uploaded file the file name is', filename)
  
    user_notice = ''
    text = "Your Image is Being Evaluated"
    user_notice = text
    # eval_image(filename)
    return render_template('index.html', filename=filename, user_notice = text )

# DIRECTLY OPEN IMAGE PAGE BY ITSELF - MAY WORK IN TANDOM WITH  UPLOADED FILE FUNC ABOVE
@app.route('/uploads/<filename>')
def send_file(filename):
 
    print('---------------------------------------')
    print('THE send_file Funciton is being called>>>>>>>>!!' )
    print('from send file the file name is', filename)
    print('---------------------------------------')
    uploaded_file(filename)
    return send_from_directory(UPLOAD_FOLDER, filename)


@app.route('/', methods=['GET', 'POST']   )
def reset_page():
    print('-----------the reset function is callede in python')
    # return redirect('/')
    return render_template("index.html")

@app.route('/load_image/', methods=['GET', 'POST']   )
def test_submit():
    print(">>>>>>--The request.method is:", request.method )
    if request.method =="GET":
        print(">>>>>>--The request form get:", request.form.get)
        print(">>>>>>--The request form get file:", request.form.get('name'))
        print(">>>>>>--The request form get GET:", request.form.get('GET'))
    if request.method =="POST":
        print(">>>>>>--The request form get:", request.form.get)
        ### below this gives us the name of the image file 
        print(">>>>>>--The request form get file:", request.form.get('file'))
        image_name =  request.form.get('file')
        print(">>>>>>--The request form get GET:", request.form.get('POST'))
        #CALL FUNCTION ABOVE
        uploaded_file(request.form.get('file'))
        # @app.route = ('/show/'+image_name)

    print(">>>>>>--The request form  :", request.form )
    print(">>>>>>--The request   :", request )
    # return redirect('/show/'+image_name)
    # return render_template('index.html')  
    return redirect('/model/'+image_name)



@app.route("/about")
def about():
    print("Server received request for 'About' page...")
    return "Welcome to my 'About' page!"
    # return    <img  src="img_chania.jpg" alt="Flowers in Chania">



if __name__ == "__main__":
    app.run(debug=True)

















# ///////////////////////////////////////////////////////////////////////////////////////////////////
# ///////////////////////////////////////////////////////////////////////////////////////////////////
# ///////////////////////////////////////////////////////////////////////////////////////////////////




# //////////////////////////////////////////////////////////////////////
# ///////BELOW WORKS TO DISPLAY AN IMAGE FROM OUR IMAGE FOLDER/////
# //////////////////////////////////////////////////////////////////////
# @app.route('/uploads/')
# def uploaded_file():
#     print('THE uploaded_file is being called>>>>>>>>!!' )
#     print('---------------------------------------')
#     image = (send_from_directory(app.config['UPLOAD_FOLDER'],'robot1.jpg'))
#     print('the image is' ,  image)
#     return image



# @app.route('/show/?file=robot1.jpg')
# def test_file(filename):
#     print('this is the file name' , filename)
#     # name = filename.split("=")
#     # print("this is the name split", name)
#     # filename = 'http://127.0.0.1:5000/uploads/' + filename
#     # filename =  name
#     # print('from uploaded file the file name is', filename)
#     # return render_template('index.html', filename=filename)
#     return






#/////   FORCE OPEN ANY WEBSITE //////////////
# @app.route('/show/?myFile=<name>')
# webbrowser.open_new(url)
# url = 'http://127.0.0.1:5000/'
# webbrowser.open(url, new=0, autoraise=True)
# url = 'http://127.0.0.1:5000/show/chef1.jpg' 
# webbrowser.open(url, new=0, autoraise=True)
#/////   FORCE OPEN ANY WEBSITE //////////////



# @app.route('/show/<filename>')
# def uploaded_file(filename):
#     filename = 'http://127.0.0.1:5000/uploads/' + filename
#     return render_template('template.html', filename=filename)

# @app.route('/uploads/<filename>')
# def send_file(filename):
#     return send_from_directory(UPLOAD_FOLDER, filename)

# <!doctype html>
# <title>Hello from Flask</title>
# {% if filename %}
#   <h1>some text <img src="{{ url_for('send_file', filename=filename) }}">more text!</h1>
# {% else %}
#   <h1>no image for whatever reason</h1>
# {% endif %}

# @app.route('/img/<filename>') 




# def show(id):
#     photo = Photo.load(id)
#     if photo is None:
#         abort(404)
#     url = photos.url(photo.filename)
#     return render_template('show.html', url=url, photo=photo)


# Open URL in a new tab, if a browser window is already open.
# webbrowser.open_new_tab(url + 'doc/')
# @app.route('/show/<filename>')
# def uploaded_file(filename):
#     print('this is the file name' , filename)


    # return render_template('index.html', filename=filename)