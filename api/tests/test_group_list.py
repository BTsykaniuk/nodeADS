import tempfile

from PIL import Image
from django.core.files import File
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from rest_framework.test import APITestCase
from model_mommy import mommy


class GroupListAPITestCases(APITestCase):
    def setUp(self):
        super().setUp()
        self.view = reverse('api:group-list')

    def get_image(self):
        image = Image.new('RGB', (100, 100))
        tmp_file = tempfile.NamedTemporaryFile(suffix='.jpg')
        image.save(tmp_file)

        file = File(tmp_file)
        uploaded_file = SimpleUploadedFile('new_image.jpg', file.read(), content_type='multipart/form-data')
        return uploaded_file

    def create_group(self, parent=None):
        """Shortcut to create Group"""
        group = mommy.make('categories.Group',
                           parent=parent,
                           icon=self.get_image())
        return group

    def create_element(self, group_kwargs=None):
        """Shortcut to create Element"""
        kwargs = group_kwargs or {}
        element = mommy.make('categories.Element',
                             icon=self.get_image(),
                             **kwargs)
        return element

    def test_group_list(self):
        """Check List request"""
        parent = self.create_group()
        child = self.create_group(parent=parent)  # child
        self.create_group(parent=child)  # child

        response = self.client.get(self.view, format='json')
        self.assertEqual(200, response.status_code, response.data)

        self.assertEqual(response.data['results'][0]['subgroups_count'], 1, response.data)
        self.assertEqual(len(response.data['results'][0]['subgroups']), 1)
        self.assertEqual(response.data['results'][0]['subgroups'][0]['subgroups_count'], 1)
        self.assertEqual(len(response.data['results'][0]['subgroups'][0]['subgroups']), 1)

    def test_group_list_elemetns(self):
        parent = self.create_group()
        self.create_element({'group': parent,
                             'moderated': True})
        child = self.create_group(parent=parent)
        self.create_element({'group': child})

        response = self.client.get(self.view, format='json')
        self.assertEqual(200, response.status_code, response.data)

        self.assertEqual(response.data['results'][0]['elements_count'], 1, response.data)
        self.assertEqual(len(response.data['results'][0]['elements']), 1)
        self.assertEqual(response.data['results'][0]['subgroups'][0]['elements_count'], 1, response.data)
        self.assertEqual(len(response.data['results'][0]['subgroups'][0]['elements']), 0, response.data)
