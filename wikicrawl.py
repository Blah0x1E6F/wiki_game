import requests, re, pickle
from bs4 import BeautifulSoup
from collections import deque
from my_modules import misc_tools as misc # my misc tools

TRUNCATE_AFTER = 5 # Set to positive int to truncate, set to None to not truncate
MAX_PAGE_VISITS = 100 # Terminate main loop after this number of page visits.

def get_valid_links_from_page(cur_url):
    response = requests.get(misc.Page.base_url + cur_url)
    if response.status_code != 200:
        print(f'Error: {response.status_code}')
        print(f'Headers: {response.headers}')
        exit()

    soup = BeautifulSoup(response.content, 'html.parser')
    all_anchors = soup.find_all('a')
    title = soup.title.text
    if title.endswith(' - Wikipedia'):
        title = title[:-12]

    valid_links = []
    for anchor in all_anchors:
        link = anchor.get('href')
        if (link and link != cur_url and link != '/wiki/Main_Page'
            and link.startswith('/wiki/') and not re.search(r'\w:\w', link) and not re.search(r'File:', link) and not re.search(r'\w#\w', link)):
            if link not in valid_links:
                valid_links.append(link)

    if TRUNCATE_AFTER:
        truncation_msg = f'({len(valid_links)} valid links {misc.RED}before truncation{misc.RESET})'
    else:
        truncation_msg = ''
    valid_links = valid_links[:TRUNCATE_AFTER]

    print(f'{misc.BOLD}{misc.BLUE}{title}{misc.RESET} ({cur_url}): {misc.BOLD}{len(valid_links)}{misc.RESET}/{len(all_anchors)} links' +  truncation_msg)

    return valid_links, title

def process_next_page(queue, graph, counters):
    # Get next URL from queue
    cur_url = queue.popleft()
    # Get links from that page (remove dupes within the same page; remove non-article links)
    links, title = get_valid_links_from_page(cur_url)
    cur_page = graph[cur_url]
    cur_page.title = title

    # Add this page's deduped outbound links into the graph for this page; we're done with this page.
    cur_page.links = links
    counters.graphVisited += 1
    counters.graphEdges += len(links)

    # For each link, add it to queue if not yet in graph 
    # Also important to add it to the graph (but with an empty list, since we haven't visited the page yet)
    # -- this is to avoid adding duplicate entries to the queue.
    localDupes = 0
    for link in links:
        if link not in graph:
            queue.append(link)
            graph[link] = misc.Page(link, parent=cur_page)
        else:
            localDupes += 1
            counters.dupeCount += 1
    
    print(f'DEPTH: {cur_page.get_depth()}')
    print(f'PATH: {misc.ITALICS}{cur_page.get_path()}{misc.UNITALICS}')
    print(f'Graph: {counters.graphVisited} visited pages, {counters.graphEdges} outgoing links, {localDupes}/{counters.dupeCount} dupes (local/total), {len(graph)-counters.graphVisited} pages in queue')
    print() # Blank line

def main():
    start_url, output_file_name = misc.get_command_line_params()
    counters = misc.Counters()
    
    #initialize queue and graph with the initial URL and page
    queue = deque([start_url])
    graph = {start_url: misc.Page(start_url)}
    
    with misc.DelayedKeyboardInterrupt() as blah:
        # Our main loop
        while len(queue) > 0 and counters.graphVisited < MAX_PAGE_VISITS and not blah.get_outta_here:
            process_next_page(queue, graph, counters)
        
        # misc.test_pickling_and_unpickling(queue, graph, counters, output_file_name)
        
        tuple = (start_url, TRUNCATE_AFTER, MAX_PAGE_VISITS, queue, graph, counters)
        print(f'Pickling our data to {output_file_name}...')
        with open(output_file_name, 'wb') as file:
            pickle.dump(tuple, file)
        print('Done.')
        
if __name__ == '__main__':
    main()
