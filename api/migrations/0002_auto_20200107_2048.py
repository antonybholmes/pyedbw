# Generated by Django 3.0 on 2020-01-07 20:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='sampleperson',
            name='person',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='sampleperson',
            name='role',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to='api.Role'),
        ),
        migrations.AddField(
            model_name='sampleperson',
            name='sample',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Sample'),
        ),
        migrations.AddField(
            model_name='samplegroup',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth.Group'),
        ),
        migrations.AddField(
            model_name='samplegroup',
            name='sample',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Sample'),
        ),
        migrations.AddField(
            model_name='samplefile',
            name='sample',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Sample'),
        ),
        migrations.AddField(
            model_name='samplefile',
            name='vfs',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.VFSFile'),
        ),
        migrations.AddField(
            model_name='sample',
            name='groups',
            field=models.ManyToManyField(through='api.SampleGroup', to='auth.Group'),
        ),
        migrations.AddField(
            model_name='sample',
            name='persons',
            field=models.ManyToManyField(through='api.SamplePerson', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='sample',
            name='sets',
            field=models.ManyToManyField(through='api.SetSample', to='api.Set'),
        ),
        migrations.AddField(
            model_name='person',
            name='groups',
            field=models.ManyToManyField(through='api.GroupPerson', to='api.Group'),
        ),
        migrations.AddField(
            model_name='groupperson',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Group'),
        ),
        migrations.AddField(
            model_name='groupperson',
            name='person',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Person'),
        ),
        migrations.AddField(
            model_name='element',
            name='sample',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Sample'),
        ),
        migrations.AddField(
            model_name='element',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.ElementType'),
        ),
        migrations.AddField(
            model_name='apikey',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
