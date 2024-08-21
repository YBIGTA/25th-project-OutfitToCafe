# Generated by Django 3.2 on 2024-08-21 01:57

import coplate.models
from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('name', models.CharField(default='Unknown', error_messages={'null': '이름을 입력해주세요.'}, max_length=15)),
                ('profile_pic', models.FileField(default='default_profile_pic.jpg', upload_to='profile_pics')),
                ('birth_date', models.DateField(blank=True, error_messages={'null': '생년월일을 입력해주세요.'}, null=True)),
                ('gender', models.IntegerField(choices=[(1, '남자'), (2, '여자')], default=1)),
                ('recommend_location', models.CharField(error_messages={'null': '존재하지 않는 역입니다.'}, max_length=100)),
                ('following', models.ManyToManyField(blank=True, related_name='followers', to=settings.AUTH_USER_MODEL)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Cafe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=100)),
                ('address_url', models.URLField(null=True)),
                ('total_review', models.IntegerField(null=True)),
                ('sns_link', models.URLField(null=True)),
                ('image1', models.ImageField(blank=True, upload_to=coplate.models.cafe_image_upload_to)),
                ('image2', models.ImageField(blank=True, upload_to=coplate.models.cafe_image_upload_to)),
                ('image3', models.ImageField(blank=True, upload_to=coplate.models.cafe_image_upload_to)),
                ('image4', models.ImageField(blank=True, upload_to=coplate.models.cafe_image_upload_to)),
                ('image5', models.ImageField(blank=True, upload_to=coplate.models.cafe_image_upload_to)),
                ('rating', models.DecimalField(blank=True, decimal_places=1, max_digits=4, null=True)),
                ('short_description', models.CharField(max_length=500)),
                ('content', models.TextField(max_length=500)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cafes', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='StyleKeyword',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('keyword', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dt_created', models.DateTimeField(auto_now_add=True)),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likes', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Dripshot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('image1', models.FileField(upload_to=coplate.models.dripshot_pic_upload_to)),
                ('image1_url', models.URLField()),
                ('image2', models.FileField(blank=True, upload_to=coplate.models.dripshot_pic_upload_to)),
                ('image2_url', models.URLField(blank=True)),
                ('image3', models.FileField(blank=True, upload_to=coplate.models.dripshot_pic_upload_to)),
                ('image3_url', models.URLField(blank=True)),
                ('image4', models.FileField(blank=True, upload_to=coplate.models.dripshot_pic_upload_to)),
                ('image4_url', models.URLField(blank=True)),
                ('image5', models.FileField(blank=True, upload_to=coplate.models.dripshot_pic_upload_to)),
                ('image5_url', models.URLField(blank=True)),
                ('dt_created', models.DateTimeField(auto_now_add=True)),
                ('dt_updated', models.DateTimeField(auto_now=True)),
                ('content', models.TextField(max_length=500)),
                ('rating', models.IntegerField(blank=True, choices=[(1, '★'), (2, '★★'), (3, '★★★'), (4, '★★★★'), (5, '★★★★★')], default=None, null=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dripshot', to=settings.AUTH_USER_MODEL)),
                ('cafe', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='dripshots', to='coplate.cafe')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(max_length=500)),
                ('dt_created', models.DateTimeField(auto_now_add=True)),
                ('dt_updated', models.DateTimeField(auto_now=True)),
                ('object_id', models.PositiveIntegerField(default=1)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to=settings.AUTH_USER_MODEL)),
                ('content_type', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
            ],
            options={
                'ordering': ['-dt_created'],
            },
        ),
        migrations.AddField(
            model_name='cafe',
            name='style_keywords',
            field=models.ManyToManyField(blank=True, related_name='cafes', to='coplate.StyleKeyword'),
        ),
        migrations.AddField(
            model_name='user',
            name='style_keywords',
            field=models.ManyToManyField(blank=True, related_name='users', to='coplate.StyleKeyword'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
        migrations.AddConstraint(
            model_name='like',
            constraint=models.UniqueConstraint(fields=('user', 'content_type', 'object_id'), name='unique_like'),
        ),
    ]
