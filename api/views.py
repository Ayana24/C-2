from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .services import PerevalService
from .models import PerevalAdded
from .serializers import PerevalAddedSerializer
from .serializers import PerevalSubmitSerializer
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
        serializer = PerevalSubmitSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data

            user_email = data['user']['email']

            # Вызов сервиса создания перевала
            pereval = PerevalDataService.create_pereval(data, user_email)

            return Response(
                {'message': 'Перевал успешно добавлен', 'pereval_id': pereval.id},
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)