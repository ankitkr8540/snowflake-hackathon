from snowflake.snowpark import Session
import snowflake.connector as snconn


def connection(account, username, password):
    # intialize new session and error
    new_session = None
    error = None
    connection_parameters = {
        "account": account,
        "user": username,
        "password": password,
    }  
    try:
        if account and username and password:
            new_session = Session.builder.configs(connection_parameters).create()
            print("New session created successfully!")
            print(new_session)
    except Exception as e:
        error = str(e)
    
    return new_session, error

def databaseConnection(username, password, account):
    if (username and password and account):
    # Create a connection object
        con = snconn.connect(
            user=username,
            password=password,
            account=account,
            warehouse="COMPUTE_WH",
            role="ACCOUNTADMIN"
        )
        return con