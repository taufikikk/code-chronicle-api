from app import db
from datetime import datetime, timezone
import json


class Chapter(db.Model):
    __tablename__ = "chapters"
    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(100), unique=True, nullable=False)
    title = db.Column(db.String(200), nullable=False)
    subtitle = db.Column(db.String(300))
    topic = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    order = db.Column(db.Integer, nullable=False, default=0)
    is_published = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    scenes = db.relationship("Scene", backref="chapter", lazy="joined", order_by="Scene.order")
    glossary_terms = db.relationship("GlossaryTerm", backref="chapter_ref", lazy="select")
    deep_dives = db.relationship("DeepDive", backref="chapter", lazy="select", order_by="DeepDive.order")
    practices = db.relationship("Practice", backref="chapter", lazy="select", order_by="Practice.order")
    cheatsheets = db.relationship("Cheatsheet", backref="chapter", lazy="select", order_by="Cheatsheet.order")
    bugs = db.relationship("BugExample", backref="chapter", lazy="select", order_by="BugExample.order")
    traces = db.relationship("TraceExercise", backref="chapter", lazy="select", order_by="TraceExercise.order")
    interviews = db.relationship("InterviewQ", backref="chapter", lazy="select", order_by="InterviewQ.order")
    flashcards = db.relationship("Flashcard", backref="chapter", lazy="select", order_by="Flashcard.order")
    deep_quizzes = db.relationship("DeepQuiz", backref="chapter", lazy="select", order_by="DeepQuiz.order")
    challenge = db.relationship("Challenge", backref="chapter", uselist=False)

    def to_dict(self, full=False):
        d = {"id": self.id, "slug": self.slug, "title": self.title, "subtitle": self.subtitle,
             "topic": self.topic, "description": self.description, "order": self.order}
        if full:
            d["scenes"] = [s.to_dict() for s in self.scenes]
            d["deep_dives"] = [x.to_dict() for x in self.deep_dives]
            d["practices"] = [x.to_dict() for x in self.practices]
            d["cheatsheets"] = [x.to_dict() for x in self.cheatsheets]
            d["bugs"] = [x.to_dict() for x in self.bugs]
            d["traces"] = [x.to_dict() for x in self.traces]
            d["interviews"] = [x.to_dict() for x in self.interviews]
            d["flashcards"] = [x.to_dict() for x in self.flashcards]
            d["deep_quizzes"] = [x.to_dict() for x in self.deep_quizzes]
            d["challenge"] = self.challenge.to_dict() if self.challenge else None
        return d


class Scene(db.Model):
    __tablename__ = "scenes"
    id = db.Column(db.Integer, primary_key=True)
    chapter_id = db.Column(db.Integer, db.ForeignKey("chapters.id"), nullable=False)
    slug = db.Column(db.String(100), nullable=False)
    filename = db.Column(db.String(100), nullable=False)
    order = db.Column(db.Integer, nullable=False, default=0)
    is_choice_target = db.Column(db.Boolean, default=False)
    choice_group = db.Column(db.String(50))
    lines = db.relationship("Line", backref="scene", lazy="joined", order_by="Line.order")
    def to_dict(self):
        return {"slug": self.slug, "filename": self.filename, "order": self.order,
                "is_choice_target": self.is_choice_target, "choice_group": self.choice_group,
                "lines": [l.to_dict() for l in self.lines]}


class Line(db.Model):
    __tablename__ = "lines"
    id = db.Column(db.Integer, primary_key=True)
    scene_id = db.Column(db.Integer, db.ForeignKey("scenes.id"), nullable=False)
    char = db.Column(db.String(50), nullable=False)
    text = db.Column(db.Text, nullable=False)
    style = db.Column(db.String(50))
    order = db.Column(db.Integer, nullable=False, default=0)
    choice_options = db.Column(db.Text)
    def to_dict(self):
        d = {"char": self.char, "text": self.text, "order": self.order}
        if self.style: d["style"] = self.style
        if self.choice_options: d["choice"] = {"options": json.loads(self.choice_options)}
        return d


class GlossaryTerm(db.Model):
    __tablename__ = "glossary_terms"
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(100), nullable=False)
    term = db.Column(db.String(200), nullable=False)
    type = db.Column(db.String(50))
    short = db.Column(db.Text, nullable=False)
    detail = db.Column(db.Text)
    chapter_id = db.Column(db.Integer, db.ForeignKey("chapters.id"))
    def to_dict(self):
        return {"key": self.key, "term": self.term, "type": self.type,
                "short": self.short, "detail": self.detail, "chapter_id": self.chapter_id}


class DeepDive(db.Model):
    __tablename__ = "deep_dives"
    id = db.Column(db.Integer, primary_key=True)
    chapter_id = db.Column(db.Integer, db.ForeignKey("chapters.id"), nullable=False)
    order = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    code = db.Column(db.Text)
    keypoint = db.Column(db.Text)
    def to_dict(self):
        return {"order": self.order, "title": self.title, "content": self.content,
                "code": self.code, "keypoint": self.keypoint}


class Practice(db.Model):
    __tablename__ = "practices"
    id = db.Column(db.Integer, primary_key=True)
    chapter_id = db.Column(db.Integer, db.ForeignKey("chapters.id"), nullable=False)
    order = db.Column(db.Integer, nullable=False)
    qtype = db.Column(db.String(20), nullable=False)
    question = db.Column(db.Text, nullable=False)
    code = db.Column(db.Text)
    options_json = db.Column(db.Text)
    answer = db.Column(db.String(200))
    explanation = db.Column(db.Text)
    category = db.Column(db.String(50))
    def to_dict(self):
        d = {"id": self.id, "order": self.order, "type": self.qtype, "question": self.question,
             "explanation": self.explanation, "category": self.category}
        if self.code: d["code"] = self.code
        if self.options_json: d["options"] = json.loads(self.options_json)
        if self.answer: d["answer"] = self.answer
        return d


