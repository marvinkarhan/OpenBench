from django.db import migrations


def create_initial_users(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    Profile = apps.get_model('OpenBench', 'Profile')

    # Create admin user
    admin_username = 'admin'
    admin_email = ''
    admin_password_hash = 'pbkdf2_sha256$600000$tG6pK7Ee1suVkkMrAPVvNt$cr05C+fBlTAvdWhF3xh/FzPaiFpbtJQkxa9+XZl2iRI='

    admin_user, created = User.objects.get_or_create(
        username=admin_username,
        defaults={
            'email': admin_email,
            'password': admin_password_hash,
            'is_staff': True,
            'is_superuser': True,
            'is_active': True,
        },
    )

    # Ensure password and flags are correct if user pre-exists
    if not created:
        admin_user.email = admin_email
        admin_user.password = admin_password_hash
        admin_user.is_staff = True
        admin_user.is_superuser = True
        admin_user.is_active = True
        admin_user.save()

    Profile.objects.update_or_create(
        user_id=admin_user.id,
        defaults={
            'enabled': True,
            'approver': True,
        },
    )

    # Create regular user
    user_username = 'marvin'
    user_email = ''
    user_password_hash = 'pbkdf2_sha256$600000$WmemcDM6U4MOfH4Wuotj0r$GxANGrrByVYXXxKpbcfyJfIXPY9pxUmrhB66ya7lTw4='

    reg_user, created = User.objects.get_or_create(
        username=user_username,
        defaults={
            'email': user_email,
            'password': user_password_hash,
            'is_staff': False,
            'is_superuser': False,
            'is_active': True,
        },
    )

    if not created:
        reg_user.email = user_email
        reg_user.password = user_password_hash
        reg_user.is_active = True
        reg_user.is_staff = False
        reg_user.is_superuser = False
        reg_user.save()

    Profile.objects.update_or_create(
        user_id=reg_user.id,
        defaults={
            'enabled': True,
            'approver': False,
        },
    )


def remove_initial_users(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    Profile = apps.get_model('OpenBench', 'Profile')
    for username in ['admin', 'user']:
        try:
            user = User.objects.get(username=username)
            Profile.objects.filter(user_id=user.id).delete()
            user.delete()
        except User.DoesNotExist:
            pass


class Migration(migrations.Migration):
    dependencies = [
        ('OpenBench', '0001_initial'),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.RunPython(create_initial_users, remove_initial_users),
    ]


