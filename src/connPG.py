########################## LIBRARY ###############################

import psycopg2

##################################################################

########################## VARIABLE ##############################

from src.envLoader import pg_user_name, pg_host_name, pg_password, pg_main_db, pg_port

##################################################################

# Establishing the connection
conn = psycopg2.connect(
    database=pg_main_db,
    user=pg_user_name,
    password=pg_password,
    host=pg_host_name,
    port=pg_port,
)
