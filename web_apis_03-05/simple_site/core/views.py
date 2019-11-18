import json

from rest_framework import status
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.reverse import reverse
from .permissions import IsOwnerOrReadOnly
from .serializers import *


def import_db():
    data = open('db.json', 'r')
    as_json = json.load(data)

    for profile in as_json['users']:
        adress = Adress.objects.create(street=profile['address']['street'],
                                       suite=profile['address']['suite'],
                                       city=profile['address']['city'],
                                       zipcode=profile['address']['zipcode'])
        name = profile['name']
        email = profile['email']
        password = "1234"
        user = User.objects.create_user(username=name,
                                        email=email,
                                        password=password)
        Profile.objects.create(user=user, name=name, email=email, adress=adress)

    for post in as_json['posts']:
        profile = Profile.objects.get(id=post['userId'])
        Post.objects.create(id=post['id'],
                            title=post['title'],
                            body=post['body'],
                            userId=profile)

    for comment in as_json['comments']:
        post = Post.objects.get(id=comment['postId'])
        Comment.objects.create(id=comment['id'],
                               name=comment['name'],
                               email=comment['email'],
                               body=comment['body'],
                               postId=post)


class ApiRoot(generics.GenericAPIView):
    name = 'api-root'

    def get(self, request, *args, **kwargs):
        return Response({
            'profiles': reverse(profiles_list, request=request),
            'profile_posts': reverse(profile_posts_list, request=request),
            'post-comments': reverse(post_comments_list, request=request),
            'profile-status': reverse(profile_status, request=request)
        })


@api_view(['GET', 'POST'])
def profiles_list(request):
    permissions_classes = (
        permissions.IsAuthenticatedOrReadOnly,
    )
    if request.method == 'GET':
        profiles = Profile.objects.all()
        profiles_serializer = ProfileSerializer(profiles, many=True)
        return Response(profiles_serializer.data)
    elif request.method == 'POST':
        profile_serializer = ProfileSerializer(data=request.data)
        if profile_serializer.is_valid():
            profile_serializer.save()
            return Response(profile_serializer.data,
                            status=status.HTTP_201_CREATED)
        return Response(profile_serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def profile_detail(request, pk):
    permissions_classes = (
        permissions.IsAuthenticatedOrReadOnly,
    )
    try:
        profile = Profile.objects.get(pk=pk)
    except Profile.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        profile_serializer = ProfileSerializer(profile)
        return Response(profile_serializer.data)
    elif request.method == 'PUT':
        profile_serializer = ProfileSerializer(profile, data=request.data)
        if profile_serializer.is_valid():
            profile_serializer.save()
            return Response(profile_serializer.data)
        return Response(profile_serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        profile.delete()
        return Response(status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def profile_posts_list(request):
    profiles = Profile.objects.all()
    profiles_posts_serializer = ProfilePostsSerializer(profiles, many=True)
    return Response(profiles_posts_serializer.data)


@api_view(['GET'])
def profile_posts_detail(request, pk):
    try:
        profile = Profile.objects.get(pk=pk)
    except Profile.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    profile_serializer = ProfilePostsSerializer(profile)
    return Response(profile_serializer.data)


@api_view(['GET'])
def post_comments_list(request):
    posts = Post.objects.all()
    post_comments_serializer = PostCommentsSerializer(posts, many=True)
    return Response(post_comments_serializer.data)


@api_view(['GET'])
def post_comments_detail(request, pk):
    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    post_serializer = PostCommentsSerializer(post)
    return Response(post_serializer.data)


@api_view(['GET', 'POST'])
def comments_list(request, pk):
    permissions_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly
    )
    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        # comments = Comment.objects.all()
        comments_serializer = CommentSerializer(post.comments, many=True)
        return Response(comments_serializer.data)
    elif request.method == 'POST':
        comment = request.data
        comment['postId'] = pk
        comment_serializer = CommentSerializer(data=comment)

        if comment_serializer.is_valid():
            comment_serializer.save()
            return Response(comment_serializer.data,
                            status=status.HTTP_201_CREATED)
        return Response(comment_serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def comment_detail(request, pk, pk2):
    permissions_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly
    )
    try:
        post = Post.objects.get(pk=pk)
        try:
            comment = Comment.objects.get(pk=pk2)
        except Comment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    except Post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        comment_serializer = CommentSerializer(comment)
        return Response(comment_serializer.data)
    elif request.method == 'PUT':
        comment_data = request.data
        comment_data['postId'] = pk
        comment_serializer = CommentSerializer(comment, data=comment_data)
        if comment_serializer.is_valid():
            comment_serializer.save()
            return Response(comment_serializer.data)
        return Response(comment_serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        comment.delete()
        return Response(status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def profile_status(request):
    profiles = Profile.objects.all()
    total = list()
    for profile in profiles:
        status = dict()
        profile_posts = 0
        post_comments = 0
        for post in profile.posts.all():
            profile_posts += 1
            for comment in post.comments.all():
                post_comments += 1
        status['pk'] = profile.id
        status['name'] = profile.name
        status['total_posts'] = profile_posts
        status['total_comments'] = post_comments
        total.append(status)
    return Response(total)