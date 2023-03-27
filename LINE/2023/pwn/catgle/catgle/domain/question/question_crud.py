from datetime import datetime

from domain.question.question_schema import QuestionCreate, QuestionUpdate
from models import Question, Answer, User
from sqlalchemy.orm import Session

def get_question_list(db: Session, skip: int = 0, limit: int = 10, keyword: str = ''):
    question_list = db.query(Question)
    if keyword:
        print(keyword)
        search = "%{}%".format(keyword)
        sub_query = db.query(Answer.question_id, Answer.content, User.username)\
                            .outerjoin(User, Answer.user_id == User.id).subquery()
        question_list = question_list.outerjoin(User)\
                                    .outerjoin(sub_query, sub_query.c.question_id == Question.id)\
                                    .filter(Question.subject.ilike(search) |
                                            Question.content.ilike(search) |
                                            User.username.ilike(search) |
                                            sub_query.c.content.ilike(search) |
                                            sub_query.c.username.ilike(search)
                                        )
    total = question_list.distinct().count()
    question_list = question_list.order_by(Question.create_date.desc())\
                            .offset(skip).limit(limit).distinct().all()
    return total, question_list

def get_question(db: Session, question_id: int):
    question = db.query(Question).get(question_id)
    return question

def create_question(db: Session, 
                    question_create:QuestionCreate,
                    user: User):
        db_question = Question(subject=question_create.subject,
                                content=question_create.content,
                                is_markdown=question_create.is_markdown,
                                create_date=datetime.now(),
                                user=user)
        db.add(db_question)
        db.commit()

def update_question(db: Session,
                    db_question: Question,
                    question_update: QuestionUpdate):
    db_question.subject = question_update.subject
    db_question.content = question_update.content
    db_question.modify_date = datetime.now()
    db_question.is_markdown = question_update.is_markdown
    db.add(db_question)
    db.commit()

def delete_question(db: Session,
                    db_question: Question):
    db.delete(db_question)
    db.commit()

def vote_question(db: Session,
                db_question: Question, db_user: User):
    if db_user in db_question.voters:
        db_question.voters.remove(db_user)
    else:
        db_question.voters.append(db_user)
    db.commit()