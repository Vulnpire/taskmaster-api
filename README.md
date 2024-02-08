## Overview

The Flask TODO API provides endpoints to manage tasks. It supports creating, reading, updating, and deleting tasks. Each task has an ID, creation timestamp, task description, and completion status.

## Installation
```
pip3 install -r requirements.txt
```
## Run the application
```
FLASK_APP=app:server flask run --reload
```

## Usage
Endpoints

    GET /todo/tasks: Get a list of tasks.
    POST /todo/tasks: Create a new task.
    GET /todo/tasks/{task_id}: Get details of a specific task.
    PUT /todo/tasks/{task_id}: Update details of a specific task.
    DELETE /todo/tasks/{task_id}: Delete a specific task.

# Get a list of tasks

```
curl -X GET http://localhost:5000/todo/tasks
```

# Create a new task

```
curl -X POST -H "Content-Type: application/json" -d '{"task": "Your task description here"}' http://localhost:5000/todo/tasks
```

# Get details of a specific task

```
curl -X GET http://localhost:5000/todo/tasks/{task_id}
```

# Update details of a specific task

```
curl -X PUT -H "Content-Type: application/json" -d '{"task": "Updated task description", "completed": true}' http://localhost:5000/todo/tasks/{task_id}
```

# Delete a specific task

```
curl -X DELETE http://localhost:5000/todo/tasks/{task_id}
```

Replace {task_id} with the actual ID of the task you want to interact with.
