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


def read_tasks(filename: str) -> List[Task]:
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
            point = 1.0+random.random()*0.2 if len(row) == 6 else float(row[6])
            tasks.append(Task(id, row[1], row[2:6], point))
    return tasks


def query(tasks: List[Task]):
    task = tasks[0]
    print(task.statement)
    ord = list(range(4))
    random.shuffle(ord)
    for i, j in enumerate(ord):
        print(f'{i+1}.{task.choice[j]}  ', end='')
    ans = int(input('\n答えは? ')) - 1
    correct = ord[ans] == 0
    result = '正解' if correct else '不正解'
    enough = False
    if correct:
        enough = task.point == 5.0
        task.point += 1.0
        task.point = min(5.0, task.point)
    else:
        task.point *= 0.5
    print(f'{result} (問題番号: {task.id}, 正答: {ord.index(0)+1})')
    if enough:
        print(f'もう学習は十分なように思いますが……')
    print('')
    heapq.heappop(tasks)
    heapq.heappush(tasks, task)


def save_tasks(filename: str, tasks: List[Task]):
    with open(filename, mode='w') as tasks_file:
        for task in tasks:
            print(task.id, task.statement,
                  *task.choice, task.point, sep='\t', file=tasks_file)


if __name__ == '__main__':
    tasks = read_tasks(sys.argv[1])
    heapq.heapify(tasks)
    try:
        while True:
            query(tasks)
    except KeyboardInterrupt:
        save_tasks(sys.argv[1], tasks)
        print('\n進捗をセーブしました！')
