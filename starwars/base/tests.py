import requests
from django.core.exceptions import ValidationError
from django.test import TestCase
from unittest.mock import patch
from datetime import datetime
from base.constants import BATCH_SIZE
from rest_framework.exceptions import ErrorDetail
from movies.models import Movie
from base.utilities import (
    fetch_star_wars_data,
    normalize_data,
    batch_create_objects,
    save_objects,
    BasePaginationClass,
)


class TestUtilities(TestCase):
    def setUp(self):
        self.mock_data = {
            "results": [
                {"title": "Movie 1", "release_date": "2023-01-01"},
                {"title": "Movie 2", "release_date": "2023-02-01"},
            ],
            "next": None,
        }

    @patch("requests.get")
    def test_fetch_star_wars_data(self, mock_get):
        mock_response = requests.models.Response()
        mock_response.status_code = 200
        mock_response.json = lambda: self.mock_data
        mock_get.return_value = mock_response

        url = "https://example.com/api/movies/"
        data = fetch_star_wars_data(url)

        self.assertEqual(data, self.mock_data)

    @patch('movies.serializers.MovieSerializer')
    def test_normalize_data(self, mock_serializer):
        # Test data to normalize
        data = [
            {'title': 'Movie 1', 'release_date': '2023-01-01'},
            {'title': 'Movie 2', 'release_date': '2023-02-01'},
            {'title': 'Movie 3', 'release_date': '2023-03-01'},
        ]

        # Create an instance of the mock serializer
        serializer_instance = mock_serializer.return_value
        # Mock the is_valid method of the serializer to return True
        serializer_instance.is_valid.return_value = True
        # Mock the validated_data attribute of the serializer to return the test data
        serializer_instance.validated_data = data

        # Call the function with the test data and the mock serializer class
        result = normalize_data(data, mock_serializer)

        # Assert that the serializer class was called once with the correct data
        mock_serializer.assert_called_once_with(data=data, many=True)

        # Assert that the return value is the validated data from the serializer
        self.assertEqual(result, data)

    @patch('movies.models.Movie.objects.bulk_create')
    def test_batch_create_objects(self, mock_bulk_create):
        # Test data to create Movie instances
        data = [
            {'title': 'Movie 1', 'release_date': '2023-01-01'},
            {'title': 'Movie 2', 'release_date': '2023-02-01'},
            {'title': 'Movie 3', 'release_date': '2023-03-01'},
        ]

        # Call the function with the test data
        result = batch_create_objects(data, Movie)

        # Assert the return value is None (since batch_create_objects doesn't return anything)
        self.assertIsNone(result)


    @patch("base.utilities.normalize_data")
    @patch("base.utilities.fetch_star_wars_data")
    def test_save_objects_success(self, mock_fetch_data, mock_normalize_data):
        mock_fetch_data.return_value = self.mock_data
        mock_normalize_data.return_value = self.mock_data["results"]

        url = "https://example.com/api/movies/"
        model_class = None
        serializer_class = None

        save_objects(url, model_class, serializer_class)

        mock_fetch_data.assert_called_once_with(url)
        mock_normalize_data.assert_called_once_with(self.mock_data["results"], serializer_class)

    @patch("base.utilities.normalize_data")
    @patch("base.utilities.fetch_star_wars_data")
    def test_save_objects_validation_error(self, mock_fetch_data, mock_normalize_data):
        mock_fetch_data.return_value = self.mock_data
        mock_normalize_data.side_effect = ValidationError(
            [{"title": [ErrorDetail(string="Validation error", code="invalid")]}]
        )

        url = "https://example.com/api/movies/"
        model_class = None
        serializer_class = None

        save_objects(url, model_class, serializer_class)

        mock_fetch_data.assert_called_once_with(url)
        mock_normalize_data.assert_called_once_with(self.mock_data["results"], serializer_class)

    @patch("base.utilities.normalize_data")
    @patch("base.utilities.fetch_star_wars_data")
    def test_save_objects_no_data(self, mock_fetch_data, mock_normalize_data):
        mock_fetch_data.return_value = None

        url = "https://example.com/api/movies/"
        model_class = None
        serializer_class = None

        save_objects(url, model_class, serializer_class)

        mock_fetch_data.assert_called_once_with(url)
        mock_normalize_data.assert_not_called()

    def test_base_pagination_class(self):
        pagination = BasePaginationClass()
        self.assertEqual(pagination.page_size, 10)
        self.assertEqual(pagination.page_size_query_param, "page_size")
        self.assertEqual(pagination.max_page_size, 100)
