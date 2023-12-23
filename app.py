from flask import Flask, render_template, request, jsonify

app = Flask(__name__, static_url_path='/static')

class Task:
    def __init__(self, id, title, description, completed):
        self.id = id
        self.title = title
        self.description = description
        self.completed = completed

tasks = []
    
@app.route('/')
def index():
    return render_template('index.html', tasks=tasks)

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': tasks})

@app.route('/api/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = next((task for task in tasks if task.id == task_id), None)
    if task is None:
        return jsonify({'error': 'Task not found'}), 404
    return jsonify({'task': task.__dict__})

@app.route('/api/tasks', methods=['POST'])
def create_task():
    if not request.json or 'title' not in request.json:
        return jsonify({'error': 'Title is required'}), 400

    task_data = {
        'id': len(tasks) + 1,
        'title': request.json['title'],
        'description': request.json.get('description', ''),
        'completed': False
    }

    tasks.append(Task(**task_data))
    return jsonify({'task': task_data}), 201

@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = next((task for task in tasks if task.id == task_id), None)
    if task is None:
        return jsonify({'error': 'Task not found'}), 404

    task.title = request.json.get('title', task.title)
    task.description = request.json.get('description', task.description)
    task.completed = request.json.get('completed', task.completed)

    return jsonify({'task': task.__dict__})

@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    global tasks
    tasks = [task for task in tasks if task.id != task_id]
    return jsonify({'result': True})


if __name__ == '__main__':
    app.run(debug=True)