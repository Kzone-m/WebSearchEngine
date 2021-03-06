import lxml.html, cssselect, re, time, urllib, MeCab
from urllib.parse import urljoin
from urllib.request import urlopen
from reppy.cache import RobotsCache


def confirm_robots_txt(target_url, max_capacity):
    """confirm that target url is allowed to crawl
    
    :type target_url: str
    :param target_url: agent wanna crawl
    :type max_capacity: int
    :param max_capacity: limit of max crawling pages
    :rtype: bool
    :return: weather it is possible to scrape
    """
    robots = RobotsCache(max_capacity)
    return robots.allowed(target_url, 'python program')


def parsing_url(url):
    """access this url, decode its info as html contents, and pass them to parse_url function
    
    :type url: str
    :param url: target url parsed by lxml
    :rtype: lxml.html.HtmlElement or NoneType
    :return: HtmlElement containing url's html info
    """
    try:
        f = urlopen(url).read()
        html = lxml.html.fromstring(f)
        time.sleep(2)
    except (UnicodeDecodeError, urllib.error.HTTPError):
        html = None
    return html


def split_html_tags_into_words(html, tag_name, words_lst):
    """based on tag name, extract text, split it into a word, and add them to words lst.
    
    :type html: lxml.html.HtmlElement
    :param html: containing its html dom info
    :type tag_name: str
    :param tag_name: tag name which user wanna know
    :type words_lst: list
    :param words_lst: container of words to create index dict
    """
    for tag_content in html.cssselect(tag_name):
        if not isinstance(None, type(tag_content.text)):
            words_lst += tag_content.text.split()


def add_page_to_index(index, url, html, target_html_tag, title):
    """get keywords' list and pass it to add_to_index function
    
    :type index: dict
    :param index: container which stores key word and corresponding url
    :type url: str
    :param url: crawling url
    :type html: lxml.html.HtmlElement
    :param html: containing its html dom info
    """
    words_lst = []
    for tag_name in target_html_tag:
        split_html_tags_into_words(html, tag_name, words_lst)
    for word in words_lst:
        word = re.sub(r'[\s\[\]\{\}\<\>\-\/\'\"*+=!#%:;.,。、]', '', word)
        pattern = re.compile(u'[一-龥ぁ-んァ-ン]')
        if len(word) == 0:
            continue
        if re.search(pattern, word):
            add_to_index(index, word, url, title)
            tagger = MeCab.Tagger()
            tagger.parse('')
            node = tagger.parseToNode(word)
            while node:
                word_ja = node.surface
                if len(word_ja) != 0:
                    add_to_index(index, word_ja, url, title)
                node = node.next
        else:
            add_to_index(index, word, url, title)


def add_to_index(index, keyword, url, title):
    """add keyword and corresponding url to index dict
    
    :type index: dict
    :param index: container which stores key word and corresponding url
    :type keyword: str
    :param keyword: index to help finding out url
    :type url: str
    :param url: crawling url
    """
    if keyword in index:
        # u => url, t => title
        # if url not in index[keyword][url]:
        if url != index[keyword].get(url):
            index[keyword][url] = title
    else:
        index[keyword] = {url: title}


def union_urls(base_url, urls, new_urls):
    """avoid making url duplicate before saving urls into db
    
    :type base_url: str
    :param base_url: hepling creating absolute url
    :type urls: list
    :param urls: containing target urls, not crawled yet
    :type new_urls: list
    :param new_urls: containing new target urls, some of which possibly have crawled url
    :rtype: None
    :return: None
    """
    for new_url in new_urls:
        new_url = urljoin(base_url, new_url.get('href'))
        if new_url not in urls:
            urls.append(new_url)


def scraping(seed_url, max_depth, max_capacity, target_html_tag):
    """parsing seed url, collecting urls related to seed url, and saving collected urls into DB
    
    :type seed_url: str
    :param seed_url: first url starting scraping
    :type max_depth: int
    :param max_depth: controlling the depth of crawls
    :type max_capacity: int
    :param max_capacity: controlling how many url collects per page
    :type target_html_tag: list
    :param target_html_tag: list containing target html tags 
    :rtype tuple(dict, dict)
    :return: tuple(dict, dict)
    
    """
    count = 0
    crawl_lst = [seed_url]    # list of targets scraping
    crawled_lst = []    # container for saving crawled urls
    next_depth = []    # temporary container containing list of next targets at each depth, and it will be initialized when scraping moves to next depth
    depth = 0    # showing the depth when scraping
    index = {}    # {keyword1, [url1, url2], keyword2, [url1, url2], ...}
    graph = {}    # {<url>, [list of url projected to another pages]}
    html = None    # html's dom info
    while crawl_lst and depth <= max_depth:
        base_url = crawl_lst.pop()
        count += 1
        print(count, ': ', base_url)
        # confirming target url is scrapable.
        if confirm_robots_txt(base_url, max_capacity):
            # parse target url as HTML object, but it sometimes can be None object
            html = parsing_url(base_url)
            if isinstance(None, type(html)):
                continue
            # firstly, confirm whether target url is already crawled
            if base_url not in crawled_lst:
                # select all a-tags projected to another html
                outlinks = html.cssselect('a')
                # the title of the base url
                title = html.cssselect('title')[0].text
                add_page_to_index(index, base_url, html, target_html_tag, title)
                graph[base_url] = [urljoin(base_url, outlink.get('href')) for outlink in outlinks]
                union_urls(base_url, next_depth, outlinks)
                crawled_lst.append(base_url)
            if not crawl_lst:
                crawl_lst, next_depth = next_depth, []
                depth = depth + 1
        else:
            continue
    return index, graph


def compute_ranks(graph):
    d = 0.8 # damping factor
    numloops = 10
    ranks = {}
    npages = len(graph)
    for page in graph:
        ranks[page] = 1.0 / npages
    for i in range(0, numloops):
        newranks = {}
        for page in graph:
            newrank = (1 - d) / npages
            for node in graph:
                if page in graph[node]:
                    newrank = newrank + d * (ranks[node] / len(graph[node]))
            newranks[page] = newrank
        ranks = newranks
    return ranks


def lookup(index, keyword):
    """search coressponding urls based on passed keyword
    
    :type index: dict
    :param index: container which stores key word and corresponding url
    :type keyword: str
    :param keyword: index to help finding out url
    :rtype: list or None
    :return: list of urls which corresponds to keyword or None
    """
    if keyword in index:
        return index[keyword]
    else:
        return None


def sort_ranks_by_descending(ranks, index, keyword):
    """return descending order of rank value and corresponding url
    
    :type ranks: dict
    :param ranks: dict containing url as a key and rank value
    :type index: dict
    :param index: container which stores key word and corresponding url
    :type keyword: str
    :param keyword: index to help finding out url
    :rtype: double list or None
    :return: double list of descending order of url and rank value or None
    """
    pages = lookup(index, keyword)    # [url1, url2, ...]
    sorted_ranks = []
    if pages:
        for page in pages:
            if page in ranks:
                sorted_ranks.append([page, ranks[page]])
        return sorted_ranks
    else:
        return None


'''
index, graph = scraping(input('enter seed url: '), int(input('enter depth: ')), int(input('decide capacity: ')))
ranks = compute_ranks(graph)
sorted_ranks = sort_ranks_by_descending(ranks, index, keyword = input('enter what you wanna search: '))
'''