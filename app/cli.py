from app.extensions import db
from app.models import Level
from app.utils.crypto import hash_answer


def register_cli(app):

    # -----------------------
    # Create Level
    # -----------------------
    @app.cli.command("create-level")
    def create_level():
        level_number = int(input("Level number: "))
        title = input("Title: ")
        description = input("Description: ")
        answer = input("Initial answer (plaintext): ")

        if Level.query.filter_by(level_number=level_number).first():
            print("Level already exists.")
            return

        level = Level(
            level_number=level_number,
            title=title,
            description=description,
            unlock_type="answer",
            answer_hashes=[hash_answer(answer)],
            is_active=True
        )

        db.session.add(level)
        db.session.commit()

        print(f"Level {level_number} created.")

    # -----------------------
    # Replace Answer
    # -----------------------
    @app.cli.command("set-answer")
    def set_answer():
        level_number = int(input("Level number: "))
        answer = input("New answer (plaintext): ")

        level = Level.query.filter_by(level_number=level_number).first()

        if not level:
            print("Level not found.")
            return

        level.answer_hashes = [hash_answer(answer)]
        db.session.commit()

        print(f"Answer for level {level_number} updated.")

    # -----------------------
    # Add Alternate Answer
    # -----------------------
    @app.cli.command("add-answer")
    def add_answer():
        level_number = int(input("Level number: "))
        answer = input("Additional valid answer: ")

        level = Level.query.filter_by(level_number=level_number).first()

        if not level:
            print("Level not found.")
            return

        hashed = hash_answer(answer)

        if hashed not in level.answer_hashes:
            level.answer_hashes.append(hashed)
            db.session.commit()
            print("Answer added.")
        else:
            print("Answer already exists.")

    # -----------------------
    # List Answers
    # -----------------------
    @app.cli.command("list-answers")
    def list_answers():
        level_number = int(input("Level number: "))

        level = Level.query.filter_by(level_number=level_number).first()

        if not level:
            print("Level not found.")
            return

        print("Stored hashes:")
        for h in level.answer_hashes:
            print(h)
