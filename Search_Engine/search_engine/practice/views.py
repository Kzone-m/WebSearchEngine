from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404
from .forms import BaseballPlayerAddForm
from .models import BaseballPlayer


def practice_list(request):
    players = BaseballPlayer.objects.all()
    d = {
        'players': players
    }
    return render(request, 'practice/practice_list.html', d)


def practice_add(request):
    # print(request.POST)
    # <QueryDict: {'name': ['SODA'], 'csrfmiddlewaretoken': ['CMT7k0f0ZAXK7sgrNwe2n5O4mQO4rRGxJ1Jb8L0E5RnGHmTBmCwW8igRWRpVNjkm'], 'position': ['Catcher'], 'yearly_pay': ['1000']}>
    # print(request.POST['name'])
    # SODA
    # print(request.POST['position'])
    # ['Catcher']

    if request.method == 'POST':
        form = BaseballPlayerAddForm(request.POST or None)
        if form.is_valid():
            # print(form.cleaned_data)
            # {'name': 'TPON', 'team': <Team: A1>, 'position': 'Outfielder', 'yearly_pay': 1000}
            name = form.cleaned_data.get('name')
            team = form.cleaned_data.get('team')
            count = BaseballPlayer.objects.filter(team=team).filter(name__contains=name).count()

            if count == 0:
                form.save()
                return HttpResponseRedirect(reverse('practice_list'))

    form = BaseballPlayerAddForm()

    d = {
        'form': form,
    }
    return render(request, 'practice/practice_add.html', d)


def practice_edit(request, id):
    try:
        player = BaseballPlayer.objects.get(id=id)
    except BaseballPlayer.DoesNotExist:
        raise Http404

    if request.method == 'POST':
        form = BaseballPlayerAddForm(request.POST, instance=player)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('practice_list'))

    form = BaseballPlayerAddForm(instance=player)
    d = {
        'form': form
    }
    return render(request, 'practice/practice_edit.html', d)


def practice_delete(request, id):
    try:
        player = BaseballPlayer.objects.get(id=id)
    except BaseballPlayer.DoesNotExist:
        raise Http404

    player.delete()
    return HttpResponseRedirect(reverse('practice_list'))