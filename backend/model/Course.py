from main import db


class Course(db.Model):
    tablename = "course"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    description = db.Column(db.String())
    is_retired = db.Column(db.Boolean, default=False, nullable=False)

    def __init__(
        self,
        id: int,
        name: str,
        description: str,
        is_retired: bool = False,
    ):
        self.id = id
        self.name = name
        self.description = description
        self.is_retired = is_retired

    def __repr__(self):
        return "<id: {}, name: {}, description: {}, is retired: {}>".format(
            self.id, self.name, self.description, self.is_retired
        )

    def to_dict(self):
        columns = self.__mapper__.column_attrs.keys()
        result = {}
        for column in columns:
            result[column] = getattr(self, column)
        return result
