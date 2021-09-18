from json import loads
from src.apps.logging_.models import Log


def related_system_info_field_to_json(logs: Log, offset_logs: list[dict]) -> None:
    for id_, offset_log in enumerate(offset_logs):
            offset_log['system_info'] = loads(logs[id_].system_info.to_json())
