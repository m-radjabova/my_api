from fastapi import HTTPException


class StatusService:
    def __init__(self):
        self.statues = ("TODO", "INPROGRESS", "VERIFIED", "DONE")

        self.taskStatues = [
            {
                "id": 1,
                "title": "TODO",
            },
            {
                "id": 2,
                "title": "INPROGRESS",
            },
            {
                "id": 3,
                "title": "VERIFIED",
            },
            {
                "id": 4,
                "title": "DONE",
            },
        ]

    def get_status_type(self):
        return self.statues
    
    def add_task_status(self, status_type: str):
        new_status = {
            "id": len(self.taskStatues) + 1,
            "title": status_type,
        }
        self.taskStatues.append(new_status)
        return new_status

    def get_status_task(self):
        return self.taskStatues

    def delete_status(self, status_id: int):
        for status in self.taskStatues:
            if status["id"] == status_id:
                self.taskStatues.remove(status)
                return status
        return HTTPException(status_code=404, detail="Status not found")
