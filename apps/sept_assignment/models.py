from __future__ import unicode_literals
from django.db import models
from django.db.models import Sum, Count, Avg
from ..login_reg.models import User


############### Poke ###############

class PokeMgr(models.Manager):
    def poke(self, target_id, userID):
        # Check if there is a poke history for the people involved.
        pokeEntry = Poke.objects.filter(poke_source_id = userID) & Poke.objects.filter(poke_target_id = target_id)

        if len(pokeEntry) > 0:
            # Poke history exists. Update it.
            pokeEntry[0].num_pokes+= 1
            pokeEntry[0].save()
            return

        # No poke history present. Add it.
        pokeEntry = Poke.objects.create(
                poke_source = User.objects.get(id = userID),
                poke_target = User.objects.get(id = target_id),
                num_pokes = 1
            )
        return

    # Returns all pokes that were targeted towards logged in user.
    def getAllMyPokes(self, userID):
        return Poke.objects.filter(poke_target_id = userID).exclude(poke_source_id = userID)

    # Return all pokes targeted towards other people (not logged in user).
    # Results are grouped by the user ID and the num_pokes summed up.
    def getPokeHistory(self, userID):
        return User.objects.exclude(id = userID).annotate(tot_pokes=Sum('poke_targets__num_pokes'))

class Poke(models.Model):
    poke_source = models.ForeignKey(User, related_name='poke_sources')
    poke_target = models.ForeignKey(User, related_name='poke_targets')
    num_pokes = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = PokeMgr()
