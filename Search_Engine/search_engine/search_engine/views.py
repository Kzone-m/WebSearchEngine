from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404
from .forms import ScrapingForm
from .scraping import scraping


def scrape(request):
    if request.method == 'POST':
        seed_url = request.POST.get('seed_url')
        max_depth = int(request.POST.get('max_depth'))
        max_capacity = int(request.POST.get('max_capacity'))
        target_html_tag = request.POST.getlist('target_html_tag')
        index, graph = scraping(seed_url, max_depth, max_capacity, target_html_tag)
        # index: {'A': [url1, url2], 'B': [url1, url2], 'C':[url1, url2]}
        # graph: {'base_url': [out_link1, out_link2, ..., out_link_n]}

        '''
        後でcleaned_dataをformクラスで再定義する
        form = ScrapingForm(request.POST or None)
        if form.is_valid():
            seed_url = form.cleaned_data['seed_url']
            max_depth = form.cleaned_data['max_depth']
            max_capacity = form.cleaned_data['max_capacity']
            target_html_tag = form.cleaned_data['target_html_tag']
        '''

    form = ScrapingForm()
    d = {
        'form': form,
    }
    return render(request, 'scrape.html', d)