# Student Employment Web App
This is a web application for tracking student employment information in the IS program

# Setting up local development environment
(Windows only. Mac might need some tweaking)
Make sure python is installed beforehand.
1. `git clone` the project
2. Open a terminal in the root directory of the project
3. Set up virtual environment `python3 -m virtualenv .venv`
4. Activate the virtual environment
    - `source ./.venv/Scripts/activate` if using git bash terminal
    - `./.venv/Scripts/activate` if using PowerShell
5. Install python dependencies: `pip install -r requirements.txt`
6. (optional) Create a superuser so you can use the Django admin panel: `python manage.py createsuper`
7. Run the development server `python manage.py runserver`
8. Visit the app in a web browser by navigating to `http://localhost:8000`
9. (optional) View the admin panel by navigating to `http://localhost:8000/admin` and logging in with the credentials you added in step 6

# Folder structure
- MainApp is where all the functionality is going to be added
    - URL routes go in urls.py
    - Views (business logic) go in views.py
    - Models (database tables) go in models.py (these are already set up)
- StudentEmployeeProject has the settings for the project