
# THIS SCRIPT IS TO FORMAT A TUPLE LIST INTO A TEXT STMT FOR SQL



def insert_data():
    data = [( "1", "abc", "03-01-2020" ) , ( "2", "xyz", "03-02-2020" )  ]
    print("data[0] is:" , data[0])
    package = ""
    ct = 1 
    for i in data :
        if (ct < len(data)):
            package = package +str(i)+ ","
        else:
            package = package +str(i)
        ct+=1
    
    stmt = f'''
        insert into test(col1, col2, col3)
        values {package} ;
    '''
        
    return stmt

print(insert_data())


