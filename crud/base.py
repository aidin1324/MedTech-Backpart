from sqlalchemy.orm import Session


class BaseCrud:
    def __init__(self, db: Session) -> None:
        self._db = db

    @property
    def connection(self) -> Session:
        return self._db