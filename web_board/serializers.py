from rest_framework import serializers
from .models import Board,Topic,Post

class BoardSerializer(serializers.ModelSerializer):
    topics = serializers.HyperlinkedIdentityField(view_name='board-topics', format='html')
    class Meta:
        model = Board
        fields = ('url','id','name','description','topics')

class TopicSerializer(serializers.ModelSerializer):
    board_name = serializers.ReadOnlyField(source='board.name')
    starter_name = serializers.ReadOnlyField(source='starter.username')
    posts = serializers.HyperlinkedIdentityField(view_name='topic-posts', format='html')
    board_id = serializers.IntegerField()
    class Meta:
        model = Topic
        fields = ('url','id','board_id','board_name', 'subject', 'starter_name',
                  'posts')



class PostSerializer(serializers.ModelSerializer):
    # posts = serializers.PrimaryKeyRelatedField(many=True, queryset=Topic.objects.all())
    topic_name = serializers.ReadOnlyField(source='topic.subject')
    created_by = serializers.ReadOnlyField(source='created_by.username')
    topic_id = serializers.IntegerField()
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = Post
        fields = ('url', 'id','topic_name','topic_id', 'message','created_by' ,'created_at')

from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    # boards = serializers.PrimaryKeyRelatedField(many=True, queryset=Board.objects.all())

    class Meta:
        model = User
        fields = ('id', 'username')