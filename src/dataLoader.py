#######################   FUNCTION   #############################

from src.createNewPDF import createLocalPDF

##################################################################

########################## VARIABLE ##############################

from src.connPG import conn
from src.envLoader import vbhc_query, book_query

##################################################################


def getCriteriaData(path, domain, type=""):
    data = ""
    cursor = conn.cursor()

    if domain == "admin-doc":
        domain_col = "VBHC"
        cursor.execute(vbhc_query, (domain_col, type))
        res = cursor.fetchone()
        data = res[0]

    if domain == "book":
        domain_col = "Sách"
        cursor.execute(book_query, (domain_col,))
        res = cursor.fetchone()
        data = res[0]

    createLocalPDF(data, path)
