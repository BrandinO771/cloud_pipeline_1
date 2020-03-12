
#########################################################################################
#              IMPORTS                                                                  #
#########################################################################################
import random
import numpy
import os
import csv

#########################################################################################
#              NOTES                                                                    #
#########################################################################################
notes = '''
========================================
|    DEV NOTES : BRANDON STEINKE       | 
========================================    
    3/8/20 - created random list of users and citys 200 lines of code
    3/9/20 - 1. take random user list, and city list with state and hardcode here as an official list 
             2. create algorithm to randomly create user orders 
             3. generate CSV for users, items, and sales
             4. use those initial csv's to populate database tables
             5. later inject dirty data population into future orders for cleaning procedures
             6. Generate 'Order Status Table' -  just with ids, order_dates, ship_status, return_status, status, comments
             7. look at mosh video for how he does 'Sales Table and promotions' 
    3/10/20 - 
            YESTERDAY COMPLETED - #2 
        1. TODAY - attempt #1 , #3,  #4 
                        A-> take 10 existing customers and inject into CSV
                            -rename customers_female to be customer_master
                                 *in addition to: fist&last name, include: birth year and gender ,customer ID 
                                 *then just zip with address, state, zip, phone numbers 
                                 *push to csv 
                        B-> from there generate orders table - pulling in those clients by client id 
                            - pull from list curr in memory - not all customers will generate orders -
                                - maybe some customers signed up but did not purchase anything 
                            - this will serve as first orders and client tables for db
                        C-> going forward - this algorithm will open client csv or db , pull all in, then random decide
                            if existing or newly generated client (combonation not in exisitng list) will place orders
                            - additionally will perhaps update the order status for previous orders placed
        END OF DAY : Completed A and B, just need to break item_name and Item_code into separate columns, 
                        Also just have basic Item_type, sofa, chair,stool
    3/11/20:
        .1 Follow up on yesterdays items:
                A. in Orders Report break item_name and Item_code into separate columns,
                B. Also just have basic Item_type, sofa, chair,stool Also just have basic Item_type, sofa, chair,stool
                C. Add Order Date to each order make within last 30 days 
        1 hour later - A,B,C Done 
        END OF DAY - I have created a database in SQLITE and have saved basic querys 
        I came back to this file to polish the order_date to have 2 characters for dd mm so the date will sort correctly in SQL
    3/12/20: 
        A. CLEAN UP SCRIPT BY DELETING ALL PRINTS ETC ..
        B. SAVE AS VERSION 4 
        C. PUSH TO REPO - WITH CSV AND DB
'''
#########################################################################################
#              VARIABLES                                                                #
#########################################################################################
customer_master_list =[]
customers_female = []
customers_male = []
customer_last_name = []
city_name = []
phone_nums =[]
city_dump=[]
address_list = []
address_build =[]
customer_address_list =[]
customer_info_list =[]

poss_male_name      = ["Boo","Jet","Kay","Zeek","Zed","Frank","Ted","Herb","Kale","Tim","Trip","Leaf","Garamond"]
poss_female_name    = ["Fay","Alaina","Sabrina","Sasha","Shanna","Jen","Wendy","Alma","Nana","MoonBeam","Unika","Gertrude"]	
poss_last_name_a    = ["Stein","Rick",	"Pole",	"Free",	"Silver","Cole","Apple","Wacker","Von",	"Wolf", "Flapper"]			
poss_last_name_b    = ["Man","Tree","Bottom","Ton","Blocker","Berg","Port","Ton","Moon","'ErTon", "Smith" ]			
poss_last_name_comp = ["DoLittle","Pinkerton","McGillicuddy","McPeepers","McCoy","UnderHill","Scott","McFadden","Zanderman"]				
poss_city_name_a    = ["Nowhere","Little","Green","Gold","Sleepy","Dreamy","Pleasant","Pony","Hopper","Candy","Copper","Steamy","Settlers", "Old", "Prospecter", "Lost"] 
poss_city_name_B    = ["Ville","Ton","Rock","Hollow","River","Stream","Trails","Mine","Creek","Lake","Hills","Meadows","Colony", "Springs", "Mills", "Pond" ]
street_names        = [	"School","Wondering","Star Light","Kings","Ocean View","Hollow","Beverly","Elm","Gopher","Fox","Bakers","Mull Berry","Maple","First","Main","Oak","Cedar","Washington","Everett"]
street_extra        = [ "Ave",	"Street","Way",	"Court","Parkway","Blvd",	"Center",	"Road"]											

