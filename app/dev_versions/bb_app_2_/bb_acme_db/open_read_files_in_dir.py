
import os
import glob
import csv
import time 
state =1


while state < 4 :


    ##############################################
    ## GET FILE NAMES IN DIR
    ##############################################
    if state == 1 :
        target_dir = "text_test/"
        files_in_dir = glob.glob(f'{target_dir}*')
        files_bundle = []
        #can also be written as -----> files_in_dir = glob.glob("test/*")
        for file in files_in_dir :
            ## glob returns path with back slashes instead of // and instead of 1 it returns 2
            ## split return on \\ backslash access the second element the file name
            split_raw_path = (file.split("\\"))
            file_name= (split_raw_path[1])
            # print("this is a file?", file)
            # print("the full path is", file)
            # print("the raw_path", raw_path)    
            # print("this is file_name", file_name)
            try:
                files_bundle.append(file_name)

            except IndexError :

                continue

        print("the file names are", files_bundle)
        state = 2 

    ##############################################
    ## OPEN CSV FILES / BUNDLE DATA   ///>> ADD TO THIS FUNC : CHECK EXISTING BAR CODES IN DB AND REJECT IF THOSE VALUES ALREADY IN DB
    ##############################################

    if state == 2 : #////build in duplicate rejections!!

        data_bundle = [] 
        dupe_check = []

        for items in files_bundle :
            files = target_dir+items
            with open(files, newline="", encoding='utf-8') as csvfile :
                temp_file = csv.reader(csvfile, delimiter=",")
                next(temp_file)
                for column in temp_file:
                    if (column[0] not in dupe_check):
                        dupe_check.append(column[0])
                        # print("dupe_check_is:", dupe_check)
                        data_bundle.append(column)

        # print("this is our bundle list", data_bundle)
        state = 3


    ##############################################
    ## PUSH DATA TO DB
    ##############################################
    if state == 3 :
        # bulk insertions and performance
        # https://docs.sqlalchemy.org/en/13/faq/performance.html
        # https://stackoverflow.com/questions/11769366/why-is-sqlalchemy-insert-with-sqlite-25-times-slower-than-using-sqlite3-directly
        import sqlalchemy
        from sqlalchemy.ext.automap import automap_base
        from sqlalchemy.orm import Session
        from sqlalchemy import Column, Integer, String, Float
        from sqlalchemy import create_engine, inspect, func
        from sqlalchemy.ext.declarative import declarative_base
        from sqlalchemy import exc  # THIS IMPORT LINE CATCHES ALL ALCHEMY ERRORS
        import time
        # import logging
        # logging.basicConfig()
        # logger = logging.getLogger("myapp.sqltime")
        # logger.setLevel(logging.DEBUG)
        data = data_bundle
        engine = create_engine("sqlite:///data/acme_furniture.sqlite", echo=False)
        conn = engine.connect()
        session = Session(engine)  

        def insert_data():
            t0= 0
            t0 = time.time()
            try:
                with engine.begin() as connection:
                    connection.execute(
                        "INSERT INTO test_a(col1, col2, col3) VALUES(?,?,?)",
                        data     
                    )
                print (  len(data), " rows added in ", str(time.time() - t0) )
                ## 501  rows , with 3 columns added in  0.1925373077392578, that is 1500 pieces of data 
                ## this would be pretty slow if you had 100,000 records it would be 38 seconds - so we can explore more 
            except exc.SQLAlchemyError as e:
                error = str(e.__dict__['orig'])
                print( "THE SQL ERROR WAS: ",error)
                pass 
        
            session.close()
         # call func above
        insert_data()
        # get out of parent loop
        state = 4

    ##################################################################################
    #  USING SQLITE3 MODULE BUILT INTO PYTHON TO INSERT INTO DB
    ##################################################################################

    if state == 20 : ##/// this version is slower by .045 almost twice as slow // test without import
        # https://docs.python.org/3.8/library/sqlite3.html
        import sqlite3
        conn = sqlite3.connect( "data/acme_furniture.sqlite")
        c = conn.cursor()
        t0 = time.time() 
        c.executemany("INSERT INTO test_a(col1, col2, col3) VALUES(?,?,?)", data_bundle)
        conn.commit()
        print (  len(data_bundle), " rows added sqlite3: Total time", str(time.time() - t0) )
        state = 100

    ##################################################################################
  
# - with open csv 
# - open gather
# - push to test db 
# - move files to new dir


    # BELOW IS THE ORIGINAL EXAMPLE
    ##################################################################################

    # import sqlite3
    # def test_sqlite3(n=100000, dbname = 'sqlite3.db'):
    #     conn = init_sqlite3(dbname)
    #     c = conn.cursor()
    #     t0 = time.time()
    #     for i in range(n):
    #         row = ('NAME ' + str(i),)
    #         c.execute("INSERT INTO customer (name) VALUES (?)", row)
    #     conn.commit()
    #     print "sqlite3: Total time for " + str(n) + " records " + str(time.time() - t0) + " sec"

 
