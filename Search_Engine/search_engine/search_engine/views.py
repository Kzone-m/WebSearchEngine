from django.http import JsonResponse
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404
from .forms import ScrapingForm, LookUpForm
from .scraping import scraping
from .models import Url, Index
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions


class AjaxData(APIView):
    # authentication_classes = (authentication.TokenAuthentication,)
    # permission_classes = (permissions.IsAdminUser,)
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        # usernames = [user.username for user in User.objects.all()]
        # return Response(usernames)
        # http://127.0.0.1:8000/api/ajax/data/?param1=a
        keyword = ""
        parameter = request.query_params    # <QueryDict: {'param1': ['a']}>
        for index in parameter:
            keyword = parameter[index]

        print(keyword)
        data = [
            {'sales':100, 'customers': 10},
            {'sales':200, 'customers': 20},
        ]
        indexes = Index.objects.filter(index__contains=keyword)
        for index in indexes:
            temp_dict = dict()
            temp_dict[index.index] = {}
            urls = index.url_set.all()
            for url in urls:
                temp_dict[index.index][url.url] = url.title
            data.append(temp_dict)

        return Response(data)


'''
def get_json_data(request):
    data = {
        'sales': 100,
        'customers': 10,
    }
    return JsonResponse(data)
'''


# index: {'A': [url1, url2], 'B': [url1, url2], 'C':[url1, url2]}
# graph: {'base_url': [out_link1, out_link2, ..., out_link_n]}


def scrape(request):
    if request.method == 'POST':
        seed_url = request.POST.get('seed_url')
        max_depth = int(request.POST.get('max_depth'))
        max_capacity = int(request.POST.get('max_capacity'))
        target_html_tag = request.POST.getlist('target_html_tag')
        index, graph = scraping(seed_url, max_depth, max_capacity, target_html_tag)
        for key in index:
            if Index.objects.filter(index = key).exists():
                target_index = Index.objects.get(index = key)
            else:
                target_index = Index.objects.create(index = key)

            for url, title in index[key].items():
                if not Url.objects.filter(index=target_index, url=url, title=title).exists():
                    Url.objects.create(index=target_index, url=url, title=title)

        '''
        後でcleaned_dataをformクラスで再定義する
        form = ScrapingForm(request.POST or None)
        if form.is_valid():
            seed_url = form.cleaned_data['seed_url']
            max_depth = form.cleaned_data['max_depth']
            max_capacity = form.cleaned_data['max_capacity']
            target_html_tag = form.cleaned_data['target_html_tag']
        '''
        # return HttpResponseRedirect(reverse('scrape_result'))
        d = {
            'index': index,
            'graph': graph,
        }
        return render(request, 'scrape_result.html', d)

    form = ScrapingForm()
    d = {
        'form': form,
    }
    return render(request, 'scrape.html', d)


def scrape_result(request):
    index_dict = {}
    indexes = Index.objects.all()
    for index in indexes:
        index_dict[index] = []
        urls = index.url_set.all()
        for url in urls:
            index_dict[index].append(url)
    d = {
        'index': index_dict,
    }
    return render(request, 'scrape_result.html', d)


def look_up(request):
    form = LookUpForm()
    d = {
        'form': form,
    }
    return render(request, 'look_up.html', d)


def look_up_result(request):
    d = {}
    if request.method == 'POST':
        form = LookUpForm(request.POST or None)
        if form.is_valid():
            query = form.cleaned_data.get('query')
            indexes = Index.objects.filter(index__contains=query)
            print("indexes:", indexes)
            for index in indexes:
                for url in index.url_set.all():
                    print(url.url)
            d = {
                'indexes': indexes,
                'form': LookUpForm(),
            }
    d = {
        'form': LookUpForm(),
    }
    return render(request, 'look_up_result.html', d)