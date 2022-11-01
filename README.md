### INSTALL AND RUN
Make sure to have installed at least python 3.8.10.

Create virtual environment and install all dependencies:

```bash
git clone https://github.com/deborahly/e-auction.git
cd e-auction
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
```

To run the application, execute:

```bash
python manage.py runserver
```
The app is going to run on [127.0.0.1:8000](http://127.0.0.1:8000/).
