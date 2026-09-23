from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .serializers import UserActivitySerializer


@api_view(['POST'])
def create_activity(request):

    serializer = UserActivitySerializer(
        data=request.data
    )

    if serializer.is_valid():
        activity = serializer.save()

        return Response(
            UserActivitySerializer(activity).data,
            status=status.HTTP_201_CREATED
        )

    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
    )