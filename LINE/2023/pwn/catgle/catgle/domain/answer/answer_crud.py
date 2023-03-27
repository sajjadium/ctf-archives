from datetime import datetime

from sqlalchemy.orm import Session

from domain.answer.answer_schema import AnswerCreate, AnswerUpdate
from models import Question, Answer, User

def create_answer(db: Session, 
                question: Question, 
                answer_create: AnswerCreate,
                user: User):
    db_answer = Answer(question=question,
                        content=answer_create.content,
                        is_markdown=answer_create.is_markdown,
                        create_date=datetime.now(),
                        user=user)
    db.add(db_answer)
    db.commit()

def get_answer(db: Session, answer_id: int):
    return db.query(Answer).get(answer_id)

def update_answer(db: Session, 
                db_answer: Answer,
                answer_update: AnswerUpdate):
    db_answer.content = answer_update.content
    db_answer.modify_date = datetime.now()
    db.add(db_answer)
    db.commit()

def delete_answer(db: Session,
                db_answer: Answer):
    db.delete(db_answer)
    db.commit()

def vote_answer(db: Session,
                db_answer: Answer,
                db_user: User):
    if db_user in db_answer.voters:
        db_answer.voters.remove(db_user)
    else:
        db_answer.voters.append(db_user)
    db.commit()