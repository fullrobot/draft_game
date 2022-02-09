import databases


DATABASE_URL = "sqlite:///./data.db"

database = databases.Database(DATABASE_URL)
