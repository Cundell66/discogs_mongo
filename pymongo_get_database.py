import os

from pymongo import MongoClient

password = os.environ.get("mongopass")
# password = "kiGcVu7OiiCLF7Ml"

def get_database():
 
   # Provide the mongodb atlas url to connect python to mongodb using pymongo
                                        #   mongodb+srv://paulplr:<kiGcVu7OiiCLF7Ml>@cluster0.lqswcrx.mongodb.net/
   CONNECTION_STRING = f"mongodb+srv://paulplr:{password}@cluster0.lqswcrx.mongodb.net/vinyllog"
 
   # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
   client = MongoClient(CONNECTION_STRING)
 
   # Create the database for our example (we will use the same database throughout the tutorial
   return client['vinyllog']
  
# This is added so that many files can reuse the function get_database()
if __name__ == "__main__":   
  
   # Get the database
   dbname = get_database()