from app.api import cruds
from app.api.dependencies import get_db
from app.api.schemas import ProgrammerDetail, ProgrammerListItem
from fastapi import APIRouter, Depends

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


@router.post("/")
def add_programmer(programmer: ProgrammerDetail, db=Depends(get_db)):
    print("programmer")
    print(programmer)
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