couch_type  =   ["love",	"long",	"short", "sectional", "sleeper"]	
item_style  =   ["Classic",	"Rustic",	"Modern",	"Urban",	"Designer"]
seating_matrl=  ["leather",	"canvas",	"suede",	"microfiber ",	"vinyl"]
chair_type  =	["desk",	"table",	"single_armless",	"captain",	"sofa", "recliner"]
chair_frame	=   ["steel",	"wood",	 "composite",	"aluminum"]	
item_color  =   ["blue", "red", "burgundy",	"black","brown", "tan",	"gray",	"lavendar",	"green", "black","white"]
couch_names =   [ ["Couchy_McCoucherton","cch_1"],["Couchy_McCouchster","cch_2"], ["Cozie_Coucher","cch_3"],["Family_Times","cch_4"], ["Den_Master","cch_5"], ["Lovers","cch_6"],["Dealers_Lounge","cch_7"]  ]
chair_names =   [ ["The_QuarterBack", "cha_1"], ["The_AnchorMan","cha_2"],  ["The_Ambassador","cha_3"],  ["The_Executive","cha_4"],  ["Lazy_Man","cha_5"], ["Regal_Beagle","cha_6"]   ]
stool_names =   [ ["Stool_Pigeon","stl_1"],	["Last_Call","stl_2"],	["Poets_Perch","stl_3"],	["Booty_Scooty","stl_4"],	["Tooshy_Zone","stl_5"] ]
stool_type  =   ['tall_backless', 'tall_low_back', 'tall_low_back_arms', 'counter_backlesss', 'counter_low_back', 'counter_low_back_arms']
item_envnmt =   [ "home_furnishing", "patio_furniture", "office_furniture" ]
type_choices =  ["chair", "couch", "stool" ]

state = 10.0  # master script state control, 0-9 Generate Customer info, 10+ Generate Order Info
counter = 0
count = 0

order_state = 0.0  # states for generating orders 
order_id = ""
order_id_list = []
order_master =[]
order_batch = []
customer_orders = []
customer_id_list = []
customer_id =""

item_quantity = 0
item_id =""# is the second element in each item
order_status = ""
promotion_amt = 0.00
store_id = ""
item_price = 0.00
order_ctr = 0
cust_ctr = 0
order_dates =''

print("<<<<<<<======= START CODE =======>>>>>>>")

#########################################################################################
#               MAIN CODE BODY                                                          #
#########################################################################################

