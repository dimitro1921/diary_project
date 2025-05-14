from app.db import SessionLocal
from app import crud, models
from datetime import datetime
import random

def generate_daily_prompts():
    """
    Generates daily reflection entries in the database for each active user.
    """
    db = SessionLocal()
    try:
        users = crud.get_all_users(db)  # тепер через crud, а не .query()

        if not users:
            return

        with open("prompts/reflection_questions.txt", "r", encoding="utf-8") as f:
            prompts = [line.strip() for line in f if line.strip()]

        for user in users:
            question = random.choice(prompts)

            entry = models.Entry(
                user_id=user.id,
                message_id=0,
                username=user.username,
                text=question,
                entry_type=models.EntryType.reflection,
                source="prompted",
                timestamp=datetime.utcnow(),
                date_only=datetime.utcnow().date()
            )
            db.add(entry)

        db.commit()

    finally:
        db.close()
