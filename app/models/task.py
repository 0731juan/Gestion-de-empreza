class Task:
    def __init__(self, id, description, completed):
        self.id = id
        self.description = description
        self.completed = completed

    def to_dict(self):
        return {
            "id": self.id,
            "description": self.description,
            "completed": self.completed,
        }

    @staticmethod
    def from_dict(data: dict) -> "Task":
        """Create a Task instance from a dictionary."""
        return Task(
            id=data.get("id"),
            description=data.get("description"),
            completed=data.get("completed", False),
        )