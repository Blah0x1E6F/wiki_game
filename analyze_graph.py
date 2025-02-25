from my_modules import misc_tools as misc # my misc tools
import pickle, time

def get_test_graph():
    # **********************************NOTE******************************
    # I've refactored wikicrawl to not use Page as key
    # So this wouldn't work anymore.
    start_url = 'a'
    graph = {}
    graph[misc.Page('a', None, 'a')] = ['b', 'c', 'd']
    graph[misc.Page('b', None, 'b')] = ['e', 'f', 'c']
    graph[misc.Page('c', None, 'c')] = ['g', 'h', 'a'] # Note loop: if we blindly follow, causes infinite recursion!
    graph[misc.Page('d', None, 'd')] = ['f', 'g', 'h']
    graph[misc.Page('e', None, 'e')] = None
    graph[misc.Page('f', None, 'f')] = ['b'] # Note loop. To avoid infinite recursion, need to keep track of visited nodes.
    graph[misc.Page('g', None, 'g')] = ['a'] # Note loop. To avoid infinite recursion, need to keep track of visited nodes.
    graph[misc.Page('h', None, 'h')] = None
    print('DICTIONARY VIEW:')
    for pair in graph.items():
        print(f'{pair[0]} -> {pair[1]}')
    return graph, start_url

def get_real_graph(input_file_name):
    with open(input_file_name, 'rb') as file:
        tuple = pickle.load(file)
    start_url, truncate_after, max_page_visits, queue, graph, counters = tuple
    print(f'Start URL: {start_url}, truncate after: {truncate_after}, max page visits: {max_page_visits}, queue size: {len(queue)}, graph size: {len(graph)}, counters: {counters}')
    return graph, start_url

def depth_first_print(graph, url, depth, seen):
    page = graph[url]
    indent = '| ' * depth
    print(f'{depth:0{2}d}{indent}{page} DEPTH {page.get_depth()}: {misc.BLUE}{page.get_path()}{misc.RESET}')
    seen.add(url)
    links = page.links # nodes is list of urls
    if links is not None: # leafe node
        for link in links:
            if link not in seen:
                depth_first_print(graph, link, depth + 1, seen)
    # xx
    # page = misc.Page(url, None)
    # indent = '| ' * depth
    # print(f'{indent}{page}')
    # seen.add(url)
    # links = graph[page] # nodes is list of urls
    # if links is not None: # leafe node
    #     for link in links:
    #         if link not in seen:
    #             depth_first_print(graph, link, depth + 1, seen)


def main():
    # graph, start_url = get_test_graph()
    graph, start_url = get_real_graph(misc.get_input_file_name())
    
    # print('DICTIONARY VIEW:')
    # for pair in graph.items():
    #     print(f'{pair[0]} -> {pair[1]}')

    print('\nINDENTED VIEW:')
    depth_first_print(graph, start_url, 0, set())

if __name__ == '__main__':
    main()
