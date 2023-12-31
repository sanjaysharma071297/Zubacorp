from pymongo import MongoClient

def get_database():
   # Provide the mongodb atlas url to connect python to mongodb using pymongo
   connection_string = "<provide_your_connection_string>"

   # Create a connection using MongoClient.
   client = MongoClient(connection_string)

   # Create the database 
   return client['zaubacorp_company_data']
  
# This is added so that many files can reuse the function get_database()
if __name__ == "__main__":
   # Get the database
   dbname = get_database()
