CodeCraftHub - Simple REST API Learning with Flask and JSON Storage

CodeCraftHub is a beginner-friendly project to learn REST API basics using Python and Flask. It stores course data in a simple JSON file (no database). You can create, read, update, and delete courses, each with a name, description, target date, and status.

    No authentication or user management
    All data stored in a JSON file (courses.json)
    Auto-generated IDs
    Created_at timestamp for each course
    Clear error handling for common issues

1) Project overview and description

CodeCraftHub provides a tiny, easy-to-understand REST API to manage a list of courses developers want to learn. It demonstrates:

    How to design CRUD endpoints (Create, Read, Update, Delete)
    How to store data in a JSON file instead of a database
    How to validate input (required fields, date format, allowed statuses)
    How to return meaningful JSON responses and HTTP status codes

API endpoints are designed to be simple for beginners to experiment with REST concepts.
2) Features

    CRUD endpoints for courses
    Data persisted in a JSON file named

    courses.json

    Auto-incrementing id starting from 1
    Fields per course:
        id (int, auto-generated)
        name (string, required)
        description (string, required)
        target_date (YYYY-MM-DD, string, required)
        status (one of: "Not Started", "In Progress", "Completed")
        created_at (UTC timestamp, auto-generated)
    Basic error handling:
        Missing required fields
        Course not found
        Invalid status values
        File read/write errors
    Beginner-friendly code with helpful comments
    Automatic creation of

    courses.json

    if it doesn’t exist

3) Installation instructions (step-by-step)

Prerequisites:

    Python 3.8+ (tested with Python 3.x)
    pip (comes with Python)

Step-by-step guide (Linux/macOS/Windows):

    Create a project directory

    mkdir CodeCraftHub
    cd CodeCraftHub

    (Optional but recommended) Create a virtual environment

    Python 3.x users:
        python -m venv venv
        On macOS/Linux: source venv/bin/activate
        On Windows: venv\Scripts\activate

    Install Flask

    pip install Flask

    Add the application code

    Create a file named app.py in the project root and paste the complete code from the provided example (the Flask REST API with JSON file storage).

    Run the application

    python app.py
    The server will start on http://127.0.0.1:5000 by default

Notes:

    The app will create courses.json automatically if it doesn’t exist.
    You don’t need to create the file manually unless you want to pre-populate data.

4) How to run the application

    Start the server:
        python app.py
    Open in your browser or test with curl:
        http://127.0.0.1:5000/api/courses
        Specific course: http://127.0.0.1:5000/api/courses/1

5) API endpoints documentation with examples

Base URL: http://127.0.0.1:5000

    POST /api/courses

    Purpose: Add a new course

    Required fields in JSON body: name, description, target_date (YYYY-MM-DD), status

    Status codes: 201 Created on success, 400 for validation errors

    Example request: curl -s -X POST
    -H "Content-Type: application/json"
    -d '{"name":"Intro to Python","description":"Learn Python basics","target_date":"2026-08-30","status":"Not Started"}'
    http://127.0.0.1:5000/api/courses

    Example response (on success): { "id": 1, "name": "Intro to Python", "description": "Learn Python basics", "target_date": "2026-08-30", "status": "Not Started", "created_at": "2026-07-22T12:34:56Z" }

    GET /api/courses

    Purpose: Get all courses

    Status codes: 200 OK

    Example request: curl -s http://127.0.0.1:5000/api/courses

    Example response (array of courses): [ { "id": 1, "name": "Intro to Python", "description": "Learn Python basics", "target_date": "2026-08-30", "status": "Not Started", "created_at": "2026-07-22T12:34:56Z" }, ... ]

    GET /api/courses/<id>

    Purpose: Get a specific course by id

    Status codes: 200 OK if found, 404 if not found

    Example request: curl -s http://127.0.0.1:5000/api/courses/1

    Example response (on success): { "id": 1, "name": "Intro to Python", "description": "Learn Python basics", "target_date": "2026-08-30", "status": "Not Started", "created_at": "2026-07-22T12:34:56Z" }

    Non-existent course (example): curl -s http://127.0.0.1:5000/api/courses/999
        Response: {"error": "Course not found"} with HTTP 404

    PUT /api/courses

    Purpose: Update a course

    Required fields in JSON body: id, name, description, target_date, status

    Status codes: 200 OK on success, 400 for validation errors, 404 if course not found

    Example request: curl -s -X PUT
    -H "Content-Type: application/json"
    -d '{"id":1,"name":"Intro to Python","description":"Learn Python basics and syntax","target_date":"2026-09-15","status":"In Progress"}'
    http://127.0.0.1:5000/api/courses

    Example response (on success): { "id": 1, "name": "Intro to Python", "description": "Learn Python basics and syntax", "target_date": "2026-09-15", "status": "In Progress", "created_at": "2026-07-22T12:34:56Z" }

    Update non-existent id: curl -s -X PUT
    -H "Content-Type: application/json"
    -d '{"id":999,"name":"X","description":"Y","target_date":"2026-12-31","status":"Not Started"}'
    http://127.0.0.1:5000/api/courses
        Response: {"error": "Course not found"} with HTTP 404

    DELETE /api/courses

    Purpose: Delete a course

    Required field in body: id

    Status codes: 200 OK on success, 400 for validation errors, 404 if course not found

    Example request: curl -s -X DELETE
    -H "Content-Type: application/json"
    -d '{"id":1}'
    http://127.0.0.1:5000/api/courses

    Example response (on success): {"message":"Course deleted","id":1}

    Delete non-existent id: curl -s -X DELETE
    -H "Content-Type: application/json"
    -d '{"id":999}'
    http://127.0.0.1:5000/api/courses
        Response: {"error": "Course not found"} with HTTP 404

