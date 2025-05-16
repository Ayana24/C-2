from rest_framework import serializers
from .models import User, Coord, PerevalAdded, PerevalImage


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class CoordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coord
        fields = '__all__'


class PerevalImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PerevalImage
        fields = ['image']


class PerevalAddedSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    coord = CoordSerializer()
    images = PerevalImageSerializer(many=True, required=False)

    class Meta:
        model = PerevalAdded
        fields = '__all__'

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        coords_data = validated_data.pop('coord')
        images_data = validated_data.pop('images', [])

        user, _ = User.objects.get_or_create(email=user_data['email'], defaults=user_data)
        coords = Coord.objects.create(**coords_data)
        pereval = PerevalAdded.objects.create(user=user, coord=coords, **validated_data)

        for image_data in images_data:
            PerevalImage.objects.create(pereval=pereval, **image_data)

        return pereval

class ImageSerializer(serializers.Serializer):
    title = serializers.CharField()
    data = serializers.ImageField()

class PerevalSubmitSerializer(serializers.Serializer):
    user = serializers.DictField()  # Можно уточнить поля отдельно, если нужно
    coords = serializers.DictField()
    beauty_title = serializers.CharField()
    title = serializers.CharField()
    other_titles = serializers.CharField(allow_blank=True, required=False)
    connect = serializers.CharField(allow_blank=True, required=False)
    level_winter = serializers.CharField(allow_blank=True, required=False)
    level_summer = serializers.CharField(allow_blank=True, required=False)
    level_autumn = serializers.CharField(allow_blank=True, required=False)
    level_spring = serializers.CharField(allow_blank=True, required=False)
    images = ImageSerializer(many=True, required=False)
