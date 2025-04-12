from django.db import models  # noqa F401


class Pokemon(models.Model):
    title = models.CharField('Название', max_length=200)
    title_en = models.CharField('Название на английском', max_length=200, blank=True)
    title_jp = models.CharField('Название на японском', max_length=200, blank=True)
    photo = models.ImageField('Изображение', upload_to='pokemon_photos')
    description = models.TextField('Описание', blank=True)
    previous_evolution = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        related_name='next_evolutions',
        verbose_name='Предыдущее поколение',
        blank=True,
        null=True,
    )

    def __str__(self):
        return f'{self.title}'
    

class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(
        Pokemon,
        on_delete=models.CASCADE, 
        related_name='entities',
        verbose_name='Разновидность покемона'
    )
    lat = models.FloatField('Координаты широты')
    lon = models.FloatField('Координаты долготы')
    appeared_at = models.DateTimeField('Время появления', blank=True, null=True)
    disappeared_at = models.DateTimeField('Время исчезновения', blank=True, null=True)
    level = models.PositiveSmallIntegerField('Уровень', blank=True, null=True)
    health = models.PositiveSmallIntegerField('Здоровье', blank=True, null=True)
    strength = models.PositiveSmallIntegerField('Сила', blank=True, null=True)
    defence = models.PositiveSmallIntegerField('Защита', blank=True, null=True)
    stamina = models.PositiveSmallIntegerField('Выносливость', blank=True, null=True)

