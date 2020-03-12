

notes = '''
========================================
|    DEV NOTES : BRANDON STEINKE       | 
========================================

    
<><><><><><>----SUMMARY----<><><><><><><

THIS PYTHON SCRIPT  CAN GENERATE : 
	* RANDOM CUSTOMERS LIST
	* RANDOM ORDERS LIST (PULLING CUSTOMER IDS FROM CUSTOMER CSV)

	ITS CONTROLLED VIA LOOP STATES: 
                   *  STATES:  0-9 Generate Customer info,
	 * STATES:  10+ Generate Order Info

-========================================================
>>>>>>>>>!!!!-CAREFUL WHICH STATES YOU RUN---!!!!<<<<<<<<<
========================================================== 
AS MAY OVERWRITE EXISTING CUSTOMER OR ORDER FILES 
I THINK IT IS CURRENTLY HARDCODED TO RUN A ORDERS LIST WITH OUT SAVING
 
STATE 12 REALLY DECIDES IF A CSV WILL BE GENERATED FOR ORDERS LIST OR NOT 
IF IT IS CODED FOR STATE 15 CSV WILL GENERATE AN OVERWRITE
 (WILL DEVELOP CONDITION TO READ EXISTING ORDERS CSV AND ITERATE TO NEW VERSION + EXISTING)  
IF STATE 100 ENDS LOOP

-------------------------------------------------------------------------------------
DAILY PRODUCTION NOTES: 
-------------------------------------------------------------------------------------
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