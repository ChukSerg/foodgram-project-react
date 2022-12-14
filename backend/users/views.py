from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from users.models import Follow
from users.serializers import FollowSerializer

User = get_user_model()


class FollowUserView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, id):
        author = get_object_or_404(User, id=id)
        print(request.user.id, author.id)
        if request.user.id == author.id:
            raise ValidationError(
                "Вы не можете подписаться сами на себя!"
            )
        serializer = FollowSerializer(
            Follow.objects.create(user=request.user, author=author),
            context={"request": request},
        )
        return Response(
            serializer.data, status=status.HTTP_201_CREATED
        )

    def delete(self, request, id):
        author = get_object_or_404(User, id=id)
        if Follow.objects.filter(
            user=request.user, author=author
        ).exists():
            Follow.objects.filter(
                user=request.user, author=author
            ).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            {"errors": "Автор отсутсвует в списке подписок"},
            status=status.HTTP_400_BAD_REQUEST,
        )


class SubscriptionsView(ListAPIView):
    serializer_class = FollowSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Follow.objects.filter(user=self.request.user)
