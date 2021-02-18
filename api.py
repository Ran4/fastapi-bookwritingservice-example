##############################################
# BookWritingService API
from enum import Enum
from typing import Union, cast

from fastapi import FastAPI
from pydantic import BaseModel

import book_writing


app = FastAPI()


class BookWritingIn(BaseModel):
    book_title: str


class BookWritingSuccessOut(BaseModel):
    book_title: str
    text: str

class BookWritingFailedOut(BaseModel):
    reason: str

class BookWritingResultOut(BaseModel):
    """
    Like book_writing.Result, but doesn't contain worker_name
    """
    status: book_writing.ResultStatus
    data: Union[BookWritingSuccessOut, BookWritingFailedOut]


book_writing_service = book_writing.BookWritingService()


@app.post("/write-book")
async def write_book(book_writing_in: BookWritingIn):
    result: book_writing.Result = book_writing_service.write_book(
        book_title=book_writing_in.book_title,
    )

    if result.status == book_writing.ResultStatus.SUCCESS:
        success = cast(book_writing.Success, result.data)
        data = BookWritingSuccessOut(
            book_title=success.book_title,
            text=success.text,
        )

    elif result.status == book_writing.ResultStatus.FAILED:
        failed = cast(book_writing.Failed, result.data)
        data = BookWritingFailedOut(
            reason=failed.reason,
        )

    else:
        raise Exception(f"Unhandled result arm {result.status}")

    return BookWritingResultOut(
        status=result.status,
        data=data,
    )
