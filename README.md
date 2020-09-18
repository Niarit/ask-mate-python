# AskMate

## Introduction

The goal was to build a Q&A site like StackOverflow with Python (Flask) & JavaScript.

## Technologies

- Python 3
- Flask 1.1
- BCrypt 3.1
- PostgreSQL

## Setup

### Environment

- Rename `.env.example` to `.env`
- Complete the key value pairs
- Create virtual environment
- Change the `app.secret_key` in the `server.py` to something else

```sh
$ python3 -m venv venv
```

- Activate virtual environment (Linux)

```bash
$ source venv/bin/activate
```

- Activate virtual environment (Windows)

```sh
$ venv\Scripts\activate.bat
```

- Install required packages

```bash
$ pip install -r requirements.txt
```

### PostgreSQL

- Create a user and database according to the previously edited `.env` file
- Import the `sample_data/askmatepart2-sample-data.sqldata.sql` file to create the
  tables and seed the database

### Webserver

Start it:

```bash
$ python server.py
```

## Status

### Sprint 3 (2019 Nov 18-22)

- [x] **_List users_**
- [x] **_User registration_**
- [x] **_User page_**: List all his/her activities
- [x] **_User login_**
- [x] **_Bind questions to user_**
- [x] **_Bind answers to user_**
- [x] **_Bind comments to user_**
- [x] **_Tag page_**: List all the existing tags
- [x] **_Accepted answer_**
- [x] **_Gain reputation_**
- [x] **_Lose reputation_**
- [Presentation](https://docs.google.com/presentation/d/1P6x9nOs2sypd4lGXyMe4ELKoCaUFDahvfg0gsFR2fhI)

### Sprint 2 (2019 Nov 4-8)

- [x] **_Use database_**: Make the application use a database instead of CSV files
- [x] **_Search questions_**: Search in question's title and/or description
- [x] **_Display latest questions_**: Display only 5 questions on the home page
- [x] **_Edit answer_**
- [x] **_Add comment to question_**
- [x] **_Delete comments_**
- [x] **Add comment to answer**
- [x] **_Edit comments_**
- [x] **_Tag question_**: Add tags to questions
- [x] **_Delete tag_**
- [x] **_Fancy search results_**: Highlight the search phrase in the search results
- [Presentation](https://docs.google.com/presentation/d/1WHhGgExH5qJVj50_K5qmJaPXYGOwvW6mk9SK7Tvdf6U)

### Sprint 1 (2019 Oct 21-25)

- [x] **_Ask a question_**
- [x] **_List questions_**: Navigating to `/` or `/list` returns all questions
- [x] **_Display a question_**: Navigating to `/question/{question_id}` returns a question with its answers
- [x] **_Post an answer_**
- [x] **_Edit a question_**
- [x] **_Vote on questions_**: Ability to vote up or down a question
- [x] **_Sort questions_**: By title, submission time, message, etc.
- [x] **_Vote on answers_**: Ability to vote up or down an answer
- [x] **_Delete question_**
- [x] **_Delete an answer_**
- [x] **_Add image_**: Ability to upload `.jpg` or `.png` to questions and answers
