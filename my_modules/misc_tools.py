import signal, pickle, sys

BOLD, RED, GREEN, BLUE, RESET = '\033[31m', '\033[1m', '\033[32m', '\033[34m', '\033[0m'
ITALICS, UNITALICS = '\x1B[3m', '\x1B[0m'

# This is a context manager. It lets us use the 'with...' statement. 
# It delays kbrd interrupt until the end of the with scope.
class DelayedKeyboardInterrupt:
    def __enter__(self):
        print('In __enter__')
        self.get_outta_here = False
        signal.signal(signal.SIGINT, self.handler)
        return self

    def handler(self, sig, frame):
        print('In handler')
        self.get_outta_here = True

    def __exit__(self, exc_type, exc_value, exc_traceback):
        print('In __exit__')

class Page:
    base_url = 'https://en.wikipedia.org'

    def __init__(self, url, title=None, parent=None, links=None):
        self.url = url
        self.title = title
        self.parent = parent
        self.links = links

    def __str__(self):
        return self.title if self.title else self.url

    # __hash__ and __eq__ will no longer be neccessary once
    # we move away from using Pages as dictionary keys
    def __hash__(self):
        return hash(self.url)
    def __eq__(self, other):
        if isinstance(other, Page):
            return self.url == other.url
        return False
    
    def get_path(self):
        resolved_title = self.title if self.title else self.url
        if not self.parent:
            return resolved_title
        else:
            return f'{self.parent.get_path()} → {resolved_title}'

    def get_depth(self):
        if not self.parent: 
            return 0
        else:
            return self.parent.get_depth() + 1

class Counters:
    def __init__(self):
        self.graphVisited, self.graphEdges, self.dupeCount = 0, 0, 0

    def __str__(self):
        return f'{self.graphVisited} visited, {self.graphEdges} edges, {self.dupeCount} dupes'

def get_command_line_params():
    if len(sys.argv) != 3:
        print(f'Usage: python3 {sys.argv[0]} <start_wiki_page_URL> <output_pickle_file>')
        print('Wiki URL format: /wiki/Python')
        print('File name format: python.pickle')
        exit(0)
    return sys.argv[1], sys.argv[2]

def get_input_file_name():
    if len(sys.argv) != 2:
        print(f'Usage: python3 {sys.argv[0]} <input_pickle_file>')
        exit(0)
    return sys.argv[1]

def save_objects_to_temp_file(queue, graph, counters, output_file):
    with open(output_file, "w") as f:
        f.write(f'QUEUE ({len(queue)}):\n')
        for item in queue:
            f.write(item.url + '\n')
        
        f.write(f'\nGRAPH ({len(graph)}):\n')
        # Sorting ensures predictable order of items when printing
        sorted_items = sorted(graph.items(), key=lambda item: item[0].url) 
        for item in sorted_items:
            f.write(f'{item[0].url}: {item[1]}\n')

        f.write('\nCOUNTERS:\n')
        f.write(str(counters)+ '\n')

def test_pickling_and_unpickling(queue, graph, counters, output_file_name):
        save_objects_to_temp_file(queue, graph, counters, 'temp_state_before_pickling.txt')
        tuple = (queue, graph, counters)
        with open(output_file_name, 'wb') as file:
            pickle.dump(tuple, file)
        print('Pickling done. Unpickling now... ')
        with open(output_file_name, 'rb') as file:
            loaded_data = pickle.load(file)
            save_objects_to_temp_file(loaded_data[0], loaded_data[1], loaded_data[2], 'temp_state_after_pickling.txt')
