##############################################
# book_writing_service.py
from enum import Enum
from typing import Union
from datetime import timedelta

from pydantic import BaseModel


class Success(BaseModel):
    book_title: str
    text: str
    time_to_generate: timedelta


class Failed(BaseModel):
    reason: str


class ResultStatus(str, Enum):
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"


class Result(BaseModel):
    status: ResultStatus
    worker_name: str
    data: Union[Success, Failed]


class BookWritingService:
    def write_book(self, book_title: str) -> Result:
        if book_title:
            # ...do complicated stuff here
            return Result(
                status=ResultStatus.SUCCESS,
                worker_name="worker01",
                data=Success(
                    book_title=book_title,
                    text=f"Once there was a {book_title}. THE END",
                    time_to_generate=0,
                ),
            )

        else:
            return Result(
                status=ResultStatus.FAILED,
                worker_name="worker01",
                data=Failed(public_reason="Empty book title"),
            )
