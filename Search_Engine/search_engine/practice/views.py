from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseRedirect, Http404
from .forms import BaseballPlayerAddForm, BaseballPlayerSearchForm
from .models import BaseballPlayer


def practice_list(request):
    # Viewに表示するために、DBに格納されている野球選手を全て取得
    players = BaseballPlayer.objects.all()

    # 野球選手検索用のformを作成し、もし検索条件用のQuery情報が送られてきたならばfilter_player_functionに情報を渡してDBで条件を絞り込む
    form = BaseballPlayerSearchForm(request.GET)
    players = form.filter_players(players)

    # 野球選手を表示するためのViewをPaginatorを使って分割し、もし例外が発生しそうなら、1ページ目を返す
    # 検索条件用のQuery情報があった場合に、その情報をPaginatorに引き継ぐためにrequest.GETからpage以外のparameter情報を取得してViewに渡す
    paginator = Paginator(players, 5)
    params = request.GET.copy()
    if 'page' in params:
        page = params['page']
        del params['page']
    else:
        page = 1

    search_params = params.urlencode()    # urlencode()はクエリーパラメーターの文字列に変換するメソッド

    try:
        players = paginator.page(page)
    except (PageNotAnInteger, EmptyPage):
        players = paginator.page(1)

    # practice_list.htmlで実際に使われる情報をdに格納する
    d = {
        'form': form,
        'players': players,
        'search_params': search_params,
    }
    return render(request, 'practice/practice_list.html', d)


def practice_add(request):

    # もしrequest.methodがPOSTなら、Query情報をクリーニングしてDBに格納する
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
    # print(request.POST)
    # <QueryDict: {'name': ['SODA'], 'csrfmiddlewaretoken': ['CMT7k0f0ZAXK7sgrNwe2n5O4mQO4rRGxJ1Jb8L0E5RnGHmTBmCwW8igRWRpVNjkm'], 'position': ['Catcher'], 'yearly_pay': ['1000']}>
    # print(request.POST['name'])
    # SODA
    # print(request.POST['position'])
    # ['Catcher']


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