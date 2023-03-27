from datetime import datetime

from sqlalchemy.orm import Session

from domain.answer.answer_schema import AnswerCreate, AnswerUpdate
from models import User, Chall

def create_chall(db: Session,
                source: str,
                user: User,
                category: str,
                file_name: str,
                file_size: int,
                failed: bool,
                failed_reason: str):
    new_chall = Chall(user_id=user.id,
                    user=user,
                    category=category,
                    source=source,
                    file_name=file_name,
                    file_size=file_size,
                    submission_date=datetime.now(),
                    failed=failed,
                    reason=failed_reason)
    db.add(new_chall)
    db.commit()
    
def get_chall_by_category(db: Session,
                        user: User,
                        category: str):
    return db.query(Chall).filter(
        (Chall.category == category) &
        (Chall.id == User.id)
    ).first()

def delete_chall_by_category(db: Session,
                            user: User,
                            category: str):
    chall = db.query(Chall).filter(
        (Chall.category == category) &
        (Chall.id == User.id)
    ).first()
    if chall:
        db.delete(chall)
        db.commit()