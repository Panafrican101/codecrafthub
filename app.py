# app.py
# A simple Flask REST API for CodeCraftHub
# - Stores data in a JSON file (courses.json)
# - CRUD operations for courses
# - No authentication, beginner-friendly with comments

from flask import Flask, request, jsonify
import json
import os
import datetime

# Initialize Flask app
app = Flask(__name__)

# Path to JSON data file
DATA_FILE = 'courses.json'
# Allowed statuses
ALLOWED_STATUSES = {"Not Started", "In Progress", "Completed"}

# Ensure the data file exists; if not, create an empty list []
def ensure_data_file():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'w') as f:
            json.dump([], f)

# Read all courses from the JSON file
def read_courses():
    with open(DATA_FILE, 'r') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            # If the file is corrupted, treat as empty
            return []

# Write the list of courses back to the JSON file
def write_courses(courses):
    with open(DATA_FILE, 'w') as f:
        json.dump(courses, f, indent=2)

# Compute the next auto-generated id (1-based)
def next_id(courses):
    if not courses:
        return 1
    return max(item['id'] for item in courses) + 1

# Validate date string format: YYYY-MM-DD
def validate_date(date_str):
    try:
        datetime.datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except (ValueError, TypeError):
        return False

# Validate payload for create/update
# - require_id is True for update
def validate_course_payload(payload, require_id=False):
    errors = []

    if not isinstance(payload, dict):
        errors.append("Invalid JSON payload")
        return False, errors

    if require_id:
        if 'id' not in payload:
            errors.append("Missing field: id")
        elif not isinstance(payload['id'], int) or payload['id'] <= 0:
            errors.append("Invalid id")

    # Required fields for both create and update
    required_fields = ['name', 'description', 'target_date', 'status']
    for field in required_fields:
        if field not in payload:
            errors.append(f"Missing field: {field}")

    # Validate name/description non-empty when provided
    if 'name' in payload and (payload['name'] is None or payload['name'] == ''):
        errors.append("Name cannot be empty")
    if 'description' in payload and (payload['description'] is None or payload['description'] == ''):
        errors.append("Description cannot be empty")

    # Validate target_date format
    if 'target_date' in payload:
        if not validate_date(payload['target_date']):
            errors.append("Invalid date format for target_date, expected YYYY-MM-DD")

    # Validate status value
    if 'status' in payload:
        if payload['status'] not in ALLOWED_STATUSES:
            errors.append(f"Invalid status. Allowed: {', '.join(ALLOWED_STATUSES)}")

    if errors:
        return False, errors
    return True, None

# Ensure the data file exists when the module is loaded
ensure_data_file()

#Create a Homepage
@app.route('/')
def home():
       return  """
       <html>
            <head>
                    <style>
                        body { background: #0f172a; color: #38bdf8; font-family; sans-serif; text-align: center; padding-top: 20vh; }
                        h1 {font-size: 3rem; margin-bottom: 0.5rem; }
                        p { color: #94a3b8; font-size: 1.2rem; }
                     </style>
            </head>
        <body>
                     <body><h1>Course API is Online</h1>
                     <p>This backend is up and running smoothly. Head over to <a href="/api/courses" style="color: #38bdf8;">/courses</a> to view the data.</p>
        </body>
    </html>
    """
                
# 1) Create a new course
@app.route('/api/courses', methods=['POST'])
def create_course():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({"error": "Invalid JSON payload"}), 400

    valid, errors = validate_course_payload(data, require_id=False)
    if not valid:
        return jsonify({"error": "Validation failed", "details": errors}), 400

    courses = read_courses()
    new_id = next_id(courses)

    course = {
        "id": new_id,
        "name": data['name'],
        "description": data['description'],
        "target_date": data['target_date'],
        "status": data['status'],
        "created_at": datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
    }

    courses.append(course)

    try:
        write_courses(courses)
    except Exception as e:
        return jsonify({"error": "Unable to write data to file", "detail": str(e)}), 500

    return jsonify(course), 201

# 2) Get all courses
@app.route('/api/courses', methods=['GET'])
def get_all_courses():
    try:
        courses = read_courses()
    except Exception as e:
        return jsonify({"error": "Unable to read data file", "detail": str(e)}), 500
    return jsonify(courses), 200

# 3) Get a specific course by id
@app.route('/api/courses/<int:course_id>', methods=['GET'])
def get_course(course_id):
    courses = read_courses()
    course = next((c for c in courses if c['id'] == course_id), None)
    if not course:
        return jsonify({"error": "Course not found"}), 404
    return jsonify(course), 200

# 4) Update a course
@app.route('/api/courses', methods=['PUT'])
@app.route('/api/courses/<int:course_id>', methods=['PUT'])
def update_course(course_id=None):
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({"error": "Invalid JSON payload"}), 400

    target_id = course_id if course_id is not None else data.get('id')
    if target_id is None:
        return jsonify({"error": "Missing field: id"}), 400

    data['id'] = target_id

    valid, errors = validate_course_payload(data, require_id=True)
    if not valid:
        return jsonify({"error": "Validation failed", "details": errors}), 400

    courses = read_courses()
    course = next((c for c in courses if c['id'] == data['id']), None)
    if not course:
        return jsonify({"error": "Course not found"}), 404

    # Update fields
    course['name'] = data['name']
    course['description'] = data['description']
    course['target_date'] = data['target_date']
    course['status'] = data['status']

    try:
        write_courses(courses)
    except Exception as e:
        return jsonify({"error": "Unable to write data to file", "detail": str(e)}), 500

    return jsonify(course), 200

# 5) Delete a course
@app.route('/api/courses', methods=['DELETE'])
@app.route('/api/courses/<int:course_id>', methods=['DELETE'])
def delete_course(course_id=None):
    data = request.get_json(silent=True)

    target_id = course_id
    if target_id is None:
        if not isinstance(data, dict) or 'id' not in data:
            return jsonify({"error": "Missing field: id"}), 400
        target_id = data['id']

    if not isinstance(target_id, int) or target_id <= 0:
        return jsonify({"error": "Invalid id"}), 400

    courses = read_courses()
    index = next((i for i, c in enumerate(courses) if c['id'] == target_id), None)
    if index is None:
        return jsonify({"error": "Course not found"}), 404

    courses.pop(index)

    try:
        write_courses(courses)
    except Exception as e:
        return jsonify({"error": "Unable to write data to file", "detail": str(e)}), 500

    return jsonify({"message": "Course deleted", "id": target_id}), 200

# Run the app
if __name__ == '__main__':
    app.run(debug=True)