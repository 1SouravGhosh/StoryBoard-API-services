
from flask_sqlalchemy import SQLAlchemy

#db_string = "dbname= db_foodease  user= postgres host= localhost password=tiger123 port= 5432"
DB_URL = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(user="postgres",pw="tiger123",url="localhost",db="db_storyboard")

db = SQLAlchemy()



