Setting up postgresql:

1. install postgresql:
`` brew  install postgresql `` (macOS)
`` sudo apt-get install postgresql `` (linux)

2. start/stop postgresql:
`` brew services start postgresql ``
`` brew services stop postgresql ``

3. create a database
`` psql postgres ``
`` CREATE DATABASE pasddb; ``
`` create user pasduser with encrypted password 'password'; ``
`` grant all privileges on database pasddb to pasdduser; ``


Make sure to also set up a virtual environment for this project.
