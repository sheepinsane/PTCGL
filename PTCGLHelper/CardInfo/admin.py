from django.contrib import admin
from .models import PokemonCard, PokemonCardSkill
# Register your models here.

admin.site.register(PokemonCard)
admin.site.register(PokemonCardSkill)