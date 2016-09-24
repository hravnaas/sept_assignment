from django.shortcuts import render,redirect
from django.core.urlresolvers import reverse
from django.db.models import Sum
from .models import User, Poke
from ..login_reg.models import User

def poke(request, poke_target_id):
    Poke.objects.poke(poke_target_id, request.session['userID'])
    return redirect(reverse('poke:index'))

def index(request):
    if "userID" not in request.session:
        # Prevent user from going to the success page if not logged in.
        return redirect(reverse('useradmin:index'))

    # User is logged in. Get the current status of pokes.
    context = {
        "alias" : User.objects.get(id = request.session['userID']).alias,
        "userPokes" : Poke.objects.getAllMyPokes(request.session['userID']),
        "pokeHistory" : Poke.objects.getPokeHistory(request.session['userID'])
    }
    return render(request, 'sept_assignment/pokes.html', context)