while state < 99:
 
    if state == 0 :#| CHOOSE RANDOM FIRST NAME -MALE |
       if counter < 10 :
        word_one =  random.choice(poss_male_name)
        poss_male_name.remove(word_one)
        customers_male.append( [word_one, '', '','', ''])
        counter +=1
       if ( counter >=10 ):
            state = 1
            counter = 0

    if state == 1 : #| CHOOSE RANDOM FIRST NAME -FEMALE |
       if counter < 10 :
        word_one =  random.choice(poss_female_name)
        poss_female_name.remove(word_one)
        customers_female.append([ word_one, '','','', ''])
        counter +=1
       if ( counter >=10 ):
            state = 2
            counter = 0

    if state == 2 : # *|| LAST NAME : DECIDE IF RANDOM COMBO OR COMPLETE NAME TO GENERATE ||*
         choice = random.randint(1,2)
         state = 3

    if state == 3 :  #|| CHOOSE LAST NAMES ||
        if counter < 20 : 

            #CHOOSE COMPLETE LAST NAME 
            if (choice == 1): 
                if ( len(poss_last_name_comp) > 0 ) :
                    word_one =  random.choice(poss_last_name_comp)
                    poss_last_name_comp.remove(word_one)
                    customer_last_name.append(word_one)
                    state = 2
                else:
                    choice = 2

            #CHOOSE LAST NAME RANDOM COMBINE 2 WORDS   
            if (choice == 2):
                if ( len(poss_last_name_a)>0 and len(poss_last_name_b) >0 ) :
                    word_one =  random.choice(poss_last_name_a)
                    poss_last_name_a.remove(word_one)
                    word_two =  random.choice(poss_last_name_b)
                    poss_last_name_b.remove(word_two) 
                    combo_word = word_one + word_two               
                    customer_last_name.append(combo_word)
                    state = 2   
                else:
                    choice = 1

                if (  len(poss_last_name_a) <= 0 and len(poss_last_name_b) <=0 and len(poss_last_name_comp) <= 0 ) :
                    state = 4
            counter +=1

            if ( counter >=20 ):
                    count = 0
                    state = 4
                    
            if ( counter < 20 ): 
                    state = 2   

    ################################################################
    #  COMPILE LAST NAME WITH - FIRST NAMES OF FEMALE AND MALE LISTS
    #################################################################
    if state == 4 :

        if (count < 20  ):
        
                ##############################################
                #             GENERATE CUSTOMER_IDS          #
                ##############################################
                def generate_cust_id ():
                    obja = random.randint( 12345, 98765)
                    objb = str(obja)
                    combo = "C_"+objb
                    if (combo not in customer_id_list):
                        customer_id_list.append(combo)
                    else:
                        generate_cust_id()
                    return (combo)

            
                i = 0
                t = 0
                h = 0
                for i in customer_last_name:

                    if ( count < 10 ):                          # GENERATE FEMALE INFO
                        customers_female[t][1] = i              # ADD LAST NAME TO CUSTOMER LIST INTO SLOT 2
                        customers_female[t][2] = "female"       # ADD GENDER 
                        customers_female[t][3] = random.randint(1940,1995)  # ADD BIRTH YEAR - SLOT 3
                        customers_female[t][4] = generate_cust_id()         # CALL CUSTOMER ID GENERATOR 
                        count +=1 
                        t+=1 
                    
                    if (count >=11 and count < 21):         # GENERATE MALE INFO
                        customers_male[h][1] = i            # ADD GENDER 
                        customers_male[h][2] = "male"       # ADD BIRTH YEAR - SLOT 3
                        customers_male[h][3] = random.randint(1940,1995)     # CALL CUSTOMER ID GENERATOR 
                        customers_male[h][4] = generate_cust_id()

                        h+=1  
                        count +=1 
                    if (count == 10):
                            count +=1

        else :
           state = 5 

    if state == 5:
        print("we made it to state 5!!")
        print("First_Name | Last_Name | Gender | Birth_Year | Cust_Id")
        # for i in customers_female:
        #     print(i)
        # for i in customers_male:
        #     print(i)
        # print(customers_female)
        # print(customers_male)
        # customer_info_list.append(customers_female)
        # customer_info_list.append(customers_male)
        combine_male_female = customers_female + customers_male
        customer_info_list.append(combine_male_female)                     
        print("the combined male femal list is")                 
        for i in customer_info_list:
            print(i)
        counter = 0 
        state = 6 
        # state = 100 # TEST HERE TO BREAK LOOP
        
    ################################################
    #  GENERATE FAKE : ADDRESS
    ################################################

    if state == 6 :

        if counter < 20 :
            ################################################
            #  GENERATE FAKE :  STREET ADDRESS
            ################################################
            st_num  =  random.randint(101,1987)
            st_num_txt = str(st_num)
            word_a  =  random.choice( street_names )
            word_b  =  random.choice ( street_extra)
            combine_street = st_num_txt +" "+ word_a + " " + word_b

            ################################################
            #  GENERATE FAKE :  ZIP
            ################################################
            zip_num = random.randint(31240,98765)

            ################################################
            #  GENERATE FAKE : STATE 
            ################################################
            state_abb = random.choice(['CA','OR','NV','AZ','WA','ID','NM','UT','MT','CO'])

            ################################################
            #  GENERATE FAKE : CITY NAME 
            ################################################
            word_one =  random.choice(poss_city_name_a)
            word_two =  random.choice(poss_city_name_B)
            city_dump.append( word_one)
            city_dump.append( word_two)
            ####################################################
            ## REMOVE CITY WORDS AFTER USED TWICE - REDUCE REDUNTENCY
            if ( city_dump.count(word_one) > 1 ):
                    poss_city_name_a.remove(word_one)

            if ( city_dump.count(word_two) > 1 ):
                    poss_city_name_B.remove(word_two)
            ######################################################        
            combo_city_name = word_one + " " + word_two               
            city_name.append(combo_city_name)
            ########## END CITY NAME #############################

            ################################################
            # GENERATE FAKE PHONE NUMBER 
            ################################################ 
            numbers_b = random.randint(1000, 9999)
            numbers_b_txt = str(numbers_b) 
            numbers_a = random.randint(123, 876)
            numbers_a_txt = str(numbers_a)
            combo_phone_num = numbers_a_txt + "-555-"+ numbers_b_txt
            phone_nums.append(combo_phone_num)

            ################################################
            #ASSEMBLE VARIABLES INTO ONE LIST
            ################################################
            address_build = [
                            combine_street,
                            combo_city_name,
                            state_abb,
                            zip_num,
                            combo_phone_num
                            ]
            ################################################
            #ADD TO CUSTOMER CONTACT LIST 
            ################################################                           
            customer_address_list.append(address_build)

        counter +=1

        if counter >=20:
            counter = 0
            state = 7 

    if state == 7 : # combined 2 lists into master client list - my version of zip

        if counter < 20:                       
            customer_master_list.append( customer_info_list[0][counter] + customer_address_list[counter])
           
        if counter >= 20:
            i = 0
            for i in customer_master_list:
                    print(i)
            state = 8  

        counter +=1


    if state == 8 : # write CLIENTS  to csv  
        print("<<<<< NOW STATE 8 >>>>>>>")
        new_output_file = os.path.join("../csv/new_customer_master_file2.csv")
        with open(new_output_file, "w", newline="") as datafile:
            data_to_be_inserted = csv.writer(datafile)
            data_to_be_inserted.writerow(["First_Name", "Last_Name", "Gender","Birth_Year","Customer_id","Street","City","State", "Zip", "Phone"])
            data_to_be_inserted.writerows(customer_master_list)

        state = 100  # MAKE THIS STATE 10 IF WANT TO CONTINUE TO GENERATE ORDERS


    #######################################################################################
    #                        GENERATE  ORDERS                                             #
    #######################################################################################
    ##############################################
    #             GENERATE ORDER_IDS             #
    ##############################################
    if ( state == 10 ) :

        if order_ctr < 10:
            obja = random.randint( 12345, 98765)
            objb = str(obja)
            combo = "O_"+objb

            if (combo not in order_id_list):
                order_id_list.append(combo)
                order_ctr +=1

        else:
            print("the order ids are:", order_id_list)

            state = 11

    ##############################################
    #             PULL IN  CUSTOMER_IDS          #
    ##############################################
    if state == 11 :
        ct = 0
        new_cust_id_list = []
        client_ids =[]
        b = 0

        # OPEN CSV - PULL IN ALL CLIENT IDS 
        file_to_analyze = os.path.join("../csv/customer_list.csv")
    
        with open(file_to_analyze, newline="", encoding='utf-8') as csvfile :
            temp_csv_data_table = csv.reader(csvfile, delimiter=",")
            next(temp_csv_data_table) # SKIP HEADER LINE
        
            for column in temp_csv_data_table : 
                if ( b < 20  ):
                    client_ids.append(column[4])
                    print(column[4])
                   
                if ( b >= 20  ):
                    break

                b+=1

        state = 11.5


    if state == 11.5 :  #|| TRACKING COUNT FOR HOW MAX ENTRIES TO GENERATE ||

        if ct < 10 :
            word_choice = random.choice(client_ids)
            new_cust_id_list.append(word_choice)
            client_ids.remove(word_choice)
            ct +=1

        if ct >= 10 :
            order_ctr = 0
            state = 12

    #######################################################
    #         GENERATE ITEMS SELECTIONS FOR ORDERS        #
    #######################################################
    # determine if same user wants to purchase many sets or one set 
    # if many sets then we will have several rows for same customer- we can choose that at the bottom and repeat
    # i want 10 customer orders , max 4 sets per customer 

    if state == 12 : # >> DETERMINE IF ORDER PROCES CONITUES OR FINISHES
        if order_ctr >= 10:

            for i in order_master :
                print(i)
            print("the length of the final order list", len(order_master))
            order_state = 100
            # state = 15    # THIS TAKES TO FINAL STATE TO OUTPUT CSV 
            state =  100   # THIS QUITS THE WHOLE LOOP - YOUR DONE! 

        if order_ctr < 10: # ASSIGN: ORDER ID - CUSTOMER ID - THIS TO CHANGE AS CUSTOMER ID WILL BE INTEGRATED ABOVE- 
            customer_id = new_cust_id_list[order_ctr]
            order_id    = order_id_list[order_ctr]
            order_state = 0
            state = 13

     
    #######################################################
    #    PICK:  ITEM  / TYPE  /Seat Mat / Stlye         #
    #######################################################   
    if order_state == 0 and  state == 13: # GENERATE ORDERS 
        
        choice_a = random.choice(type_choices)
        i_mat   = random.choice(seating_matrl)
        i_style = random.choice(item_style)
        order_state = 1

    if order_state == 1:  # || PICK ITEM ||
        if choice_a =="chair":
            i_choice = random.choice(chair_names)
            i_type  = random.choice(chair_type)
            i_cat   = "chair"        
            
        if choice_a == "couch" :
            i_choice = random.choice(couch_names)
            i_type   = random.choice(couch_type)
            i_cat   = "couch"        

        if choice_a == "stool":
            i_choice = random.choice(stool_names)
            i_type   = random.choice(stool_type)
            i_cat   = "stool"    
        
        i_code = i_choice[1] 
        i_name = i_choice[0]
        order_state = 2            

    ##############################################
    #           PICK: QUANTITY / FRAME           #
    ##############################################
    if order_state == 2 :
        color = random.choice( item_color ) 

        if ( choice_a == "chair" or choice_a == "stool" ):
            quant_choices = ["1", "2", "4", "6", "8"]
            i_quant = random.choice(quant_choices)
            i_frame = random.choice(chair_frame)
            order_state = 2.5

        if ( choice_a == "couch" ):
            i_quant = random.randint(1, 2)
            i_frame = "wood"
            order_state = 2.5  

    ##############################################
    #             GENERATE ORDER_DATES           #
    ##############################################
    if order_state == 2.5 :
        numb_a = random.randint(1,29) # day
        numb_a_txt = str(numb_a)
        if ( len(numb_a_txt) == 1 ) : 
            numb_a_txt = "0" + numb_a_txt 
        # numb_b = random.choice( ['1','2'] ) # month
        order_dates = '2020-' + '02' + '-' + numb_a_txt

        if order_dates != "" :
            order_state = 3
        else:
            order_state = 2.5

    ##############################################
    #         APPEND COMPLETE ORDERS TO LIST     #
    ############################################## 
    if order_state == 3:
        order_batch =   [    
                        order_dates,
                        order_id,
                        customer_id,
                        i_code,
                        i_quant,
                        i_name,
                        i_cat,
                        i_type,
                        i_style,
                        i_mat,
                        i_frame
                        ]
        order_master.append(order_batch) 
        customer_orders.append(customer_id) # here we are creating a list to check count of unique customers and quantity of their orders
        order_state = 4

    ##############################################
    #    DETERMINE IF CUSTOMER ORDERS MORE       #
    ##############################################
    if order_state == 4:
        order_choice = random.randint(1,6)

        if order_choice >= 5  :

            if  customer_orders.count(customer_id) <=2 :
                order_state = 0
            else:
                order_state = 5  

        else:
            order_state = 5  


    if order_state == 5: #|| RETURN TO TOP TO GENERATE MORE ORDERS  ||
        order_ctr +=1
        state = 12        


    if state == 15 : # GENERATE ORDERS CSV 
        new_output_file = os.path.join("../csv/orders_list.csv")

        with open( new_output_file, "w", newline="" ) as datafile :
            data_to_be_inserted = csv.writer(datafile)
            data_to_be_inserted.writerow(["Order_Date", "Order_id", "Customer_id", "Item_Code", "Quantity", "Item_Name", "Item_Category", "Type", "Style", "Seating_Material", "Frame" ])
            data_to_be_inserted.writerows(order_master)
        
        print("YOU ORDER REPORT IS READY AT FOLLOWING LOCATION", new_output_file)
        state = 100


#########################################################################################
#########################################################################################
#########################################################################################
#                  END CODE BODY                                                        #
#########################################################################################


