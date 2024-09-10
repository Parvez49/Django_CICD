from rest_framework import serializers
from account.models import User
from .models import UserPost, PostFile, Comment


class PostUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email", "fname", "lname")


class CommentSerializer(serializers.ModelSerializer):
    user = PostUserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ("id", "user", "body", "created_at")


class PostFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostFile
        fields = ["id", "post", "file"]


class UserPostSerializer(serializers.ModelSerializer):
    user = PostUserSerializer(read_only=True)
    # files = PostFileSerializer(many=True, read_only=True)
    files = PostFileSerializer(many=True, read_only=True)  # Read-only for GET requests
    files_input = serializers.ListField(
        child=serializers.FileField(), write_only=True, required=False
    )

    class Meta:
        model = UserPost
        fields = [
            "id",
            "user",
            "body",
            "likes",
            "loves",
            "share",
            "files",
            "files_input",
            "created_at",
        ]

    def create(self, validated_data):
        files = validated_data.pop("files_input", [])
        user_post = super().create(validated_data)
        for file in files:
            PostFile.objects.create(post=user_post, file=file)
        return user_post

    def update(self, instance, validated_data):
        files = validated_data.pop("files_input", [])
        instance = super().update(instance, validated_data)
        if files:
            instance.files.all().delete()
            for file in files:
                PostFile.objects.create(post=instance, file=file)
        return instance

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["loves"] = instance.number_of_loves()
        data["likes"] = instance.number_of_likes()
        data["share"] = instance.number_of_share()

        return data


class PostDetailSerializer(serializers.ModelSerializer):
    user = PostUserSerializer(read_only=True)
    files = PostFileSerializer(many=True, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = UserPost
        fields = [
            "id",
            "user",
            "body",
            "likes",
            "loves",
            "share",
            "files",
            "comments",
            "created_at",
        ]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["loves"] = instance.number_of_loves()
        data["likes"] = instance.number_of_likes()
        data["share"] = instance.number_of_share()

        return data


# class UserPostSerializer(serializers.ModelSerializer):
#     # files = PostFileSerializer(many=True, read_only=True)
#     # number_of_likes = serializers.SerializerMethodField()
#     # number_of_loves = serializers.SerializerMethodField()
#     # number_of_shares = serializers.SerializerMethodField()

#     class Meta:
#         model = UserPost
#         fields = ['id', 'user', 'body', 'likes', 'loves', 'share']


#     def to_representation(self, instance):
#         data = super().to_representation(instance)
#         data['loves'] = instance.number_of_loves()
#         data['likes'] = instance.number_of_loves()
#         data['share'] = instance.number_of_share()

#         return data

#     # def get_number_of_likes(self, obj):
#     #     return obj.number_of_likes()
