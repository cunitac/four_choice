import csv
import random
import sys
import heapq
from typing import *


class Task:
    def __init__(self, id: int, statement: str, choice: List[str], point: float):
        self.id = id
        self.point = point
        self.statement = statement
        self.choice = choice

    def __lt__(self, rhs):
        return self.point < rhs.point


def read_tasks(filename: str, reset: bool) -> List[Task]:
    ids = set()
    tasks = list()
    with open(filename) as tasks_file:
        tasks_file = csv.reader(tasks_file, delimiter='\t')
        for row_n, row in enumerate(tasks_file):
            id = int(row[0])
            if id in ids:
                print(f'重複した問題番号: {id} (第{row_n+1}行)')
                exit(1)
            ids.add(id)
            point = 0.0 if reset or len(row) == 6 else float(row[6])
            tasks.append(Task(id, row[1], row[2:6], point))
    if reset:
        print('進捗をリセットしました！')
    return tasks


def query(tasks: List[Task]):
    task = tasks[0]
    print(task.statement)
    ord = list(range(4))
    random.shuffle(ord)
    for i, j in enumerate(ord):
        print(f'{i+1}.{task.choice[j]}  ', end='')
    try:
        ans = int(input('\n答えは? ')) - 1
        correct = ord[ans] == 0
    except ValueError:
        correct = False
    result = '\033[32m\033[1mAC\033[0m' if correct else '\033[31m\033[1mWA\u001b[0m'
    prev_point = task.point
    task.point *= 0.584804
    task.point += (int(correct) + 1) * 50 / 2.408501
    print(
        f'{result} 問題番号: {task.id}, 正答: {ord.index(0)+1}.{task.choice[0]}, スコア: {prev_point:.01f} -> {task.point:.01f}')
    print('')
    heapq.heappop(tasks)
    heapq.heappush(tasks, task)


def save_tasks(filename: str, tasks: List[Task]):
    with open(filename, mode='w') as tasks_file:
        tasks.sort(key=lambda task: task.id)
        for task in tasks:
            print(task.id, task.statement,
                  *task.choice, task.point, sep='\t', file=tasks_file)


if __name__ == '__main__':
    reset, shuffle = False, False
    if len(sys.argv) == 3:
        if sys.argv[2] == '--reset':
            reset = True
        elif sys.argv[2] == '--shuffle':
            shuffle = True
        else:
            raise 'Unknown Option'
    else:
        assert len(sys.argv) == 2
    tasks = read_tasks(sys.argv[1], reset)
    if shuffle:
        print('シャッフルしました！')
        random.shuffle(tasks)
    heapq.heapify(tasks)
    try:
        while True:
            query(tasks)
    except KeyboardInterrupt:
        pass
    finally:
        save_tasks(sys.argv[1], tasks)
        print('\n進捗をセーブしました！')
