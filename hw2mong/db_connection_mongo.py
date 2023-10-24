#-------------------------------------------------------------------------
# AUTHOR: Estefania C
# FILENAME: db_connection_mongopy
# SPECIFICATION: description of the program
# FOR: CS 4250- Assignment #2
# TIME SPENT: 6hrs
#-----------------------------------------------------------*/

#IMPORTANT NOTE: DO NOT USE ANY ADVANCED PYTHON LIBRARY TO COMPLETE THIS CODE SUCH AS numpy OR pandas. You have to work here only with
# standard arrays

#importing some Python libraries
# --> add your Python code here
import re
from pymongo import MongoClient

def connectDataBase():

    # Create a database connection object using pymongo
    # --> add your Python code here
    
    DB_HOST = 'localhost:27017'
    
    try:
        client = MongoClient(host=[DB_HOST])
        db = client.corpus
        return db
        
    except:
        print("Database not connected")

def createDocument(col, docId, docText, docTitle, docDate, docCat):

#     # create a dictionary to count how many times each term appears in the document.
#     # Use space " " as the delimiter character for terms and remember to lowercase them.
#     # --> add your Python code here

    terms = re.sub(r'[^\w\s]', '', docText)
    
    terms = terms.lower().split()
    
    countdict = {}
    
    for x in terms:
        
        if x not in countdict.keys():
            
            countdict.update({x: terms.count(x)})
        
    

#     # create a list of dictionaries to include term objects.
#     # --> add your Python code here

    dictlist = []
    
    for word,c in countdict.items():
        
        ex = {"term": word, "numbchar": len(word), "count": c}
        dictlist.append(ex)

#     #Producing a final document as a dictionary including all the required document fields
#     # --> add your Python code here

    nc = 0
    
    for y in terms:
        nc = nc + len(y)
        
    cname = docCat
    
    if cname == "Sports":
        cid = 1
        
    elif cname == "Seasons":
        cid = 2
        
    doc = {
        "docnumb": docId,
        "dtext": docText,
        "dtitle": docTitle,
        "date": docDate,
        "dnumb_chars": nc,
        "catid": cid,
        "category": docCat,
        "Terms": dictlist
    }

#     # Insert the document
#     # --> add your Python code here

    col.insert_one(doc)
    
def deleteDocument(col, docId):

#     # Delete the document from the database
#     # --> add your Python code here

    col.delete_one({'docnumb': docId})

def updateDocument(col, docId, docText, docTitle, docDate, docCat):

#     # Delete the document
#     # --> add your Python code here

    deleteDocument(col, docId)
    
#     # Create the document with the same id
#     # --> add your Python code here

    createDocument(col, docId, docText, docTitle, docDate, docCat)

def getIndex(col):

#     # Query the database to return the documents where each term occurs with their corresponding count. Output example:
#     # {'baseball':'Exercise:1','summer':'Exercise:1,California:1,Arizona:1','months':'Exercise:1,Discovery:3'}
#     # ...
#     # --> add your Python code here

    pipeline = [
     {
        '$unwind': {
            'path': '$Terms'
        }
     },
     {
         '$group':{
             '_id':[
                 '$dtitle', '$Terms.term'
             ],
             'count': {
                 '$sum': "$Terms.index.count"
             }
         }
     },
     {
         '$sort':{
             'Terms.term': 1
         }
     }
        
    ]
    
    documents = col.aggregate(pipeline)
    print(documents)
    iindex = {}
    dum = ''
    for x in documents:
        dtitle = x['_id'][0]
        term = x['_id'][1]
        termc = x['count']
        if dum != term:
            val = dtitle + ':' + str(termc)
            dum = term
        else:
            val += ', ' + dtitle + ':' + str(termc)
        
        iindex.update({term: val})
        
    return iindex