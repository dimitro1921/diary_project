import os

structure = {
    "app": [
        "__init__.py",
        "config.py",
        "db.py",
        "models.py",
        "schemas.py",
        "crud.py",
        "exporter.py"
    ],
    "api": [
        "__init__.py",
        "main.py",
        "routes.py",
        "auth.py",
        "scheduler.py",
        "send_prompt.py"
    ],
    "bot": [
        "__init__.py",
        "main.py",
        "handlers.py",
        "states.py",
        "client.py"
    ],
    "prompts": [
        "reflection_questions.txt"
    ],
    "data": [
        "diary.db"
    ],
    ".": [  # root files
        ".env",
        "requirements.txt",
        "Dockerfile",
        "docker-compose.yml",
        "README.md"
    ]
}

for folder, files in structure.items():
    for file in files:
        path = os.path.join(folder, file) if folder else file
        os.makedirs(os.path.dirname(path), exist_ok=True)
        # Create file only if it doesn't exist
        if not os.path.exists(path):
            with open(path, "w", encoding="utf-8") as f:
                pass  # create empty file

print("Project structure created.")
