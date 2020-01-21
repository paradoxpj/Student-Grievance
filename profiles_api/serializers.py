from rest_framework import serializers

from profiles_api import models


class HelloSerializer(serializers.Serializer):
    '''Serializes a name field for testing our API view'''
    name = serializers.CharField(max_length=10)


class UserProfileSerializer(serializers.ModelSerializer):
    '''Serializes a user profile model'''

    class Meta:
        model = models.UserProfile
        fields = ('id', 'email', 'name', 'password')
        extra_kwargs = {
            'password': {
                'write_only': True,
                'style': {'input_type': 'password'}
            }
        }

    def create(self, validated_data):
        '''Create and return a new user'''
        user = models.UserProfile.objects.create_user(
            email=validated_data['email'],
            name=validated_data['name'],
            password=validated_data['password'],
        )

        return user


class ProfileFeedItemSerializer(serializers.ModelSerializer):
    '''serializes profile feed items'''

    class Meta:
        model = models.ProfileFeedItem
        fields = ('id', 'user_profile', 'status_text', 'created_on',)
        extra_kwargs = {
            'user_profile': {
                'read_only': True,
            }
        }


class IssueSerializer(serializers.ModelSerializer):
    '''serializes issues'''

    class Meta:
        model = models.Issue
        fields = ('id', 'name',)


class CollegeSerializer(serializers.ModelSerializer):
    '''serializes list of colleges'''

    class Meta:
        model = models.College
        fields = ('id', 'name', 'location',)
