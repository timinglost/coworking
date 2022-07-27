from django.core.management.base import BaseCommand
from createapp.models import RoomCategory, Room, Address
from userapp.models import UserModel
from django.contrib.auth.models import User

import json, os
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
            address_name = room["address"]
            user_name = room["full_name"]
            _category = RoomCategory.objects.get(name=category_name)
            _address = Address.objects.get()
            _user = UserModel.objects.get(name=user_name)
            room['category'] = _category
            room['address'] = _address
            room['full_name'] = _user
            new_category = Room(**room)
            new_category.save()

        super_user = User.objects.create_superuser('admin', 'django@geekshop.local', 'admin')
