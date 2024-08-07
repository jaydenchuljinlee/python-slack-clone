from uuid import uuid4

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


from rest_framework import viewsets, permissions, generics, status
from rest_framework.generics import get_object_or_404
from rest_framework.request import Request
from rest_framework.response import Response

from .models import ChatChannel
from workspace.models import Workspace
from .serializers import ChannelSerializer, ChatChannelSerializer, ChatChannelModifySerializer, \
    ChatChannelFixDescSerializer, ChatChannelMembersModifyRequestSerializer, \
    ChatChannelAdminsModifyRequestSerializer


class ChatChannelView(generics.CreateAPIView,
                      generics.ListAPIView,
                      generics.UpdateAPIView):
    queryset = ChatChannel.channel_objects.all()
    serializer_class = ChatChannelSerializer
    http_method_names = ['get', 'post', 'patch']
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            self.serializer_class = ChatChannelModifySerializer
        elif self.request.method == 'PATCH':
            self.serializer_class = ChatChannelFixDescSerializer

        return self.serializer_class

    def get_queryset(self):
        hashed_value = self.kwargs.get('workspace__hashed_value', None)
        result = self.queryset.filter(workspace__hashed_value=hashed_value)
        return result

    def post(self, request: Request, *args, **kwargs):
        """
        `workspace_hashed_value`를 입력하면 해당 workspace의 `chat_channel`을 추가합니다.
        `name`에는 만들 채널의 이름을 넣으십시오.
        채널을 생성하면 `members`안에는 자동으로 만든 사람의 정보가 포함 됩니다.
        채널 만든 사람은 `admins`안에 역시 자동으로 들어갑니다.
        """
        if request.data.get('name', None) is None:
            return Response({'msg': 'name field is not filled.'}, status=status.HTTP_400_BAD_REQUEST)

        hashed_value = self.kwargs.get('workspace__hashed_value', None)

        workspace = Workspace.objects.get(hashed_value__exact=hashed_value)
        chat_channel = ChatChannel.objects.create(name=request.data.get('name', None),
                                                  description=request.data.get('description', None),
                                                  workspace=workspace,
                                                  hashed_value=str(uuid4())[:8])
        chat_channel.members.add(request.user)
        chat_channel.admins.add(request.user)

        serializer = self.get_serializer(chat_channel)
        return Response(serializer.data)

    def get(self, request: Request, *args, **kwargs):
        """
        `workspace_hashed_value`를 입력하면 해당 workspace의 `chat_channel`들이 나옵니다.
        """
        chat_channels = self.get_queryset()
        serializer = self.get_serializer(chat_channels, many=True)

        return Response(data=serializer.data)

    def patch(self, request: Request, *args, **kwargs):
        """
        `ChatChannel`의 설명 문구를 바꾸기 위한 엔드포인트 입니다.
        이걸로 `ChatChannel`의 이름이나 `members`는 못바꿉니다.
        `admins`안에 포함되지 않은 유저는 401이 나옵니다.
        """
        chat_channel = self.get_queryset().get(hashed_value__exact=request.data.get('hashed_value', None))

        if request.user not in chat_channel.admins.all():
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        chat_channel.description = request.data.get('description', None)
        chat_channel.save()

        serializer = ChatChannelSerializer(chat_channel)
        return Response(serializer.data)


