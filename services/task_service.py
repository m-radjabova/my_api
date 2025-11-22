import datetime
from http.client import HTTPException
from schema.task import RequestTask

class TaskService:
    def __init__(self):
        self.status_tasks = ["TODO", "IN_PROGRESS", "VERIFIED", "DONE"]
        self.tasks = [
            {
                "id": 1,
                "title": "Task 1",
                "description": "Description 1",
                "status": "TODO",
                "assignees": [
                     {
                        "id": 1,
                        "username": "Muslima Radjabova",
                        "email": "muslima@gmail.com",
                    },
                    {
                        "id": 2,
                        "username": "Daler Ismatov",
                        "email": "ismatov@gmail.com",
                    }
                ],
                "priority": "HIGH",
                "end_date": "2023-08-01",
                "created_date": "2023-07-01",
            }
        ]
    
    def get_tasks(self,
              assignee_id: int | None = None,
              priority: str | None = None,
              from_date: str | None = None,
              title: str | None = None,
              ):
        filtered = self.tasks.copy()  

        if assignee_id:
            filtered = [
                t for t in filtered
                if any(a["id"] == assignee_id for a in t["assignees"])
            ]

        if priority and priority != "ALL":
            filtered = [t for t in filtered if t["priority"] == priority]

        if from_date:
            filtered = [
                t for t in filtered
                if t["created_date"] >= from_date
            ]

        if title:
            filtered = [
                t for t in filtered
                if title.lower() in t["title"].lower()
            ]

        return [
            {
                "status": status,
                "tasks": [t for t in filtered if t["status"] == status]
            }
            for status in self.status_tasks
        ]
    
    def get_task_status(self):
        return self.status_tasks

    # def __get_status_tasks(self, status):
    #     return [task for task in self.tasks if task["status"] == status]

    def create_task(self, task_data: RequestTask):
        task_dict = task_data.model_dump()
        task_dict["id"] = len(self.tasks) + 1
        task_dict["created_date"] = datetime.datetime.now().strftime("%Y-%m-%d")
        self.tasks.append(task_dict)
        return task_dict

    def update_task(self, task_id: int, task_data: RequestTask):
        for i, task in enumerate(self.tasks):
            if task["id"] == task_id:
                updated = task_data.model_dump()
                updated["id"] = task_id
                updated["created_date"] = task["created_date"] 
                self.tasks[i] = updated
                return updated

    def delete_task(self, task_id: int):
        for i, task in enumerate(self.tasks):
            if task["id"] == task_id:
                del self.tasks[i]
                return HTTPException(status_code=204, detail="Task deleted successfully")
        return HTTPException(status_code=404, detail="Task not found")
    
    def update_task_status(self, task_id: int, new_status: str):
        for task in self.tasks:
            if task["id"] == task_id:
                task["status"] = new_status
                return task
        return HTTPException(status_code=404, detail="Task not found")