MySQL setup notes for this project

1) Install a MySQL driver for Python on Windows:
   - Recommended: PyMySQL (pure Python, easy to install)
     pip install pymysql

   - Alternative (faster, but requires wheels/build tools): mysqlclient
     pip install mysqlclient

2) If you use PyMySQL, add this at the top of `stars/settings.py` (before DATABASES) or in `manage.py` startup:

   import pymysql
   pymysql.install_as_MySQLdb()

3) Make sure `DATABASES` in `stars/settings.py` matches your MySQL credentials. Example:

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'stars_db',
        'USER': 'root',
        'PASSWORD': 'your_password_here',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

4) Run migrations and create superuser from PowerShell in the `stars_project` folder:

```powershell
py -3 -m pip install -r requirements.txt  # if you have requirements
py manage.py makemigrations
py manage.py migrate
py manage.py createsuperuser
py manage.py runserver
```

5) If you see errors connecting to MySQL, verify the DB credentials in MySQL Workbench and that the MySQL server is running and accepting TCP connections on port 3306.

6) Notes about forms:
   - I added `forms.py` ModelForm implementations for `users`, `gallery`, `gamification`, and `moderation`.
   - Views should import these forms and use them (e.g., `from users.forms import RegistrationForm, UserProfileForm`).
   - These form classes are non-breaking; they don't change templates or view logic automatically. You can progressively switch your views to use them (I'll help wire them into specific views if you want).