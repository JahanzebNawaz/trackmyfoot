
from django.contrib.auth.models import  Group
from django.db.models import fields
from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from rest_framework.authtoken.models import Token
from .models import Goal, GoalDetails


User = get_user_model()


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        # fields = ['url','username','email', 'first_name', 'last_name', 'phone_no', 'date_of_birth', 'profile_image']
        # fields = "__all__"
        extra_kwargs = {'password': {'write_only': True, 'required': True}}
        lookup_field = 'username'
        exclude = ('user_permissions',)


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']
    


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        
        user.set_password(validated_data['password'])
        user.save()

        Token.objects.create(user=user)
        return user


class GoalSerializer(serializers.HyperlinkedModelSerializer):
    # user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=False)  
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Goal
        fields = '__all__'



class GoalDetailSerializer(serializers.HyperlinkedModelSerializer):
    goal = serializers.PrimaryKeyRelatedField(queryset=Goal.objects.all(), many=False)  
    user = serializers.ReadOnlyField(source='user.username')
    
    class Meta:
        model = GoalDetails
        fields = '__all__'
