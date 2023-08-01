import datetime

from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Address(models.Model):
    city = models.CharField(max_length=128, db_column="city", null=False, blank=False)
    street = models.CharField(max_length=128, db_column="street", null=False, blank=False)
    house_number = models.CharField(max_length=20, db_column="house_number", null=False, blank=False)
    floor_number = models.IntegerField(db_column="floor_number", null=True, blank=True)

    def __str__(self):
        return f"{self.street}, {self.house_number}, {self.city}"

    class Meta:
        db_table = 'address'


# validators
def validate_birth_date(val):
    if datetime.datetime.today().year - val < 18:
        raise ValidationError("User must be at least 18 years old")


class UserDetails(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    phone_number = models.CharField(max_length=20, db_column="phone_number", null=False, blank=False)
    address = models.ForeignKey(Address, on_delete=models.RESTRICT)
    birth_year = models.IntegerField(db_column='birth_year', null=False, validators=[validate_birth_date])

    def __str__(self):
        return self.user.name

    class Meta:
        db_table = 'user_details'


class Child(models.Model):
    user = models.ForeignKey(User, on_delete=models.RESTRICT)
    child_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=128, db_column="child_name", null=False, blank=False)
    age = models.FloatField()
    kindergarten = models.CharField(max_length=128, db_column="kindergarten", null=True, blank=True)
    school = models.CharField(max_length=128, db_column="school", null=True, blank=True)
    classroom = models.CharField(max_length=128, db_column="classroom", null=True, blank=True)
    interests = models.ManyToManyField('Interests', through='ChildInterests')
    events = models.ManyToManyField('Event', through='ChildEvent')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'children'


class Event(models.Model):
    event_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=128, db_column="title", null=False, blank=False)
    description = models.TextField(db_column='description', null=True, blank=False)
    start_event = models.DateTimeField(db_column="start_event", null=False, blank=False)
    end_event = models.DateTimeField(db_column="end_event", null=False, blank=False)
    location = models.CharField(max_length=128, db_column="location", null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'event'


class ChildEvent(models.Model):
    child = models.ForeignKey(Child, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.child.name} in event {self.event.name}"

    class Meta:
        db_table = 'child_event'


class Interests(models.Model):
    interest_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=128, db_column="name", null=False, blank=False)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'interests'


class ChildInterests(models.Model):
    child = models.ForeignKey(Child, on_delete=models.CASCADE)
    interest = models.ForeignKey(Interests, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.child.name} the kid's area of interest: {self.interest.name}"

    class Meta:
        db_table = 'children_interests'


class Schedule(models.Model):
    child = models.ForeignKey(Child, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    type_activity = models.CharField(max_length=128, db_column="type_activity", null=False, blank=False)

    def __str__(self):
        return f"Child: {self.child.name} schedule"

    class Meta:
        db_table = 'schedule'







