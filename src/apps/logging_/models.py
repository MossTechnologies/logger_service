from mongoengine import (
    Document,
    StringField,
    DictField,
    ReferenceField,
    IntField,
)


class Project(Document):
    id_ = IntField(unique=True)
    client_name = StringField(max_length=250)
    name = StringField(max_length=250)


class Log(Document):
    id_ = IntField()
    project = ReferenceField(Project)
    log = DictField()