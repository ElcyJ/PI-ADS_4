from rest_framework import serializers
from .models import *


class AdressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Adress
        fields = ('street', 'suite', 'city', 'zipcode')


class ProfileSerializer(serializers.ModelSerializer):
    adress = AdressSerializer()

    class Meta:
        model = Profile
        fields = ('id', 'name', 'email', 'adress')

    def create(self, validated_data):
        name = validated_data("name")
        email = validated_data("email")
        password = "1234"
        request_address = validated_data.pop('adress')
        adress = Adress.objects.create(**request_address)
        user = User.objects.create_user(username=name, email=email,
                                        password=password)
        user.save()
        return Profile.objects.create(user=user,adress=adress,
                                      **validated_data)

    def update(self, instance, validated_data):
        adress_data = validated_data.pop('adress')
        adress = instance.adress
        instance.email = validated_data.get('email', instance.email)
        instance.name = validated_data.get('name', instance.name)
        adress.street = adress_data.get('street', adress.street)
        adress.suite = adress_data.get('suite', adress.suite)
        adress.city = adress_data.get('city', adress.city)
        adress.zipcode = adress_data.get('zipcode', adress.zipcode)
        instance.save()
        adress.save()
        return instance


class PostSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Post
        fields = ('title', 'body', 'userId', 'owner')


class ProfilePostsSerializer(serializers.ModelSerializer):
    posts = PostSerializer(many=True, read_only=True)

    class Meta:
        model = Profile
        fields = ('name', 'email', 'posts')


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'name', 'email', 'body', 'postId')


class PostCommentsSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ('title', 'body', 'userId', 'comments', 'owner')
