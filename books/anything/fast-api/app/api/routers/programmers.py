from app.api import cruds
from app.api.dependencies import get_db
from app.api.schemas import ProgrammerDetail, ProgrammerListItem
from fastapi import APIRouter, Depends, HTTPException

router = APIRouter()


@router.get(
    "/",
    response_model=list[ProgrammerListItem],
)
def list_programmers(db=Depends(get_db)):
    return cruds.get_programmers(db)


@router.get(
    "/{name}",
    response_model=ProgrammerDetail,
)
def detail_programmer(name: str):
    # TODO: データの取得
    return ProgrammerDetail(
        name="John Doe",
        languages=["Python", "Java", "JavaScript"],
        twitter_id="my.twitter.id",
    )


@router.post(
    "/",
    responses={
        400: {
            "description": "programmer already exists",
        }
    },
)
def add_programmer(programmer: ProgrammerDetail, db=Depends(get_db)):
    items = cruds.get_programmers(db)
    checker = [it.name == programmer.name for it in items]
    if any(checker):
        raise HTTPException(
            status_code=400,
            detail="programmer already exists",
        )

    cruds.add_programmer(db, programmer)
    return {"result": "OK"}


@router.put("/{name}")
def update_programmer(name: str, programmer: ProgrammerDetail):
    # TODO: データの更新
    return {"result": "OK"}


@router.delete("/{name}")
def delete_programmer(name: str):
    # TODO: データの削除
    return {"name": "OK"}
