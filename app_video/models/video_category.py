from django.db import models


class VideoCategory(models.TextChoices):
    """
    Enumeration of available video categories.

    Used as choices for categorizing Video objects in the database.
    """
    ACTION = 'action', 'Action'
    COMEDY = 'comedy', 'Comedy'
    DOCUMENTARY = 'documentary', 'Documentary'
    DRAMA = 'drama', 'Drama'
    HORROR = 'horror', 'Horror'