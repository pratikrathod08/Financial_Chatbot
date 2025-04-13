# create_tables.py

from app.database.database import Base, engine
from app.models.models import ChatHistory, User

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    print("✅ All tables created successfully.")
