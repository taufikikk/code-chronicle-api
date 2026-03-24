"""Seed database. Usage: python seed_db.py [--reset]"""
import sys
from app import create_app, db
import models

def seed_all(reset=False):
    app = create_app()
    with app.app_context():
        if reset:
            print("Dropping tables...")
            db.drop_all()
        print("Creating tables...")
        db.create_all()

        if models.Chapter.query.first() and not reset:
            print("Already seeded. Use --reset.")
            return

        print("Seeding...")
        from seed.chapter0 import seed as seed_ch0
        from seed.chapter1 import seed as seed_ch1
        seed_ch0(db, models)
        seed_ch1(db, models)

        ch = models.Chapter.query.count()
        sc = models.Scene.query.count()
        ln = models.Line.query.count()
        gl = models.GlossaryTerm.query.count()
        dd = models.DeepDive.query.count()
        pr = models.Practice.query.count()
        bg = models.BugExample.query.count()
        tr = models.TraceExercise.query.count()
        iv = models.InterviewQ.query.count()
        fc = models.Flashcard.query.count()
        dq = models.DeepQuiz.query.count()

        print(f"\nDone! Chapters:{ch} Scenes:{sc} Lines:{ln} Glossary:{gl}")
        print(f"DeepDive:{dd} Practice:{pr} Bugs:{bg} Traces:{tr} Interview:{iv} Flashcards:{fc} DeepQuiz:{dq}")

if __name__ == "__main__":
    seed_all("--reset" in sys.argv)
