from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .services import PerevalService
from .models import PerevalAdded, User
from .serializers import PerevalAddedSerializer
from .services import PerevalDataService

class PerevalAddedViewSet(viewsets.ModelViewSet):
    queryset = PerevalAdded.objects.all()
    serializer_class = PerevalAddedSerializer

class PerevalCreateAPIView(APIView):
    def post(self, request):
        try:
            pereval = PerevalService.create_pereval(request.data)
            return Response({"status": "success", "id": pereval.id}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"status": "error", "message": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class SubmitDataView(APIView):
    def post(self, request):
        # Создание перевала
        user_email = request.data.get('user', {}).get('email')
        if not user_email:
            return Response({"error": "Email пользователя обязателен"}, status=status.HTTP_400_BAD_REQUEST)
        pereval = PerevalDataService.create_pereval(request.data, user_email)
        return Response({"id": pereval.id}, status=status.HTTP_201_CREATED)

    def get(self, request, id=None):
        # Если id передан, возвращаем один перевал
        if id:
            pereval = get_object_or_404(PerevalAdded, id=id)
            data = PerevalDataService.serialize_pereval(pereval)
            return Response(data, status=status.HTTP_200_OK)

        # Если id нет, проверяем query params на user__email и возвращаем список
        email = request.query_params.get('user__email')
        if email:
            user = get_object_or_404(User, email=email)
            perevals = PerevalAdded.objects.filter(user=user)
            data = [PerevalDataService.serialize_pereval(p) for p in perevals]
            return Response(data, status=status.HTTP_200_OK)

        return Response({"error": "id или user__email параметр обязателен"}, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, id=None):
        if not id:
            return Response({"state": 0, "message": "ID перевала обязателен"}, status=status.HTTP_400_BAD_REQUEST)

        pereval = get_object_or_404(PerevalAdded, id=id)

        if pereval.status != 'new':
            return Response({"state": 0, "message": "Редактирование возможно только для перевалов со статусом 'new'"}, status=status.HTTP_400_BAD_REQUEST)

        # Проверяем запрет на изменение user info (ФИО, email, телефон)
        user_data = request.data.get('user', {})
        if any(field in user_data for field in ['email', 'fam', 'name', 'otc', 'phone']):
            return Response({"state": 0, "message": "Редактирование ФИО, email и телефона запрещено"}, status=status.HTTP_400_BAD_REQUEST)

        # Обновляем поля перевала (кроме user info)
        updated = PerevalDataService.update_pereval(pereval, request.data)
        if updated:
            return Response({"state": 1}, status=status.HTTP_200_OK)
        else:
            return Response({"state": 0, "message": "Ошибка при обновлении перевала"}, status=status.HTTP_400_BAD_REQUEST)