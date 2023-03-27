import os
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, UploadFile
from sqlalchemy.orm import Session
from starlette import status

from database import get_db
from domain.answer import answer_schema, answer_crud
from domain.question import question_crud
from domain.chall import chall_crud, chall_schema
from domain.user import user_crud
from domain.user.user_router import get_current_user
from models import User

import tensorflow as tf
import torch

UPLOAD_DIR = "uploads/"
try:
    os.mkdir(UPLOAD_DIR)
except:
    pass

router = APIRouter(
    prefix="/api/chall"
)

@router.post('/upload/{category}', status_code=status.HTTP_204_NO_CONTENT)
def handle_upload(category: str,
                file: UploadFile,
                user: User = Depends(get_current_user),
                db:Session = Depends(get_db)):
    if not ('classification' == category.lower() or \
        'gan' == category.lower()):
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                            detail='Only submissions for classifcation and gan are allowed')
    if user.last_activity is not None and \
            (datetime.now() - user.last_activity).seconds <= 3:
        raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                            detail="sending too many requests. wait 3 seconds and retry")
    # delete existing submission
    chall_crud.delete_chall_by_category(db=db, user=user, category=category)

    file_signature = file.file.read(4)
    file.file.seek(0)

    saved_name = os.urandom(16).hex()
    if file_signature == '\x89HDF':
        saved_name += '.h5'

    failed = False
    failed_reason = ''

    with open(UPLOAD_DIR + saved_name, "wb") as f:
        file_data = file.file.read()
        file_size = len(file_data)
        f.write(file_data)

    if saved_name[-3:] == '.h5':
        try:
            model = tf.keras.models.load_model(UPLOAD_DIR+saved_name)
            model_shape = model.input_shape[-3:]
            if model_shape != (299, 299, 3):
                failed = True
                failed_reason = f'Input shape must be (299, 299, 3). You provided {model_shape}'
        except:
            failed = True
            failed_reason = f'Failed to load model. https://www.tensorflow.org/tutorials/keras/save_and_load#hdf5_format'
    else:
        try:
            model = torch.load(UPLOAD_DIR+saved_name)
            # it seems there is no method to get shape of an input layer, so just skipping check.
        except Exception as e:
            failed = True
            failed_reason = f'Failed to load model. https://pytorch.org/tutorials/beginner/saving_loading_models.html#save-load-entire-model'
            # process failed torch model and raise
    try:
        os.remove(UPLOAD_DIR + saved_name) # I will not actually run inferences.
    except:
        pass
    # validation done. save chal in DB
    chall_crud.create_chall(db=db,
                            source=os.urandom(4).hex(), # source acts like a "key" in FilePond
                            user=user,
                            file_name=file.filename,
                            file_size=file_size,
                            category=category,
                            failed=failed,
                            failed_reason=failed_reason)

    user_crud.add_participation(db=db,
                                user=user,
                                category=category)

@router.delete('/cancel/{category}', status_code=status.HTTP_204_NO_CONTENT)
def handle_delete(category: str,
                user: User = Depends(get_current_user),
                db: Session = Depends(get_db)):
    if user.last_activity is not None and \
            (datetime.now() - user.last_activity).seconds <= 3:
        raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                            detail="sending too many requests. wait 3 seconds and retry")
    chall_crud.delete_chall_by_category(db=db, user=user, category=category)
    user_crud.delete_participation(db=db, user=user, category=category)

@router.get('/progress/{category}')
def get_progress(category: str,
                db: Session = Depends(get_db),
                user: User = Depends(get_current_user)):
    chall = chall_crud.get_chall_by_category(db=db, user=user, category=category)
    if not chall:
        raise HTTPException(status_code=status.HTTP_428_PRECONDITION_REQUIRED,
                            detail="Model not submitted yet.")
    if chall.failed:
        raise HTTPException(status_code=status.HTTP_417_EXPECTATION_FAILED,
                            detail=chall.reason)

    return {
        'detail': "Model submitted successfully and validated. Actual evaluation will be done after LINE CTF 2023 ends."
    }

@router.get('/get/{category}', response_model=chall_schema.UploadedModel)
def get_uploaded(category: str,
                db: Session = Depends(get_db),
                user: User = Depends(get_current_user)):
    if user.last_activity is not None and \
            (datetime.now() - user.last_activity).seconds <= 3:
        raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                            detail="sending too many requests. wait 3 seconds and retry")
    chall = chall_crud.get_chall_by_category(db=db, user=user, category=category)
    if not chall:
        raise HTTPException(status_code=status.HTTP_428_PRECONDITION_REQUIRED,
                            detail="Model not submitted yet")
    return {
        'source': chall.source,
        'file_name': chall.file_name,
        'file_size': chall.file_size
    }
