from django.core.management.base import BaseCommand
from createapp.models import RoomCategory, Room, Address, OfferImages
from userapp.models import UserModel
from django.contrib.auth.models import User

import json
import os

JSON_PATH = 'mainapp/jsons'


def load_from_json(file_name):
    with open(os.path.join(JSON_PATH, file_name + '.json'), mode='r', encoding='UTF-8') as infile:
        return json.load(infile)


class Command(BaseCommand):
    def handle(self, *args, **options):
        categories = load_from_json('categories')
        RoomCategory.objects.all().delete()
        for category in categories:
            new_category = RoomCategory(**category)
            new_category.save()

        addresses = load_from_json('addresses')
        Address.objects.all().delete()
        for address in addresses:
            new_address = Address(**address)
            new_address.save()

        users = load_from_json('users')
        UserModel.objects.all().delete()
        for user in users:
            new_user = UserModel(**user)
            new_user.save()

        rooms = load_from_json('rooms')
        Room.objects.all().delete()
        for room in rooms:
            category_name = room["category"]
            _category = RoomCategory.objects.get(name=category_name)
            room['category'] = _category
            new_category = Room(**room)
            new_category.save()

            address_name = room["address"]
            _address = Address.objects.get(name=address_name)
            room['address'] = _address
            new_addr = Address(**address)
            new_addr.save()

            user_name = room["room_owner"]
            _user = UserModel.objects.get(name=user_name)
            room['user'] = _user
            new_u = UserModel(**user)
            new_u.save()

        images = load_from_json('images')
        OfferImages.objects.all().delete()
        for image in images:
            new_image = OfferImages(**image)
            new_image.save()

    super_user = UserModel.objects.create_superuser('admin', 'django2@geekshop.local', 'Admin095863248')
