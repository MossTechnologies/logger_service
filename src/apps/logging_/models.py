import json

from mongoengine import (
    Document,
    StringField,
    DictField,
    ReferenceField,
    IntField,
    CASCADE
)


class SystemInfo(Document):
    os = StringField(max_length=10)
    nodename = StringField(max_length=100)
    release = StringField(max_length=300)
    version = StringField(max_length=300)

    system_bits = StringField(max_length=10)
    cpu_usage = IntField()
    ram_usage = IntField()

    memory_total = IntField()
    memory_used = IntField()


class Project(Document):
    id_ = IntField(unique=True)
    client_name = StringField(max_length=250)
    name = StringField(max_length=250)


class Log(Document):
    id_ = IntField()
    project = ReferenceField(Project)
    log = DictField()
    system_info = ReferenceField(SystemInfo, reverse_delete_rule=CASCADE)
