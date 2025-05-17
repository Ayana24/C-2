from .models import PerevalAdded, PerevalImage, User, Coord
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction

class PerevalService:
    @staticmethod
    @transaction.atomic
    def create_pereval(data: dict) -> PerevalAdded:
        """
        Создание новой записи перевала и связанных объектов (User, Coord, Images).
        """
        try:
            user_data = data.pop("user")
            coord_data = data.pop("coord")
            images_data = data.pop("images", [])

            user, _ = User.objects.get_or_create(email=user_data["email"], defaults=user_data)
            coord = Coord.objects.create(**coord_data)

            pereval = PerevalAdded.objects.create(user=user, coord=coord, status='new', **data)

            for image in images_data:
                PerevalImage.objects.create(pereval=pereval, **image)

            return pereval

        except Exception as e:
            print("Ошибка при создании:", e)
            return None

    @staticmethod
    def update_pereval(pereval_id, update_data):
        try:
            pereval = PerevalAdded.objects.get(id=pereval_id)
            if pereval.status != "new":
                return None  # Нельзя редактировать, если не в статусе new

            coords_data = update_data.pop("coords", None)
            images_data = update_data.pop("images", None)

            for attr, value in update_data.items():
                setattr(pereval, attr, value)
            pereval.save()

            if coords_data:
                for attr, value in coords_data.items():
                    setattr(pereval.coords, attr, value)
                pereval.coords.save()

            if images_data is not None:
                pereval.images.all().delete()
                for image in images_data:
                    PerevalImage.objects.create(pereval=pereval, **image)

            return pereval

        except ObjectDoesNotExist:
            return None

    @staticmethod
    def get_perevals(user_email=None):
        if user_email:
            return PerevalAdded.objects.filter(user__email=user_email)
        return PerevalAdded.objects.all()

    @staticmethod
    def get_pereval_by_id(pereval_id):
        try:
            return PerevalAdded.objects.get(id=pereval_id)
        except PerevalAdded.DoesNotExist:
            return None


class PerevalDataService:
    @staticmethod
    @transaction.atomic
    def create_pereval(data: dict, user_email: str):
        # Создаем или получаем пользователя по email
        user_data = data.get('user', {})
        user, _ = User.objects.get_or_create(
            email=user_email,
            defaults={
                'fam': user_data.get('fam', ''),
                'name': user_data.get('name', ''),
                'otc': user_data.get('otc', ''),
                'phone': user_data.get('phone', ''),
            }
        )

        # Создаем координаты
        coord_data = data.get('coords')
        coord = Coord.objects.create(
            latitude=coord_data.get('latitude'),
            longitude=coord_data.get('longitude'),
            height=coord_data.get('height')
        )

        # Создаем перевал
        pereval = PerevalAdded.objects.create(
            beautyTitle=data.get('beauty_title'),
            title=data.get('title'),
            other_titles=data.get('other_titles', ''),
            connect=data.get('connect', ''),
            add_time=data.get('add_time'),
            coord=coord,
            user=user,
            status='new',
            level_winter=data.get('level_winter', ''),
            level_summer=data.get('level_summer', ''),
            level_autumn=data.get('level_autumn', ''),
            level_spring=data.get('level_spring', ''),
        )

        # Сохраняем изображения (если есть)
        images = data.get('images', [])
        for img in images:
            PerevalImage.objects.create(
                pereval=pereval,
                title=img.get('title', ''),
                image=img.get('data')
            )

        return pereval

    @staticmethod
    def serialize_pereval(pereval):
        # Пример сериализации перевала в словарь, чтобы вернуть через API
        return {
            "id": pereval.id,
            "beautyTitle": pereval.beautyTitle,
            "title": pereval.title,
            "other_titles": pereval.other_titles,
            "connect": pereval.connect,
            "add_time": pereval.add_time,
            "status": pereval.status,
            "coord": {
                "latitude": pereval.coords.latitude,
                "longitude": pereval.coords.longitude,
                "height": pereval.coords.height
            },
            "user": {
                "email": pereval.user.email,
                "fam": pereval.user.fam,
                "name": pereval.user.name,
                "otc": pereval.user.otc,
                "phone": pereval.user.phone
            },
            # Можно добавить другие поля по необходимости
        }

    @staticmethod
    @transaction.atomic
    def update_pereval(pereval, data: dict):
        try:
            # Обновляем простые поля перевала
            pereval.beautyTitle = data.get('beauty_title', pereval.beautyTitle)
            pereval.title = data.get('title', pereval.title)
            pereval.other_titles = data.get('other_titles', pereval.other_titles)
            pereval.connect = data.get('connect', pereval.connect)
            pereval.add_time = data.get('add_time', pereval.add_time)

            # Обновляем координаты, если есть
            coord_data = data.get('coords')
            if coord_data:
                pereval.coord.latitude = coord_data.get('latitude', pereval.coord.latitude)
                pereval.coord.longitude = coord_data.get('longitude', pereval.coord.longitude)
                pereval.coord.height = coord_data.get('height', pereval.coord.height)
                pereval.coord.save()

            pereval.save()
            return True
        except Exception:
            return False