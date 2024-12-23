# Assignment-5 on Python/Flask
---

This is a basic Travel API based multiple microservices developed using Flask. Each microservice will handle a distinct function, such as managing destinations, handling user accounts and authentication.

Microservices Overview
1. Destination Service
    - Manages travel destinations, including posting/deleting(Admin only), and viewing destination details.
2. User Service
    - Handles user registration, authentication, and profile management.
3. Authentication Service
    -  Manages user authentication tokens and enforces role-based access for secure access to endpoints.
---
## File Structure
```
.
├── coverage_re
│   ├── coverage_html.js
│   ├── d_145eef247bfb46b6_authentication_service_py.html
│   ├── d_145eef247bfb46b6_destination_service_py.html
│   ├── d_145eef247bfb46b6_user_service_py.html
│   ├── favicon_32.png
│   ├── index.html
│   ├── keybd_closed.png
│   ├── keybd_open.png
│   ├── status.json
│   └── style.css
├── destinations.json
├── htmlcov
│   ├── coverage_html.js
│   ├── d_145eef247bfb46b6_authentication_service_py.html
│   ├── d_145eef247bfb46b6_destination_service_py.html
│   ├── d_145eef247bfb46b6_user_service_py.html
│   ├── d_145eef247bfb46b6_UUUser_service_py.html
│   ├── favicon_32.png
│   ├── index.html
│   ├── keybd_closed.png
│   ├── keybd_open.png
│   ├── status.json
│   └── style.css
├── pytest.ini
├── README.md
├── requirements.txt
├── src
│   ├── authentication_service.py
│   ├── destination_service.py
│   ├── destinations.json
│   ├── __init__.py
│   ├── __pycache__
│   │   ├── authentication_service.cpython-310.pyc
│   │   ├── destination_service.cpython-310.pyc
│   │   ├── __init__.cpython-310.pyc
│   │   └── user_service.cpython-310.pyc
│   ├── user_service.py
│   └── users.json
├── test_requirements.txt
├── tests
│   ├── conftest.py
│   ├── __init__.py
│   ├── __pycache__
│   │   ├── conftest.cpython-310-pytest-7.3.1.pyc
│   │   ├── conftest.cpython-310-pytest-8.3.3.pyc
│   │   ├── __init__.cpython-310.pyc
│   │   ├── test_authentication_service.cpython-310-pytest-7.3.1.pyc
│   │   ├── test_destination_service.cpython-310-pytest-7.3.1.pyc
│   │   ├── test_user_service copy.cpython-310-pytest-7.3.1.pyc
│   │   ├── test_user_service.cpython-310.pyc
│   │   └── test_user_service.cpython-310-pytest-7.3.1.pyc
│   ├── test_authentication_service.py
│   ├── test_destination_service.py
│   └── test_user_service.py
└── users.json
```

**Important Files/Folder Description**
- ./src - contains all the  files that are used to create the APIs
- ./tests - contains all the unittests that are used to evaluate the code in ./src folder
- ./htmlcov/index.html - contains the code coverage report

## Steps to run the Project
1. Clone the git repository.
2. Navigate to the root directory of the project.
3. Run the following command to install the required packages.
    ```bash
    pip install -r requirements.txt
    ```
4. Run all three .py files in ./src under the same environment but different instances. Run, the follwing command in three different terimnals- 
    ```bash
    python ./src/authentication_service.py
    python ./src/destination_service.py
    python ./src/user_service.py
    ```
5. All the swagger UIs will be visible in the following urls:
    - [User Service API - localhost:5002/apidocs](http://localhost:5002/apidocs)
    - [Authentication Service API - localhost:5003/apidocs](http://localhost:5003/apidocs)
    - [Destination Service API - localhost:5001/apidocs](http://localhost:5001/apidocs)

    If not running, please start from step 1 and make sure that these files run accordingly.

## Swagger UIs Interface
1. Ensure all the urls are running.
- User Service API 
    - Navigate to the user_service page.
    - Register yourself as an Admin/User.
    - LOGIN using the registered email and password.
    - Upon login you will get a TOKEN to authenticate yourself.
    - Authorize yourself using the token and GET your profile information. 
- Destination Service API 
    - Navigate to the destination_service page.
    - GET the destinations(view the list of destinations).
    - Authorize yourself as an Admin/User.
    - POST destinations- Admin only.
    - DELETE destination by their ID- Admin only.
- Authentication Service API 
    - Ensure Admins have access to specific actions.
    - Validates authorization.
    


## Running the tests
After installing all the API servers, one may run the tests using the following command.

```pytest -v```

**Coverage output**
```
Name                            Stmts   Miss  Cover   Missing
-------------------------------------------------------------
src/authentication_service.py      43      5    88%   83, 122-125
src/destination_service.py         58      8    86%   42-43, 51-52, 57, 63, 114, 160
src/user_service.py                64      7    89%   64, 70, 124, 132, 136, 223, 237
-------------------------------------------------------------
TOTAL                             165     20    88%
```
## Author
Rubayet Shareen

Software Engineer Intern, 
W3 Engineers Ltd.

