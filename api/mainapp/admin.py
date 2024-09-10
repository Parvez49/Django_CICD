from django.contrib import admin
from django.contrib.auth.models import Group
from .models import Profile, Post, Comment, UserPreference

admin.site.unregister(Group)


# profile info along with user
class ProfileInLine(admin.StackedInline):
    model = Profile


# class UserAdmin(admin.ModelAdmin):
#     model = User
#     #fields = ["usename"]
#     inlines = [ProfileInLine]

# # Unregister initial user
# admin.site.unregister(User)

# # Register user and profile.
# admin.site.register(User, UserAdmin)
admin.site.register(Profile)

# register Post
admin.site.register(Post)

# register posts comments
admin.site.register(Comment)

# register usr preference
admin.site.register(UserPreference)
