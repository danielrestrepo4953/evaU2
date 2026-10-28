from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.RunSQL(
            sql=(
                'ALTER TABLE auth_user '
                'ADD UNIQUE INDEX auth_user_email_unique (email);'
            ),
            reverse_sql=(
                'ALTER TABLE auth_user '
                'DROP INDEX auth_user_email_unique;'
            ),
        ),
    ]