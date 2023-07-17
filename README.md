# star-wars-django

A sample Django application which will act as an API server serving the data from  https://sw-api-rwjfuiltyq-el.a.run.app/ with Few enhancements.

Currently Supports the following -
- Planets List API with pagination and Search Filters with sorting.
- Movies List API with pagination and Search Filters with sorting.
- Utility Management Command which will Query the API and ingest the data into the database.
- Favorites API which allows a user to set a custom name for every Planet and Movies and to make it as Favorite (Currently custom name is only supported if we mark it as favorite, as wanted to showcase the Annotate, Exists query for the Generic FK.)
- A search on Movie and Planets List API will also search the custom names and give the relevant results.


Django and Django Rest Frameworks Concepts Showcased:
- Serializers to Normalise data according to Database Schema during ingestion.
- Filter and Search classes in Views
- Generic Foreign Key for a Generic Implementation of Favourites for Movies and Planets which can be extended to other objects as well with Minimal changes.
- Generic Relationships are used for reverse lookups and queries for Favorites.
- Management Commands are used for Initializing the Database with data from the Star Wars API.
- Using Bulk Create functions to handle scale import of data.

Setup:
1. Clone the repo
2. Create a python virtualenv using the command 
>> virtualenv -p python3 venv
3. Initialize venv
>> source venv/bin/active
4. Install the pip packages
>> pip install -r requirements.txt
5. Go to the project folder and Run DB migrations
>> python manage.py migrate
6. Initialize Data into the DB from the APIs
>> python manage.py initialize_database
7. Start Backend Server
>> python manage.py runserver

