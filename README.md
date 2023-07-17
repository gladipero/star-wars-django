# star-wars-django

A sample Django application which will act as an API server serving the data from  https://sw-api-rwjfuiltyq-el.a.run.app/ with Few enhancements.

Currently Supports the following -
- Planets List API with pagination and Search Filters with sorting.
- Movies List API with pagination and Search Filters with sorting.
- Utility Management Command which will Query the API and ingest the data into the database.

Django and Django Rest Frameworks Concepts Showcased
- Serializers to Normalise data according to Database Schema during ingestion.
- Filter and Search classes in Views
- Generic Foreign Key for a Generic Implementation of Favourites for Movies and Planets which can be extended to other objects as well with Minimal changes.
- Generic Relationships are used for reverse lookups and queries for Favorites.
- Management Commands are used for Initializing the Database with data from the Star Wars API.