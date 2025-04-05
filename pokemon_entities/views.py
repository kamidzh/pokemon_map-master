import folium

from django.http import HttpResponseNotFound
from django.shortcuts import render, get_object_or_404
from django.utils.timezone import localtime

from pokemon_entities.models import Pokemon, PokemonEntity


MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        # Warning! `tooltip` attribute is disabled intentionally
        # to fix strange folium cyrillic encoding bug
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon_entity in PokemonEntity.objects.filter(appeared_at__lt=localtime(), disappeared_at__gt=localtime()):
        if pokemon_entity.pokemon.photo:
            photo = request.build_absolute_uri(pokemon_entity.pokemon.photo.url)
        else:
            photo = DEFAULT_IMAGE_URL
        add_pokemon(
            folium_map, pokemon_entity.lat,
            pokemon_entity.lon,
            photo
        )
    pokemons_on_page = []
    pokemons = Pokemon.objects.all()
    for pokemon in pokemons:
        pokemon_description = {
            'pokemon_id' : pokemon.id,
            'title_ru' : pokemon.title
        }
        if pokemon.photo:
            pokemon_description['img_url'] = request.build_absolute_uri(pokemon.photo.url)
        else:
            pokemon_description['img_url'] = DEFAULT_IMAGE_URL
        pokemons_on_page.append(pokemon_description)


    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    requested_pokemon = get_object_or_404(Pokemon, id=pokemon_id)
    
    pokemon_description = {
        'pokemon_id' : requested_pokemon.id,
        'title_ru' : requested_pokemon.title,
        'title_en' : requested_pokemon.title_en,
        'title_jp' : requested_pokemon.title_jp,
        'description' : requested_pokemon.description,
    }
    previous_evolution = requested_pokemon.previous_evolution
    if previous_evolution:
        pokemon_description['previous_evolution'] = {
            'title_ru' : previous_evolution.title,
            'pokemon_id' : previous_evolution.id
        }
        if previous_evolution.photo:
            pokemon_description['previous_evolution']['img_url'] = request.build_absolute_uri(previous_evolution.photo.url)
        else:
            pokemon_description['previous_evolution']['img_url'] = DEFAULT_IMAGE_URL
    next_evolutions = requested_pokemon.next_evolutions.all()
    if next_evolutions:
        next_pokemon = next_evolutions[0]
        pokemon_description['next_evolution'] = {
            'title_ru' : next_pokemon.title,
            'pokemon_id' : next_pokemon.id
        }
        if next_pokemon.photo:
            pokemon_description['next_evolution']['img_url'] = request.build_absolute_uri(next_pokemon.photo.url)
        else:
            pokemon_description['next_evolution']['img_url'] = DEFAULT_IMAGE_URL
    if requested_pokemon.photo:
        pokemon_description['img_url'] = request.build_absolute_uri(requested_pokemon.photo.url)
    else:
        pokemon_description['img_url'] = DEFAULT_IMAGE_URL
    
    pokemon_entitites = PokemonEntity.objects.filter(pokemon=requested_pokemon)
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon_entity in pokemon_entitites:
        if pokemon_entity.pokemon.photo:
            photo = request.build_absolute_uri(pokemon_entity.pokemon.photo.url)
        else:
            photo = DEFAULT_IMAGE_URL
        add_pokemon(
            folium_map, pokemon_entity.lat,
            pokemon_entity.lon,
            photo
        )

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': pokemon_description
    })
