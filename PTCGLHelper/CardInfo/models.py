from django.db import models

# Create your models here.
class PokemonCard(models.Model):
    card_name = models.CharField(max_length=30, verbose_name='卡片名稱', blank=True, null=True)
    evolve_marker = models.CharField(max_length=10, verbose_name='進化類別', blank=True, null=True)
    card_hp = models.CharField(max_length=10, verbose_name='卡片血量', blank=True, null=True)
    Type = models.CharField(max_length=10, verbose_name='屬性', blank=True, null=True)
    Weakness = models.CharField(max_length=10, verbose_name='弱點', blank=True, null=True)
    Resistance = models.CharField(max_length=10, verbose_name='抵抗', blank=True, null=True)
    Escape = models.CharField(max_length=10, verbose_name='撤退', blank=True, null=True)
    description = models.TextField(verbose_name='說明', blank=True, null=True)
    card_alpha = models.CharField(max_length=100, verbose_name='發行盒號', blank=True, null=True)
    card_rule = models.CharField(max_length=200, verbose_name='卡標', blank=True, null=True)
    card_number = models.CharField(max_length=100, verbose_name='編號', blank=True, null=True)
    web_url = models.CharField(max_length=200, verbose_name='路徑', blank=True, null=True)
    web_id = models.CharField(max_length=100, verbose_name='路徑id', blank=True, null=True)

    def __str__(self):
        return f'{self.card_name} ({self.evolve_marker})'
    

class PokemonCardSkill(models.Model):
    card = models.ForeignKey(PokemonCard, on_delete=models.CASCADE, related_name='skills', verbose_name='卡片')
    skill_type = models.CharField(max_length=10, verbose_name='種類' ,blank=True, null=True)
    skill_name = models.CharField(max_length=100, verbose_name='名稱' ,blank=True, null=True)
    skill_cost = models.CharField(max_length=100, verbose_name='能量' ,blank=True, null=True)
    skill_damage = models.CharField(max_length=100, verbose_name='傷害',blank=True, null=True)
    skill_effect = models.CharField(max_length=1000, verbose_name='特效' ,blank=True, null=True)
    
    def __str__(self):
        return f'{self.skill_name} ({self.skill_type})'
    
