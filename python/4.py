from enum import Enum
from typing import Dict, List, NamedTuple, Optional, Tuple
import re

class Timestamp(NamedTuple):
    year: int
    mont: int
    day: int
    hour: int
    minute: int


class Action(Enum):
    StartShift = 0
    WakeUp = 1
    FallAsleep = 2

    @staticmethod
    def from_string(raw: str) -> 'Action':
        if raw == 'falls asleep':
            return Action.FallAsleep
        elif raw == 'wakes up':
            return Action.WakeUp
        else:
            return Action.StartShift


class Record(NamedTuple):
    timestamp: Timestamp
    action: Action
    guard: Optional[int]


line_parse_regex = re.compile(r'\[([\d]+)-([\d]+)-([\d]+) ([\d]+):([\d]+)\] (falls asleep|wakes up|Guard #([\d]+) begins shift)')


def parse_line(line: str) -> Record:
    match = line_parse_regex.match(line)
    if match is None:
        raise Exception(f"Invalid line: {line}")
    year, month, day, hour, minute, raw_action, raw_guard = match.groups()
    timestamp = Timestamp(int(year), int(month), int(day), int(hour), int(minute))
    action = Action.from_string(raw_action)
    guard = int(raw_guard) if raw_guard is not None else None
    return Record(timestamp, action, guard)


def load_records() -> List[Record]:
    records = []
    with open('../input/4') as f:
        for line in f:
            records.append(parse_line(line))
    return sorted(records)


class GuardSleepLog:
    def __init__(self, guard_id: int):
        self.id: int = guard_id
        self.times: Dict[int, int] = {}
        for minute in range(0, 60):
            self.times[minute] = 0

    def record_sleep(self, start: int, stop: int) -> None:
        for minute in range(start, stop):
            self.times[minute] += 1

    def total_sleep_time(self) -> int:
        return sum(self.times.values())

    def highest_frequency(self) -> int:
        return self.times[self.most_frequent_minute()]

    def most_frequent_minute(self) -> int:
        return max(self.times, key=lambda x: self.times[x])


def both_parts() -> Tuple[str, str]:
    records = load_records()
    if records[0].guard is None:
        raise Exception("Invalid records, doesn't start with new shift")

    guards: Dict[int, GuardSleepLog] = {}

    current_guard: int = records[0].guard
    start: int = 0
    for record in records:
        if record.guard is not None:
            current_guard = record.guard
        elif record.action == Action.FallAsleep:
            start = record.timestamp.minute
        else:
            if current_guard not in guards:
                guards[current_guard] = GuardSleepLog(current_guard)
            stop = record.timestamp.minute
            guards[current_guard].record_sleep(start, stop)

    sleepiest_id = max(guards, key=lambda g: guards[g].total_sleep_time())
    sleepiest = guards[sleepiest_id]
    part_1 = sleepiest_id * sleepiest.most_frequent_minute()

    consistent_id = max(guards, key=lambda g: guards[g].highest_frequency())
    consistent = guards[consistent_id]
    part_2 = consistent_id * consistent.most_frequent_minute()

    return (f'{part_1}', f'{part_2}')


if __name__ == '__main__':
    part_1, part_2 = both_parts()
    print(f'Part 1: {part_1}')
    print(f'Part 2: {part_2}')
