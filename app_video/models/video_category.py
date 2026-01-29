from django.db import models


class VideoCategory(models.TextChoices):
    ACTION = 'action', 'Action'
    COMEDY = 'comedy', 'Comedy'
    DOCUMENTARY = 'documentary', 'Documentary'
    DRAMA = 'drama', 'Drama'
    HORROR = 'horror', 'Horror'