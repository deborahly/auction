# CHILI CARDS (anki)

This was my capstone project for Harvard's CS50's Web Programming with Python and JavaScript, having conceived the project and built it from the ground up completely on my own.

### CONCEPT
Chili Cards lets the user create flashcards with front and back sides to exercice any given knowledge, such as languages and school disciplines. The app enables the creation of different decks and the configuration of the study sessions by minutes you want to spend or number of cards you want to review.

App presentation video: [https://youtu.be/dCjwqGBTr50](https://youtu.be/dCjwqGBTr50)

### PROJET CHARACTERISTICS 
The app uses a good amount of JavaScript code to comunicate with the server, fetching data as well as updating the client side without reloading the pages. Sass was adopted to facilitate styling. Among the style features, it is worth mentioning the app's screen responsiveness, with two different page layouts, one for small and the other for large screens.

On the server side, Django's framework was considerably explored. Apart from the must-have views and urls setting, the project also makes use of Django's models, forms and tests. Specially models. Queries using models to navigate the database appear numerous times.

### KEY FEATURES
#### When not logged in, users will be able to: 
- Register
- Login
- Go to Home and read a welcome text
#### When logged in, users will be able to:
- Manage existing decks and cards
- Create, archive and delete decks
- Create, edit and delete cards
- Study with cards, by way of memorizing information through repetition
- Set the quantity of cards of each study session
- Set a timer for each study session (optional)
- Grade the difficulty of each card
- Have information on each deck, such as when it was created, when it was last updated and what is its level of difficulty, which is defined as the difficulty average of all the cards it contains

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

### TEST
The code contains endpoints tests in /anki/test_endpoints.py.

To run the tests, execute:

```bash
python manage.py test
``` 
