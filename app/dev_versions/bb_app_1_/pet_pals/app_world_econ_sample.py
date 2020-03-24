import os

import pandas as pd
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


#################################################
# Database Setup
#################################################

# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db/bellybutton.sqlite"
# db = SQLAlchemy(app)
# # reflect an existing database into a new model
# Base = automap_base()
# # reflect the tables
# Base.prepare(db.engine, reflect=True)
# # Save references to each table
# Samples_Metadata = Base.classes.sample_metadata
# Samples = Base.classes.samples

# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db/global_db.sqlite"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db/econ_db.sqlite"
# IMAGE_FOLDER = 'static/js/Flags'
# app.config['IMAGE_FOLDER'] = IMAGE_FOLDER 
db = SQLAlchemy(app)

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(db.engine, reflect=True)

# Save references to each table
#Export = Base.classes.export3
econ_1_ = Base.classes.econ





@app.route("/")
def index():
    """Return the homepage."""
    return render_template("index.html")

# ////////////////////////////////////
# BELOW WORKS WITH CSV
# ///////////////////////////////////////
# @app.route("/names")
# def names():
#     """Return a list of sample names."""
#     df = pd.read_csv("db/country_trade.csv")


#     # Use Pandas to perform the sql query
#     # stmt = db.session.query(Samples).statement
#     # df = pd.read_sql_query(stmt, db.session.bind)

#     # Return a list of the column names (sample names)
#     # return jsonify(list(df.columns)[1:])
#     return jsonify(list(df["Country"]))



@app.route("/names")
def names():
    """Return a list of sample names."""

    # Use Pandas to perform the sql query
    #stmt = db.session.query(Export).statement
    stmt = db.session.query(econ_1_).statement

    df = pd.read_sql_query(stmt, db.session.bind)

    # Return a list of the column names (sample names)
    # return jsonify(list(df.columns)[1:])//this was example where samples were the all the column headers
    return jsonify(list(df["country_name_a"]))



@app.route("/metadata/balrank")
def get_balance_rank():
    # stmt = db.session.query(Export).statement
    # df   = pd.read_sql_query(stmt, db.session.bind)
    #  results = db.session.query.filter(Export.bal_rank).all()

    # results = db.session.query(Export.country, Export.bal_rank).all()
    # results = db.session.query(Export.country, Export.exp_ytd).all()
    #results = db.session.query(Export.exp_ytd).all()

    print('here are the results', results)

    jresults = []


    for result in results:
        # print("here is each result: ",result )
        jdic ={}
        jdic["country"] =result[0]
        jdic["balance_rank"] =result[1]
        jresults.append(jdic)

    return jsonify(jresults)



