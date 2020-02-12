from rest_framework import serializers
from .models import *

#   {    this format is only use for 1 model fields , if we want other model's field  we have to add fieldsof other model by take any relation between them.



# class ProfileSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = '__all__'
#                                                                }


# other models fields  added here by calling 1 serializer to other  
class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()  
    user_first_name = serializers.SerializerMethodField()
    user_last_name = serializers.SerializerMethodField()
    user_email = serializers.SerializerMethodField()
    user_username = serializers.SerializerMethodField()
    user_password = serializers.SerializerMethodField()


    def get_user(self, obj):
        user = User.objects.get(pk=obj.user.id)
        return int(user.pk)

    def get_user_first_name(self, obj):
        user = User.objects.get(pk=obj.user.id)
        return user.first_name

    def get_user_last_name(self, obj):
        user = User.objects.get(pk=obj.user.id)
        return user.last_name

    def get_user_email(self, obj):
        user = User.objects.get(pk=obj.user.id)
        return user.email

    def get_user_username(self, obj):
        user = User.objects.get(pk=obj.user.id)
        return user.username

    def get_user_password(self, obj):
        user = User.objects.get(pk=obj.user.id)
        return user.password


    class Meta:
        model = Profile
        fields = '__all__'


#Method 1:
# -> Create Method for each fields.
# -> User Another serializer