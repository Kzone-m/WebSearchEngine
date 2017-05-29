from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404
from .forms import ScrapingForm
from .scraping import scraping
from .models import Url, Index

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

            for url in index[key]:
                if not Url.objects.filter(url=url, index=target_index).exists():
                    Url.objects.create(url=url, index=target_index)

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