@app.route("/metadata/<sample>")
def sample_metadata(sample):
    """Return the MetaData for a given sample."""
    # sel = [
    #     Samples_Metadata.sample,
    #     Samples_Metadata.ETHNICITY,
    #     Samples_Metadata.GENDER,
    #     Samples_Metadata.AGE,
    #     Samples_Metadata.LOCATION,
    #     Samples_Metadata.BBTYPE,
    #     Samples_Metadata.WFREQ,
    # ]
    # sel = [
    #         Export.country,
    #         Export.bal_september,
    #         Export.bal_ytd	,
    #         Export.bal_rank	,
    #         Export.exp_september,
    #         Export.exp_ytd	,
    #         Export.exp_rank	,
    #         Export.september_cus,
    #         Export.ytd_cus	,
    #      ]


    sel = [
            econ_1_.country_name_a,
            econ_1_.World_Rank,
            econ_1_.Region_Rank,
            econ_1_._2019_Score,
            econ_1_.Property_Rights,
            econ_1_.Judical_Effectiveness,
            econ_1_.Government_Integrity,
            econ_1_.Tax_Burden,
            econ_1_.Govt_Spending,
            econ_1_.Fiscal_Health,
            econ_1_.Business_Freedom,
            econ_1_.Labor_Freedom,
            econ_1_.Monetary_Freedom,
            econ_1_.Trade_Freedom,
            econ_1_.Investment_Freedom,
            econ_1_.Financial_Freedom,
            econ_1_.Tariff_Rate,
            econ_1_.Income_Tax_Rate,
            econ_1_.Corporate_Tax_Rate,
            econ_1_.Tax_Burden__of_GDP,
            econ_1_.Govt_Expenditure_of_GDP,
            econ_1_.Population_Millions,
            econ_1_.GDP_Billions_PPP,
            econ_1_.GDP_Growth_Rate,
            econ_1_._5_Year_GDP_Growth_Rate,
            econ_1_.GDP_per_Capita_PPP,
            econ_1_.Unemployment,
            econ_1_.Inflation,
            econ_1_.FDI_Inflow_Millions,
            econ_1_.Public_Debtof_GDP
         ]


    results = db.session.query(*sel).filter(econ_1_.country_name_a == sample).all()

    sample_metadata = {}


    for result in results:
        # print("here is each result: ",result )
        # sample_metadata["Country"] = result[0]
        # sample_metadata["Balance September"] = result[1]
        # sample_metadata["Balance Year To Date"] = result[2]
        # sample_metadata["Balance Rank"] = result[3]
        # sample_metadata["Exports For September 2019"] = result[4]
        # sample_metadata["Exports Year To Date 2019"] = result[5]
        # sample_metadata["Export Rank"] = result[6]
        # sample_metadata["September CUS"] = result[7]
        # sample_metadata["Year To Date CUS"] = result[8]
        sample_metadata["A. Country"] = result[0]      
        sample_metadata["B. World Rank"]  = result[1]
        # sample_metadata["Region_Rank"]  = result[2]
        sample_metadata["C. 2019 Score"]  = result[3]
        # sample_metadata[" Property_Rights"]   = result[4]
        sample_metadata["L. Judical Efficieny"]  = result[5]
        sample_metadata["K. Govt Integrity"]  = result[6]
        sample_metadata["Q. Tax Burden"]  = result[7]
        sample_metadata["I. Govt Spending"]  = result[8]
        sample_metadata["E. Fiscal Health"]  = result[9]
        sample_metadata["M. Business Freedom"]  = result[10]
        # sample_metadata["P.  Labor Freedom"]  = result[11]
        # sample_metadata["Monetary_Freedom"]   = result[12]
        # sample_metadata["N.  Trade Freedom"]  = result[13]
        # sample_metadata["O.  Investment Freedom"]  = result[14]
        # sample_metadata["Financial_Freedom"]  = result[15]
        sample_metadata["P. Tariff Rate"]  = result[16]
        sample_metadata["R. Income Tax Rate"]  = result[17]
        sample_metadata["S. Corporate Tax Rate"]  = result[18]
        # sample_metadata["Tax_Burden__of_GDP"]  = result[19]
        # sample_metadata["Govt_Expend_of_GDP"]  = result[20]
        sample_metadata["D. Population Millions"]  = result[21]
        # sample_metadata["GDP_Billions_PPP"]   = result[22]
        sample_metadata["J. GDP Growth Rate"]  = result[23]
        # sample_metadata["_5_Year_GDP_Growth_Rate"] = result[24]
        # sample_metadata["GDP_per_Capita_PPP"] = result[25]
        sample_metadata["F. Unemployment"]  = result[26]
        sample_metadata["G. Inflation"]  = result[27]
        # sample_metadata["FDI_Inflow_Millions"]= result[28]
        sample_metadata["H. Public Debt of GDP"]  = result[29]

    # <option id="op1">  World_Rank           </option>
    # <option id="op1">  Government_Integrity </option>
    # <option id="op1">  Judical_Effectiveness</option>
    # <option id="op1">  Fiscal_Health        </option>
    # <option id="op1">  Inflation            </option>
    # <option id="op1">  Public_Debtof_GDP    </option>
    # <option id="op1">  Income_Tax_Rate      </option>
    # <option id="op1">  Corporate_Tax_Rate   </option>
    # <option id="op1">  Unemployment         </option>

    print("here is the sample meta data", sample_metadata)
    return jsonify(sample_metadata)

# /top_ten/World_Rank
@app.route("/top_ten/<user_selection>")

def top_ten_five(user_selection):
       
    sort_method = 0 
    method_list = [ 'World_Rank', 'Inflation','Public_Debtof_GDP', 'Income_Tax_Rate', 'Corporate_Tax_Rate','Unemployment']
    if user_selection in method_list :
        sort_method = 1  
    else :
        sort_method = 2 

    if ( user_selection == 'World_Rank'):
            query_var =  econ_1_.World_Rank # SORT ASC
    if ( user_selection == 'Inflation'):# SORT ASC
            query_var =  econ_1_.Inflation  # SORT ASC
    if ( user_selection == 'Public_Debtof_GDP'): # SORT ASC
            query_var =  econ_1_.Public_Debtof_GDP
    if ( user_selection == 'Income_Tax_Rate'):  # SORT ASC
            query_var =  econ_1_.Income_Tax_Rate
    if ( user_selection == 'Corporate_Tax_Rate'):  # SORT ASC
            query_var =  econ_1_.Corporate_Tax_Rate
    if ( user_selection == 'Unemployment'):  # SORT ASC
            query_var =  econ_1_.Unemployment

    if ( user_selection == 'Government_Integrity'):
            query_var =  econ_1_.Government_Integrity
    if ( user_selection == 'Judical_Effectiveness'):
            query_var =  econ_1_.Judical_Effectiveness
    if ( user_selection == 'Fiscal_Health'):
            query_var =  econ_1_.Fiscal_Health
    if ( user_selection == 'GDP_Billions_PPP'):
            query_var =  econ_1_.GDP_Billions_PPP
    if ( user_selection == 'Population_Millions'):
            query_var =  econ_1_.Population_Millions

    sel =   [
            econ_1_.country_name_a,
            query_var
            ]
    # #   TAKE THE SELECTION FROM WEBPAGE QUERY , GRAB THE COUNTRY NAMES AND THE SELECTION VALUES GRAP TOP 5 THEN BOTTOM 5 
    if (sort_method == 2) :
        results = db.session.query(*sel).filter(query_var>0).order_by(sel[1].desc()).limit(10).all()
    if (sort_method == 1) :
        results = db.session.query(*sel).filter(query_var>0).order_by(sel[1]).limit(10).all()

    # sample_data = {}
    all_results=[]
    complete_dict = {}
    sample_datas = {}
