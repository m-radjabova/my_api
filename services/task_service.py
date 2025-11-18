import datetime

from fastapi import HTTPException

from schema.status import StatusType
from schema.task import Task

class TaskService:
    def __init__(self):
        self.priority = ("HIGH", "MEDIUM", "LOW")
        self.tasks = [
            {
                "id": 1,
                "title": "Task 1",
                "description": "Description 1",
                "status": "TODO",
                "assignee": ["Muslima Radjabova", "Daler Ismatov"],
                "priority": ["HIGH"],
                "end_date": "2023-08-01",
                "created_date": "2023-07-01",
            },
            {
                "id": 2,
                "title": "Task 2",
                "description": "Description 2",
                "status": "INPROGRESS",
                "assignee": ["Muslima Radjabova", "Daler Ismatov"],
                "priority": ["MEDIUM"],
                "end_date": "2023-08-01",
                "created_date": "2023-07-01",
            },
            {
                "id": 3,
                "title": "Task 3",
                "description": "Description 3",
                "status": "VERIFIED",
                "assignee": ["Muslima Radjabova", "Daler Ismatov"],
                "priority": ["LOW"],
                "end_date": "2023-08-01",
                "created_date": "2023-07-01",
            },
            {
                "id": 4,
                "title": "Task 4",
                "description": "Description 4",
                "status": "DONE",
                "assignee": ["Muslima Radjabova", "Daler Ismatov"],
                "priority": ["HIGH"],
                "end_date": "2023-08-01",
                "created_date": "2023-07-01",
            },
        ]

    def get_tasks(self):
        return self.tasks
    
    def get_task_priority(self):
        return self.priority


    def add_task(self, task: Task):
        new_task = {
            "id": len(self.tasks) + 1,
            "title": task.title,
            "description": task.description,
            "status": task.status,
            "assignee": task.assignee,
            "priority": task.priority,
            "end_date": task.end_date,
            "created_date": datetime.datetime.now().strftime("%Y-%m-%d"),
        }
        self.tasks.append(new_task)
        return new_task
    
    def get_tasks_by_status(self, status: StatusType):
        return [task for task in self.tasks if task["status"] == status]
    
    def delete_task(self, task_id: int):
        for task in self.tasks:
            if task["id"] == task_id:
                self.tasks.remove(task)
                return task
        raise HTTPException(status_code=404, detail="Task not found")
    
    def update_task(self, task_id: int, task: Task):
        for t in self.tasks:
            if t["id"] == task_id:
                t["title"] = task.title
                t["description"] = task.description
                t["status"] = task.status
                t["assignee"] = task.assignee
                t["priority"] = task.priority
                t["end_date"] = task.end_date
                return t
        raise HTTPException(status_code=404, detail="Task not found")