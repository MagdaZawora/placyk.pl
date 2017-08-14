from django.db import models
from datetime import datetime
#from django.utils import datetime
from django.forms import widgets
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

QUARTER = (('not defined', 0),
           ('Bronowice Małe', 1),
           ('Krowodrza', 2),
           ('Nowa Huta', 3))

AGE = ((-1, 'not defined'),
       (0, '0 - 1'),
       (1, '1'),
       (2, '2'),
       (3, '3'),
       (4, '4'),
       (5, '5'),
       (6, '6'))

SEX = ((1, 'dziewczynka'),
       (2, 'chłopiec'))


class Quarter(models.Model):
    name = models.CharField(max_length=64, choices=QUARTER, default='not defined')

    def __str__(self):
        return str(self.name)


class Pground(models.Model):
    place = models.CharField(max_length=128)
    description = models.TextField()
    quarter = models.ForeignKey(Quarter)

    def __str__(self):
        return 'placyk {} w dzielnicy {}'.format(self.place, self.quarter)


class Child(models.Model):
    name = models.CharField(max_length=128)
    age = models.IntegerField(choices=AGE, default=-1)
    sex = models.IntegerField(choices=SEX, default=1)
    whose_child = models.ForeignKey(User, related_name='children')

    def __str__(self):
        return '{}, {} lat'.format(self.name, self.age)


class Parent(models.Model):
    user = models.OneToOneField(User)
    quarter = models.ForeignKey(Quarter)
    children = models.ManyToManyField(Child)


    @property
    def how_many_children(self):
        return self.children.count()

    def __str__(self):
        return self.user.username


class Visit(models.Model):
    who = models.ForeignKey(User)
    pground = models.ForeignKey(Pground)
    time_from = models.DateTimeField()
    time_to = models.DateTimeField()

    def __str__(self):
        return '{} na placyku {} od {} do {}'.format(self.who, self.pground,
                                                                               self.time_from, self.time_to)


class Message(models.Model):
    sender = models.ForeignKey(User)
    receiver = models.ForeignKey(User, related_name="message_receiver")
    content = models.TextField()
    creation_date = models.DateTimeField(default=datetime.now)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return 'Message from {} to {} @ {}'.format(self.sender, self.receiver, self.creation_date)
