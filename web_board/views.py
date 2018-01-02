from django.contrib.auth.models import User
from rest_framework import renderers
from rest_framework.decorators import detail_route, list_route

from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from web_board.models import Board, Topic, Post
from web_board.permissions import IsOwnerOrReadOnly, IsOwnerOrReadOnlyPost, IsOwnerOrReadOnlyBoard
from web_board.serializers import BoardSerializer, TopicSerializer, PostSerializer, UserSerializer
from django.views.decorators.csrf import csrf_exempt

class BoardViewSet(viewsets.ModelViewSet):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnlyBoard,)


    @detail_route(url_name='topics',url_path='topics', methods=['get','post'], serializer_class=TopicSerializer)
    def topics(self, request, pk=None):

        queryset = Topic.objects.filter(board_id=pk)
        serializer = TopicSerializer(queryset,
                                     context={'request': request,'pk':pk},
                                     many=True)
        return Response(serializer.data)

    @detail_route(methods=['get'],url_path='topics/(?P<topic_id>[0-9]+)')
    def topics_detail(self, request, pk, topic_id):
        queryset = Topic.objects.filter(pk=topic_id)
        serializer = TopicSerializer(queryset,
                                     context={'request': request, 'pk': pk},
                                     many=True)
        return Response(serializer.data)

    # def perform_create(self, serializer):
    #     serializer.save(board_id = self.request.data.get('board_id'), starter_id = self.request.user.id)



class TopicViewSet(viewsets.ModelViewSet):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(board_id = self.request.data.get('board_id'), starter_id = self.request.user.id)



    @detail_route(url_name='posts',methods=['GET','POST'] , serializer_class = PostSerializer)
    def posts(self, request, pk=None):
        queryset = Post.objects.filter(topic_id=pk)
        serializer = PostSerializer(queryset,
                                    context={'request': request},
                                    many=True)

        return Response(serializer.data)


# @csrf_exempt
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnlyPost)

    def perform_create(self, serializer):
        serializer.save(created_by_id = self.request.user.id,topic_id = self.request.data.get('topic_id'))


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


