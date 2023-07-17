from django.db import IntegrityError
from rest_framework.exceptions import ValidationError
import requests
from datetime import datetime
from base.constants import BATCH_SIZE
from rest_framework.pagination import PageNumberPagination

from movies.utilities import save_movies
from planets.utilities import save_planets


def initialize_database():
    """
    Function which will fetch data from the API and add it to the database, will implement as a management command
    but can be a periodic running query as well.
    """
    save_movies()
    save_planets()


def fetch_star_wars_data(url):
    """
    Fetches data from the Star Wars API.

    Args:
        url (str): The URL to fetch the data from.

    Returns:
        dict: The JSON response containing the fetched data, or None if the request fails.
    """
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        results = data.get('results', [])
        next_url = data.get('next')

        while next_url:
            response = requests.get(next_url)
            if response.status_code == 200:
                next_data = response.json()
                results.extend(next_data.get('results', []))
                next_url = next_data.get('next')
            else:
                #  Log and handle other cases
                print("API response was non 200, Please Verify")
                break

        data['results'] = results
        return data

    return None


def normalize_data(data, serializer_class):
    """
    Normalizes and validates the data using the provided serializer class.

    Args:
        data (list): The list of data objects to normalize.
        serializer_class (class): The serializer class to use for normalization.

    Returns:
        list: The normalized and validated data objects.
    """
    serializer = serializer_class(data=data, many=True)
    serializer.is_valid(raise_exception=True)
    return serializer.validated_data


def batch_create_objects(objects, model_class):
    """
    Creates objects in batches using bulk_create.

    Args:
        objects (list): The list of objects to create.
        model_class (class): The model class for the objects being created.
    """
    try:
        model_class.objects.bulk_create(objects, BATCH_SIZE)
    except IntegrityError as e:
        # can log integrity error or even loop over bulk create to create all entries except the one's that are erroring out.
        print(f"IntegrityError: {e}")
    except Exception as e:
        # Log other exceptions
        print(f"Error occurred during bulk creation: {e}")


def save_objects(url, model_class, serializer_class):
    """
    Fetches and saves objects from the Star Wars API to the database.

    Args:
        url (str): The URL to fetch the objects from.
        model_class (class): The model class for the objects being saved.
        serializer_class (class): The serializer class for normalizing the data.
    """
    data = fetch_star_wars_data(url)
    if data:
        results = data.get('results', [])
        try:
            normalized_data = normalize_data(results, serializer_class)
            objects_to_create = [model_class(**item) for item in normalized_data]
            batch_create_objects(objects_to_create, model_class)
        except ValidationError as e:
            # This can be used to either skip whole initialization if DB already populated 
            # Or can be used to have an updation logic by first querying DB 
            print("validation Error means already done, skipping this import")
            pass
    else:
        print("No data found, Check API")


class BasePaginationClass(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100