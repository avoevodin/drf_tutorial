from django.db import models
from datetime import date


class Category(models.Model):
    """Category

    """

    name = models.CharField('Category', max_length=150)
    description = models.TextField('Description')
    url = models.SlugField(max_length=160, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Actor(models.Model):
    """Actors

    """
    name = models.CharField('Category', max_length=100)
    age = models.PositiveSmallIntegerField('Age', default=0)
    description = models.TextField('Description')
    image = models.ImageField('Image', upload_to='actors/')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Actors and directors'
        verbose_name_plural = 'Actors and directors'


class Genre(models.Model):
    """Genre

    """
    name = models.CharField('Name', max_length=100)
    description = models.TextField('Description')
    url = models.SlugField(max_length=160, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Genre'
        verbose_name_plural = 'Genres'


class Movie(models.Model):
    """Movie

    """
    title = models.CharField('Title', max_length=100)
    tagline = models.CharField('Tagline', max_length=100, default='')
    description = models.TextField('Description')
    poster = models.ImageField('Poster', upload_to="movies/")
    year = models.PositiveSmallIntegerField('Release date', default=2021)
    country = models.CharField('Country', max_length=30)
    directors = models.ManyToManyField(
        Actor, verbose_name='directors', related_name='film_director'
    )
    actors = models.ManyToManyField(
        Actor, verbose_name='actors', related_name='film_actor'
    )
    genres = models.ManyToManyField(Genre, verbose_name='genres')
    world_premiere = models.DateField('World premiere', default=date.today)
    budget = models.PositiveIntegerField(
        'Budget', default=0, help_text='Enter the amount in dollars'
    )
    fees_in_usa = models.PositiveIntegerField(
        'Fees in USA', default=0, help_text='Enter the amount in dollars'
    )
    fees_in_world = models.PositiveIntegerField(
        'Fees in the World', default=0, help_text='Enter the amount in dollars'
    )
    category = models.ForeignKey(
        Category, verbose_name='Category', on_delete=models.SET_NULL, null=True
    )
    url = models.SlugField(max_length=160, unique=True)
    draft = models.BooleanField('Draft', default=False)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Movie'
        verbose_name_plural = 'Movie'


class MovieShots(models.Model):
    """Movie shots

    """
    title = models.CharField('Title', max_length=100)
    description = models.TextField('Description')
    image = models.ImageField('Image', upload_to='actors/')
    movie = models.ForeignKey(Movie, verbose_name='Movie', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Movie shot'
        verbose_name_plural = 'Movie shots'


class RatingStar(models.Model):
    """Rating star

    """
    value = models.SmallIntegerField('Value', default=0)

    def __str__(self):
        return self.value

    class Meta:
        verbose_name = 'Rating star'
        verbose_name_plural = 'Rating stars'


class Rating(models.Model):
    """Rating

    """
    ip = models.CharField('IP', max_length=15)
    star = models.ForeignKey(RatingStar, on_delete=models.CASCADE, verbose_name='star')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, verbose_name='movie')

    def __str__(self):
        return f'{self.star} - {self.movie}'

    class Meta:
        verbose_name = 'Rating'
        verbose_name_plural = 'Ratings'


class Review(models.Model):
    """Reviews

    """
    email = models.EmailField()
    name = models.CharField('Name', max_length=100)
    text = models.TextField('Text', max_length=5000)
    parent = models.ForeignKey(
        'self', verbose_name='Parent', on_delete=models.SET_NULL,
        blank=True, null=True
    )
    movie = models.ForeignKey(
        Movie, verbose_name='movie', on_delete=models.CASCADE,
        related_name='reviews',
    )

    def __str__(self):
        return f'{self.name} - {self.movie}'

    class Meta:
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'