#     sample_datas = []

    for result in results:
                # sample_datas["name"] = result[0]
                # sample_datas["value"] = result[1]
                # all_results.append(sample_datas)
                print(result)
                sample_datas = { "name" : result[0] , "value" :format(result[1] , ',')  } 
                all_results.append(sample_datas)


    print("all_results are ", all_results )
        #     print("this is jdic", complete_dict) 
    return jsonify(all_results)
        # print(result)
        # print("result is", result )
        # print("result[0] is", result[0] )
        # print("result[0][1] is", result[1] ) 
        # sample_datas = {}
        #############################################
        # sample_datas["Country"] = result[0]
        # sample_datas[f"{user_selection}"] = result[1]
        #############################################
        # test below / works above 
        # sample_datas[ str(result[0])]= str(result[1])
        # all_results.append((result[1],')__', result[0]     ))
        #############################################
        # sample_datas[ result[0] ] = result[1]
        # all_results.append(sample_datas)
        #############################################
        # sample_datas[ result[0] ] = result[1]
        # sample_datas[ result[1] ] = result[0]
        # complete_dict.update(sample_datas)


        # print("all results", all_results)  
        # print("complete dict is:", complete_dict) 
        # j_complete_dict = jsonify(complete_dict)


#     all_results.append(complete_dict) 
#     print("this is jdic", complete_dict) 
#     return jsonify(all_results)

        # all_results.append( [result[1],result[0]])
        # all_results.append(result[1])

#     return jsonify(all_results )

  

        #############################################

    #         temps_dic = {}
    #         temps_dic["1_Minimum Temp"] = i[0]
    #         temps_dic["2_Average Temp"] = round( (i[1]),2) # can also do  = station, name
    #         temps_dic["3_Maximum Temp"] = i[2]
    #         all_results.append(temps_dic)





   #############################################################################################    
    # VARIOUS ALCHEMY SAMPLES 
    #############################################################################################    
    # same_sporder = session.query(EA, NA).filter(EA.sporder == NA.sporder).limit(10).all()

    # data_extract = session.query(Measurement.date, Measurement.prcp).\
    #     filter(Measurement.date >= '2016-08-23').\
    #     order_by(Measurement.date).all()

    # results = db.session.query(*sel).filter(econ_1_.country_name_a == sample)order_by(econ_1_.user_selection).limit(5).all()
    # results = db.session.query(*sel).filter(econ_1_.country_name_a == sample).all()
    #############################################################################################    
    # for  date, station, prcp, in results:
    #     all_results = []
    #     prcp_dic = {}
    #     prcp_dic["date"] = date 
    #     prcp_dic["station"] = station # can also do  = station, name
    #     prcp_dic["precipation"] = prcp
    #     all_results.append(prcp_dic)
    #     return jsonify(all_results)


    #     for i in results:
    #         temps_dic = {}
    #         temps_dic["1_Minimum Temp"] = i[0]
    #         temps_dic["2_Average Temp"] = round( (i[1]),2) # can also do  = station, name
    #         temps_dic["3_Maximum Temp"] = i[2]
    #         all_results.append(temps_dic)


    ############################################################################################

# @app.route("/samples/<sample>")
# def samples(sample):
#     """Return `otu_ids`, `otu_labels`,and `sample_values`."""
#     # stmt = db.session.query(Samples).statement
#     # df = pd.read_sql_query(stmt, db.session.bind)

#     df = pd.read_csv("db/country_trade.csv")

#     # Filter the data based on the sample number and
#     # only keep rows with values above 1
#     sample_data = df.loc[df[sample] > 1, ["Year-to-Date:IMP:CFI", "Country", sample]]

#     # Sort by sample
#     sample_data.sort_values(by=sample, ascending=False, inplace=True)

#     # Format the data to send as json
#     data = {
#         "otu_ids": sample_data.otu_id.values.tolist(),
#         "sample_values": sample_data[sample].values.tolist(),
#         "otu_labels": sample_data.otu_label.tolist(),
#           }
    # return jsonify(data)# 


if __name__ == "__main__":
    app.run()
   # logictest.run()
