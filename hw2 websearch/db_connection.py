#-------------------------------------------------------------------------
# AUTHOR: Estefania Chavez
# FILENAME: db_connection.py
# SPECIFICATION: database python code
# FOR: CS 4250- Assignment #2
# TIME SPENT: 10 hrs
#-----------------------------------------------------------*/

#IMPORTANT NOTE: DO NOT USE ANY ADVANCED PYTHON LIBRARY TO COMPLETE THIS CODE SUCH AS numpy OR pandas. You have to work here only with
# standard arrays
#importing some Python libraries
# --> add your Python code here
import psycopg2
from psycopg2.extras import RealDictCursor

#clean text from characters like periods
def cleanText(str):
    newString = str.replace(" ", "")
    newString = newString.replace(".", "")
    newString = newString.replace(",", "")
    newString = newString.replace(";", "")
    newString = newString.replace("!", "")
    newString = newString.replace("?", "")
    newString = newString.replace(":", "")
    newString = newString.replace("(", "")
    newString = newString.replace(")", "")
    newString = newString.replace("-", "")
    newString = newString.replace("'", "")
    newString = newString.replace("[", "")
    newString = newString.replace("]", "")
    newString = newString.replace("\"", "") #double check this
    newString = newString.replace("/", "")
    newString = newString.replace("", "")
    return len(newString)
    
def cleanTextWS(str):
    newString = str.replace(".", "")
    newString = newString.replace(",", "")
    newString = newString.replace(";", "")
    newString = newString.replace("!", "")
    newString = newString.replace("?", "")
    newString = newString.replace(":", "")
    newString = newString.replace("(", "")
    newString = newString.replace(")", "")
    newString = newString.replace("-", "")
    newString = newString.replace("'", "")
    newString = newString.replace("[", "")
    newString = newString.replace("]", "")
    newString = newString.replace("\"", "") #double check this
    newString = newString.replace("/", "")
    newString = newString.replace("", "")
    return newString.lower()

def connectDataBase():

    # Create a database connection object using psycopg2
    # --> add your Python code here
    DB_NAME = "H2"
    DB_USER = "postgres"
    DB_PASS = "123"
    DB_HOST = "localhost"
    DB_PORT = "5432"
    
    try:
        conn = psycopg2.connect(database=DB_NAME,
                                user=DB_USER,
                                password=DB_PASS,
                                host=DB_HOST,
                                port=DB_PORT,
                                cursor_factory=RealDictCursor)
        return conn

    except:
        print("Database not connected successfully")

def createCategory(cur, catId, catName):
    
    # Insert a category in the database
    # --> add your Python code here    
    sql = "Insert into category (cid, cname) VALUES (%s, %s)"
    
    recset = [catId, catName]
    
    cur.execute(sql, recset)
        
def createDocument(cur, docId, docText, docTitle, docDate, docCat):
    # 1 Get the category id based on the informed category name
    # --> add your Python code here
    sql = "Select cid from category where cname = %(docCat)s"
    
    cur.execute(sql, {'docCat': docCat})
    
    recset = cur.fetchall()
    
    cidcat = str(recset[0]['cid'])
    
    # 2 Insert the document in the database. For num_chars, discard the spaces and punctuation marks.
    # --> add your Python code here
    numbc = cleanText(docText)
    
    sql2 = "Insert into documents (dnumb, dtext, dtitle, ddate, numb_chars, catid) VALUES (%s, %s, %s, %s, %s, %s)"
    
    recset = [docId, docText, docTitle, docDate, numbc, cidcat]
    
    cur.execute(sql2, recset)
    
    # 3 Update the potential new terms.
    # 3.1 Find all terms that belong to the document. Use space " " as the delimiter character for terms and Remember to lowercase terms and remove punctuation marks.
    # 3.2 For each term identified, check if the term already exists in the database
    # 3.3 In case the term does not exist, insert it into the database
    # --> add your Python code here
    
    newtxt = cleanTextWS(docText)
    listnewtxt = newtxt.split()
    
    for x in listnewtxt:
        num = len(x)
        sql3 = "select term from terms where terms.term = %(listnewtxt)s"
        cur.execute(sql3, {"listnewtxt": x})
        recset = cur.fetchall()
        if recset == []:
            sql4 = "Insert into terms (term, num_chars) VALUES (%s, %s)"
            recset = [x, num]
            cur.execute(sql4, recset)
        else:
            print(x, "is not new")
    
        
    # 4 Update the index
    # 4.1 Find all terms that belong to the document
    # 4.2 Create a data structure the stores how many times (count) each term appears in the document
    # 4.3 Insert the term and its corresponding count into the database
    # --> add your Python code here
    
    w = {}
        
    for x in listnewtxt:
        if x not in w.keys():
            w.update({x : listnewtxt.count(x)})
            
    for y, z in w.items():
        sql5 = "Insert into index (count, tterm, ddnum) Values (%s, %s, %s)"
        recset = [z, y, docId]
        cur.execute(sql5, recset)
        

def deleteDocument(cur, docId):
    # 1 Query the index based on the document to identify terms
    # 1.1 For each term identified, delete its occurrences in the index for that document
    # 1.2 Check if there are no more occurrences of the term in another document. If this happens, delete the term from the database.
    # --> add your Python code here
    
    sql6 = "Select tterm from index where ddnum = %(docId)s"
    cur.execute(sql6, {"docId" : docId})
    recset = cur.fetchall()
    
    a = []
    b = []
    
    for rec in recset:
        a.append(dict(rec))
    for ab in a:
        b.append(ab["tterm"])
        
    sql7 = "Delete from index where ddnum = %(docId)s"
    cur.execute(sql7, {"docId": docId})
    
    for x in b:
        sql8 = "Select ddnum from index where tterm = %(listnewtxt)s"
        cur.execute(sql8, {"listnewtxt": x})
        recset = cur.fetchall()
        
        if recset == []:
            sql9 = "Delete from terms where term = %(listnewtxt)s"
            cur.execute(sql9, {"listnewtxt": x})
            
    # 2 Delete the document from the database
    # --> add your Python code here
    
    sql10 = "Delete from documents where dnumb = %(docId)s"
    cur.execute(sql10, {"docId": docId})
    
def updateDocument(cur, docId, docText, docTitle, docDate, docCat):
    # 1 Delete the document
    # --> add your Python code here
    
    deleteDocument(cur, docId)
    
    # 2 Create the document with the same id
    # --> add your Python code here

    createDocument(cur, docId, docText, docTitle, docDate, docCat)

def getIndex(cur):
    # Query the database to return the documents where each term occurs with their corresponding count. Output example:
    # {'baseball':'Exercise:1','summer':'Exercise:1,California:1,Arizona:1','months':'Exercise:1,Discovery:3'}
    # ...
    # --> add your Python code here
    
    cur.execute("Select term, dtitle, count from terms inner join index on terms.term = index.tterm inner join documents on index.ddnum = documents.dnumb order by terms.term")
    
    dict = {}
    s = ''
    t = ''
    results = cur.fetchall()
    
    for x in results:
        if t != x['term']:
            s = x['dtitle'] + ':' + str(x['count'])
            t = x['term']
        else:
            s += ', ' + x['dtitle'] + ':' + str(x['count'])
    
        dict.update({x['term'] : s})
        
    return dict