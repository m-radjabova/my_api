import datetime
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

    def get_task_status(self):
        return self.status_tasks
    
    def get_tasks(self):
        tasks = []
        for status in self.status_tasks:
            tasks.append({
                "status": status,
                "tasks": self.__get_status_tasks(status)
            })
        return tasks

    def __get_status_tasks(self, status):
        return [task for task in self.tasks if task["status"] == status]

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
        return None

    def delete_task(self, task_id: int):
        for i, task in enumerate(self.tasks):
            if task["id"] == task_id:
                del self.tasks[i]
                return True
        return False