Error scenarios to test

    Invalid date format for target_date curl -s -X POST -H "Content-Type: application/json" -d '{"name":"Bad Date","description":"Bad date format","target_date":"2026/08/30","status":"Not Started"}' http://127.0.0.1:5000/api/courses

    Invalid status value curl -s -X POST -H "Content-Type: application/json" -d '{"name":"Bad Status","description":"Status wrong","target_date":"2026-08-30","status":"Started"}' http://127.0.0.1:5000/api/courses

    Missing id for update curl -s -X PUT -H "Content-Type: application/json" -d '{"name":"X","description":"Y","target_date":"2026-12-31","status":"Not Started"}' http://127.0.0.1:5000/api/courses

    Missing id for delete curl -s -X DELETE -H "Content-Type: application/json" -d '{}' http://127.0.0.1:5000/api/courses

Notes:

    The id is auto-generated on create. It increments with each new course.
    created_at is a UTC timestamp generated at creation time.
    All data is stored in courses.json in the project directory. To reset, delete courses.json and restart the server.

6) Testing instructions

    Start the server:
        python app.py
    Use the curl commands shown in the API endpoints section to test each operation.
    Tips:
        You can test sequentially (create, read, update, delete) to see how the data changes.
        If you’re on Windows PowerShell, ensure you escape quotes properly or use single quotes where allowed.

Optional tools:

    Postman or Insomnia for a GUI-based REST client
    unittest/pytest for automated tests (optional for beginners)

7) Troubleshooting common issues

    Server won’t start or port is in use
        Ensure no other process is listening on port 5000.
        Try changing the port by editing the app.py if needed (not required for the current setup).

    Python or Flask not found
        Ensure Python is installed and added to PATH.
        Ensure you installed Flask in your active environment: pip install Flask

    JSON file read/write errors
        Make sure the project directory is writable.
        If courses.json is corrupted, the app handles JSONDecodeError and uses an empty list.

    Validation errors (missing fields, invalid date, invalid status)
        Double-check required fields in the request body.
        Confirm target_date is in YYYY-MM-DD format (e.g., 2026-08-30).
        Ensure status is exactly one of: Not Started, In Progress, Completed.

    404 for a course not found
        The ID you request may not exist yet. Create a new course to get a valid ID, then test with that ID.

8) Project structure explanation

    app.py
        The main Flask application implementing the REST API.
        Handles:
            Loading and saving data to courses.json
            Input validation (required fields, date format, allowed statuses)
            CRUD endpoints:
                POST /api/courses
                GET /api/courses
                GET /api/courses/<id>
                PUT /api/courses
                DELETE /api/courses
        Auto-creates courses.json if missing.

    courses.json
        JSON file used as the simple database.
        Stores a list of course objects.

    venv (optional)
        Virtual environment directory (if you chose to use one).

    README.md
        This file containing user-friendly instructions and API reference.

    requirements.txt (optional)
        If you want to pin dependencies, you can add: Flask>=2.x
