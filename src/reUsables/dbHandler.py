import cx_Oracle
import pandas as pd
from sqlalchemy.engine import create_engine


class DbHandler:

    def setInstantClient(self, instantPath):
        cx_Oracle.init_oracle_client(instantPath)
        print("cx_oracle instant client has been set")

    def connectIntoOracle(self, userName, password, hostName, port, serviceName):
        try:
            DIALECT = 'oracle'
            SQL_DRIVER = 'cx_oracle'
            sid = cx_Oracle.makedsn(hostName, port, service_name=serviceName)
            ENGINE_PATH_WIN_AUTH = "{0}+{1}://{2}:%s@{3}".format(DIALECT, SQL_DRIVER, userName, sid)
            from urllib.parse import quote_plus as urlquote
            engine = create_engine(ENGINE_PATH_WIN_AUTH % urlquote(password))
            return engine
        except Exception as e:
            print(e)
            print("Username : {0}\nPassword : {1}\nHostName : {2}\nPort : {3}\nServiceName : {4}"
                  .format(userName, password, hostName, port, serviceName))
            assert 0 == 1, "Unable to connect into oracle Database"

    def select(self, engine, query):
        try:
            resultDF = pd.read_sql_query(query, engine)
            return resultDF
        except Exception as e:
            print("Unable to fetch data for query")
            return {"error": str(e)}

    def callProcedure(self, engine, query):
        print(query)
        try:
            connection = engine.raw_connection()
            cursor = connection.cursor()
            cursor.execute(query)
            return "Done"
        except Exception as e:
            print("Unable to execute the Procedure")
            print(e)
        finally:
            connection.close()
            cursor.close()

    def getTableColumnNames(self, engine, tableName):
        query = "select * from {0} where 0=1".format(tableName)
        try:
            resultDF = pd.read_sql_query(query, engine)
            return resultDF.columns.values.tolist()
        except Exception as e:
            print("Unable to fetch data for query")
            print(e)