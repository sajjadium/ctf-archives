from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from database import get_db
from domain.answer import answer_schema, answer_crud
from domain.question import question_crud
from domain.user.user_router import get_current_user
from models import User

router = APIRouter(
    prefix="/api/answer"
)

@router.post("/create/{question_id}", status_code=status.HTTP_204_NO_CONTENT)
def answer_create(question_id: int,
                    _answer_create:answer_schema.AnswerCreate,
                    db:Session = Depends(get_db),
                    current_user: User = Depends(get_current_user)):
    if current_user.last_activity is not None and \
            (datetime.now() - current_user.last_activity).seconds <= 3:
        raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                            detail="sending too many requests. wait 3 seconds and retry")
    current_user.last_activity = datetime.now()
    question = question_crud.get_question(db, question_id=question_id)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    answer_crud.create_answer(db, question=question,
                                answer_create=_answer_create,
                                user=current_user)

@router.get('/detail/{answer_id}', response_model=answer_schema.Answer)
def answer_data(answer_id: int, db: Session = Depends(get_db)):
    answer = answer_crud.get_answer(db, answer_id=answer_id)
    return answer

@router.put('/update', status_code=status.HTTP_204_NO_CONTENT)
def answer_update(_answer_update: answer_schema.AnswerUpdate,
                db: Session = Depends(get_db),
                current_user: User = Depends(get_current_user)):
    if current_user.last_activity is not None and \
            (datetime.now() - current_user.last_activity).seconds <= 3:
        raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                            detail="sending too many requests. wait 3 seconds and retry")
    current_user.last_activity = datetime.now()
    db_answer = answer_crud.get_answer(db, answer_id=_answer_update.answer_id)
    if not db_answer or \
            current_user.id != db_answer.user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='invalid comment id')
    answer_crud.update_answer(db=db,
                            db_answer=db_answer,
                            answer_update=_answer_update)

@router.delete('/delete', status_code=status.HTTP_204_NO_CONTENT)
def answer_delete(_answer_delete: answer_schema.AnswerDelete,
                db: Session = Depends(get_db),
                current_user: User = Depends(get_current_user)):
    if current_user.last_activity is not None and \
            (datetime.now() - current_user.last_activity).seconds <= 3:
        raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                            detail="sending too many requests. wait 3 seconds and retry")
    current_user.last_activity = datetime.now()
    db_answer = answer_crud.get_answer(db, answer_id=_answer_delete.answer_id)
    if not db_answer or\
            current_user.id != db_answer.user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='invalid comment id')
    answer_crud.delete_answer(db=db, db_answer=db_answer)

@router.post('/upvote', status_code=status.HTTP_204_NO_CONTENT)
def answer_vote(_answer_vote: answer_schema.AnswerVote,
                db: Session = Depends(get_db),
                current_user: User = Depends(get_current_user)):
    if current_user.last_activity is not None and \
            (datetime.now() - current_user.last_activity).seconds <= 3:
        raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                            detail="sending too many requests. wait 3 seconds and retry")
    current_user.last_activity = datetime.now()
    db_answer = answer_crud.get_answer(db, answer_id=_answer_vote.answer_id)
    if not db_answer:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Invalid answer id')
    answer_crud.vote_answer(db, db_answer=db_answer, db_user=current_user)