from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from database import get_db
from domain.question import question_schema, question_crud
from domain.user.user_router import get_current_user
from models import User

router = APIRouter(
    prefix="/api/question",
)

@router.get("/list", response_model=question_schema.QuestionList)
def question_list(db: Session = Depends(get_db),
                page: int = 0, size: int = 10, keyword: str = ''):
    total, _question_list = question_crud.get_question_list(db, 
                                                    skip=page*size,
                                                    limit=size,
                                                    keyword=keyword)
    return {
        'total': total,
        'question_list': _question_list
    }

@router.get("/detail/{question_id}", response_model=question_schema.Question)
def question_detail(question_id: int, db: Session = Depends(get_db)):
    question = question_crud.get_question(db, question_id=question_id)
    return question

@router.post("/create", status_code=status.HTTP_204_NO_CONTENT)
def question_create(_question_create:question_schema.QuestionCreate,
                    db: Session = Depends(get_db),
                    current_user: User = Depends(get_current_user)):
    if current_user.last_activity is not None and \
            (datetime.now() - current_user.last_activity).seconds <= 3:
        raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                            detail="sending too many requests. wait 3 seconds and retry")
    current_user.last_activity = datetime.now()
    question_crud.create_question(db=db, 
                                question_create=_question_create,
                                user=current_user)    

@router.put('/update', status_code=status.HTTP_204_NO_CONTENT)
def question_update(_question_update: question_schema.QuestionUpdate,
                    db: Session = Depends(get_db),
                    current_user: User = Depends(get_current_user)):
    if current_user.last_activity is not None and \
            (datetime.now() - current_user.last_activity).seconds <= 3:
        raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                            detail="sending too many requests. wait 3 seconds and retry")
    current_user.last_activity = datetime.now()
    db_question = question_crud.get_question(db, question_id=_question_update.question_id)
    if not db_question or current_user.id != db_question.user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Invalid id")
    
    question_crud.update_question(db=db,
                                db_question=db_question,
                                question_update=_question_update)

@router.delete('/delete', status_code=status.HTTP_204_NO_CONTENT)
def question_delete(_question_delete: question_schema.QuestionDelete,
                    db: Session = Depends(get_db),
                    current_user: User = Depends(get_current_user)):
    if current_user.last_activity is not None and \
            (datetime.now() - current_user.last_activity).seconds <= 3:
        raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                            detail="sending too many requests. wait 3 seconds and retry")
    current_user.last_activity = datetime.now()
    db_question = question_crud.get_question(db, question_id=_question_delete.question_id)
    if not db_question or current_user.id != db_question.user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Invalid id')
    question_crud.delete_question(db=db, db_question=db_question)

@router.post('/upvote', status_code=status.HTTP_204_NO_CONTENT)
def question_vote(_question_vote: question_schema.QuestionVote,
                db: Session = Depends(get_db),
                current_user: User = Depends(get_current_user)):
    if current_user.last_activity is not None and \
            (datetime.now() - current_user.last_activity).seconds <= 3:
        raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                            detail="sending too many requests. wait 3 seconds and retry")
    current_user.last_activity = datetime.now()
    db_question = question_crud.get_question(db, question_id=_question_vote.question_id)
    if not db_question:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Invalid question id')
    question_crud.vote_question(db, db_question=db_question, db_user=current_user)