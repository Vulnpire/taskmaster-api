from flask import Flask, abort
from flask_smorest import Api, Blueprint
from marshmallow import Schema, fields
from datetime import datetime, timezone
import uuid
import enum
import unittest
from flask.testing import FlaskClient
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask.views import MethodView
from marshmallow_enum import EnumField

server = Flask(__name__)

# Configuration settings for API
class APIConfig:
    API_TITLE = "TODO API"
    API_VERSION = "v1"
    OPENAPI_VERSION = "3.0.3"
    OPENAPI_URL_PREFIX = "/"
    OPENAPI_SWAGGER_UI_PATH = "/docs"
    OPENAPI_SWAGGER_UI_URL = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    OPENAPI_REDOC_PATH = "/redoc"
    OPENAPI_REDOC_UI_URL = "https://cdn.jsdelivr.net/npm/redoc@next/bundles/redoc.standalone.js"

server.config.from_object(APIConfig)
api = Api(server)
todo = Blueprint("todo", "todo", url_prefix="/todo", description="TODO API")

# Sample tasks data
tasks = [
    {
        "id": uuid.UUID("ebe0bf6c-4bd2-406a-8aa1-52fddae5dc07"),
        "created": datetime.now(timezone.utc),
        "completed": False,
        "task": "Create Flask API",
    }
]

# Schema for creating a task
class CreateTask(Schema):
    task = fields.String()

# Schema for updating a task
class UpdateTask(CreateTask):
    completed = fields.Bool()

# Schema for representing a task
class Task(UpdateTask):
    id = fields.UUID()
    created = fields.DateTime()

# Schema for representing a list of tasks
class ListTasks(Schema):
    tasks = fields.List(fields.Nested(Task))

# Enumeration for sorting criteria
class SortByEnum(enum.Enum):
    task = "task"
    created = "created"

# Enumeration for sorting direction
class SortDirectionEnum(enum.Enum):
    asc = "asc"
    desc = "desc"

# Schema for query parameters when listing tasks
class ListTasksParameters(Schema):
    order_by = EnumField(SortByEnum, load_default=SortByEnum.created)
    order = EnumField(SortDirectionEnum, load_default=SortDirectionEnum.asc)

# Define endpoint for managing tasks
@todo.route("/tasks")
class TodoCollection(MethodView):
    """Endpoint for managing tasks."""

    # Define GET method to retrieve list of tasks
    @todo.arguments(ListTasksParameters, location="query")
    @todo.response(status_code=200, schema=ListTasks)
    def get(self, parameters):
        """Get a list of tasks."""
        return {
            "tasks": sorted(
                tasks,
                key=lambda task: task[parameters["order_by"].value],
                reverse=parameters["order"] == SortDirectionEnum.desc
            )
        }

    # Define POST method to create a new task
    @todo.arguments(CreateTask)
    @todo.response(status_code=201, schema=Task)
    def post(self, task):
        """Create a new task."""
        task["id"] = uuid.uuid4()
        task["created"] = datetime.now(timezone.utc)
        task["completed"] = False
        tasks.append(task)
        return task

# Define endpoint for managing individual tasks
@todo.route("/tasks/<uuid:task_id>")
class TodoTask(MethodView):
    """Endpoint for managing individual tasks."""

    # Define GET method to retrieve details of a specific task
    @todo.response(status_code=200, schema=Task)
    def get(self, task_id):
        """Get details of a specific task."""
        for task in tasks:
            if task["id"] == task_id:
                return task
        abort(404, f"Task with ID {task_id} not found")

    # Define PUT method to update details of a specific task
    @todo.arguments(UpdateTask)
    @todo.response(status_code=200, schema=Task)
    def put(self, payload, task_id):
        """Update details of a specific task."""
        for task in tasks:
            if task["id"] == task_id:
                task["completed"] = payload["completed"]
                task["task"] = payload["task"]
                return task
        abort(404, f"Task with ID {task_id} not found")

    # Define DELETE method to delete a specific task
    @todo.response(status_code=204)
    def delete(self, task_id):
        """Delete a specific task."""
        for index, task in enumerate(tasks):
            if task["id"] == task_id:
                tasks.pop(index)
                return
        abort(404, f"Task with ID {task_id} not found")

api.register_blueprint(todo)

if __name__ == "__main__":
    server.run(debug=True)
