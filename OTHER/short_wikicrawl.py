import requests, re, collections, bs4
base_url, start_url = 'https://en.wikipedia.org', '/wiki/Moon'
queue, graph = collections.deque([start_url]), {start_url: None}
while len(queue) > 0:
    url, valid_links = queue.popleft(), []
    all_anchors = bs4.BeautifulSoup(requests.get(base_url + url).content, 'html.parser').find_all('a')
    for anchor in all_anchors:
        link = anchor.get('href')
        if (link and link != url and link != '/wiki/Main_Page' and link.startswith('/wiki/') and not re.search(r'\w:\w', link) and not re.search(r'\w#\w', link) and link not in valid_links):
            valid_links.append(link)
    print(f'{url}: {len(valid_links)}/{len(all_anchors)} links')
    graph[url] = valid_links
    for link in valid_links:
        if link not in graph:
            queue.append(link)
            graph[link] = None