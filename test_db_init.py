from app.db import Base, engine

# Import this to define Entry model if you already have it
# from app.models import Entry

if __name__ == "__main__":
    print("Creating database schema...")
    Base.metadata.create_all(bind=engine)
    print("✅ Done. Check data/diary.db file.")