class Cheatsheet(db.Model):
    __tablename__ = "cheatsheets"
    id = db.Column(db.Integer, primary_key=True)
    chapter_id = db.Column(db.Integer, db.ForeignKey("chapters.id"), nullable=False)
    order = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    def to_dict(self):
        return {"order": self.order, "title": self.title, "content": self.content}


class BugExample(db.Model):
    __tablename__ = "bug_examples"
    id = db.Column(db.Integer, primary_key=True)
    chapter_id = db.Column(db.Integer, db.ForeignKey("chapters.id"), nullable=False)
    order = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    buggy_code = db.Column(db.Text, nullable=False)
    fixed_code = db.Column(db.Text, nullable=False)
    why = db.Column(db.Text)
    def to_dict(self):
        return {"order": self.order, "title": self.title, "description": self.description,
                "buggy_code": self.buggy_code, "fixed_code": self.fixed_code, "why": self.why}


class TraceExercise(db.Model):
    __tablename__ = "trace_exercises"
    id = db.Column(db.Integer, primary_key=True)
    chapter_id = db.Column(db.Integer, db.ForeignKey("chapters.id"), nullable=False)
    order = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(200), nullable=False)
    code = db.Column(db.Text, nullable=False)
    steps_json = db.Column(db.Text, nullable=False)
    question = db.Column(db.Text)
    answer = db.Column(db.String(200))
    explanation = db.Column(db.Text)
    def to_dict(self):
        return {"order": self.order, "title": self.title, "code": self.code,
                "steps": json.loads(self.steps_json), "question": self.question,
                "answer": self.answer, "explanation": self.explanation}


class InterviewQ(db.Model):
    __tablename__ = "interview_questions"
    id = db.Column(db.Integer, primary_key=True)
    chapter_id = db.Column(db.Integer, db.ForeignKey("chapters.id"), nullable=False)
    order = db.Column(db.Integer, nullable=False)
    question = db.Column(db.Text, nullable=False)
    answer = db.Column(db.Text, nullable=False)
    tip = db.Column(db.Text)
    def to_dict(self):
        return {"order": self.order, "question": self.question, "answer": self.answer, "tip": self.tip}


class Flashcard(db.Model):
    __tablename__ = "flashcards"
    id = db.Column(db.Integer, primary_key=True)
    chapter_id = db.Column(db.Integer, db.ForeignKey("chapters.id"), nullable=False)
    order = db.Column(db.Integer, nullable=False)
    front = db.Column(db.Text, nullable=False)
    back = db.Column(db.Text, nullable=False)
    def to_dict(self):
        return {"order": self.order, "front": self.front, "back": self.back}


class DeepQuiz(db.Model):
    __tablename__ = "deep_quizzes"
    id = db.Column(db.Integer, primary_key=True)
    chapter_id = db.Column(db.Integer, db.ForeignKey("chapters.id"), nullable=False)
    order = db.Column(db.Integer, nullable=False)
    qtype = db.Column(db.String(20), nullable=False)  # write, predict, draw, explain, debug
    difficulty = db.Column(db.String(20), nullable=False)  # basic, medium, hard, master
    question = db.Column(db.Text, nullable=False)
    hint = db.Column(db.Text)
    accept_json = db.Column(db.Text, nullable=False)  # JSON array of acceptable answer substrings
    perfect = db.Column(db.Text, nullable=False)  # model answer
    explanation = db.Column(db.Text)
    def to_dict(self):
        return {"id": self.id, "order": self.order, "type": self.qtype, "difficulty": self.difficulty,
                "question": self.question, "hint": self.hint,
                "accept": json.loads(self.accept_json), "perfect": self.perfect,
                "explanation": self.explanation}


class Challenge(db.Model):
    __tablename__ = "challenges"
    id = db.Column(db.Integer, primary_key=True)
    chapter_id = db.Column(db.Integer, db.ForeignKey("chapters.id"), nullable=False)
    buggy_code = db.Column(db.Text, nullable=False)
    fixed_code = db.Column(db.Text, nullable=False)
    starter_code = db.Column(db.Text, nullable=False)
    validation_rules = db.Column(db.Text, nullable=False)
    hints = db.Column(db.Text)
    def to_dict(self):
        return {"buggy_code": self.buggy_code, "fixed_code": self.fixed_code,
                "starter_code": self.starter_code,
                "validation_rules": json.loads(self.validation_rules),
                "hints": json.loads(self.hints) if self.hints else []}


class UserProgress(db.Model):
    __tablename__ = "user_progress"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(100), nullable=False)
    chapter_id = db.Column(db.Integer, db.ForeignKey("chapters.id"), nullable=False)
    current_scene_slug = db.Column(db.String(100))
    choice_made = db.Column(db.String(100))
    challenge_completed = db.Column(db.Boolean, default=False)
    completed = db.Column(db.Boolean, default=False)
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc),
                           onupdate=lambda: datetime.now(timezone.utc))
    __table_args__ = (db.UniqueConstraint("user_id", "chapter_id", name="uq_user_chapter"),)
    def to_dict(self):
        return {"chapter_id": self.chapter_id, "current_scene_slug": self.current_scene_slug,
                "choice_made": self.choice_made, "challenge_completed": self.challenge_completed,
                "completed": self.completed}
