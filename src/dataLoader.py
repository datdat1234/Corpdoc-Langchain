#######################   FUNCTION   #############################

from src.createNewPDF import createLocalPDF

##################################################################

########################## VARIABLE ##############################

from src.connPG import conn
from src.envLoader import vbhc_query_level1, book_query_hc, book_query_phc

##################################################################


def getCriteriaData(path, domain):
    data = ""
    cursor = conn.cursor()

    if domain == "admin-doc":
        cursor.execute(vbhc_query_level1)
        res = cursor.fetchone()
        data = res[0]

    if domain == "book":
        cursor.execute(book_query_hc)
        res = cursor.fetchone()
        data = data + res[0]
        
        cursor.execute(book_query_phc)
        res = cursor.fetchone()
        data = data + res[0]

    createLocalPDF(data, path)
    
def queryData(query):
    cursor = conn.cursor()
    cursor.execute(query)
    res = cursor.fetchone()
    return res[0]
    