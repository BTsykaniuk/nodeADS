import tempfile

from PIL import Image
from django.core.files import File
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from rest_framework.test import APITestCase
from model_mommy import mommy


class ElementCreateAPITestCases(APITestCase):
    def setUp(self):
        super().setUp()
        self.group = self.create_group()
        self.view = reverse('api:create-element', kwargs={'id': self.group.id})

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

    def test_create_element(self):
        """Check List request"""
        file = File(open('static/rest_framework/img/grid.png', 'rb'))
        uploaded_file = SimpleUploadedFile('new_image.jpg', file.read(), content_type='multipart/form-data')
        data = {
            'name': 'TestElement',
            'icon': uploaded_file,
            'description': 'Some Text'
        }

        response = self.client.post(self.view, data, format='multipart')
        self.assertEqual(201, response.status_code, response.data)
