import logging
import time
from os import environ
from multiprocessing import Queue, Process


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MyProcess(Process):
    count = 0

    def __init__(self, collection):
        logger.info('Process: collection length:%d' % len(collection))
        self.queue = Queue()
        self.collection = collection
        super().__init__(target=self.__execute, args=(collection,))

    def execute(self, collection):
        return []

    def __execute(self, collection):
        result = self.execute(collection)
        MyProcess.count = MyProcess.count + 1
        for r in result:
            self.queue.put(r)
        return result

    def get_result(self):
        result = []
        # self.join()
        # while not self.queue.empty():
        for i in range(0, len(self.collection)):
            result.append(self.queue.get())
        return result


def split_collection(num_of_collections, collection):
    collections = []
    collection_size = len(collection)
    batch_size = int(collection_size / num_of_collections)
    if collection_size % num_of_collections != 0:
        batch_size += 1
    for i in range(0, num_of_collections):
        st = batch_size * i
        end = min(batch_size * (i + 1), collection_size)
        collections.append(collection[st: end])
    return collections


# Use to execute methods with multiple processes
class Parallel:
    def __init__(self):
        self.num_of_processes = 1
        if 'NUM_OF_PROCESSORS' in environ:
            self.num_of_processes = int(environ['NUM_OF_PROCESSORS'])

    def parallelize(self, method):
        def decorated(collection):
            result = []
            collections = split_collection(self.num_of_processes, collection)
            processes = []
            for collection in collections:
                process = method(collection)
                process.start()
                processes.append(process)
            for process in processes:
                result.extend(process.get_result())
            return result

        return decorated

    # Use this method if the method which is being decorated has the following constraints:
    # 1. The method has just one argument named collection and returns another collection with the same length
    # 2. Use self just for reading not writing
    # 3. Each element of the collection can be processed independent from other elements in the collection

    def parallelize_method(self, method):
        def decorated(r, collection):
            class DecoratedProcess(MyProcess):
                def execute(self, process_collection):
                    super().execute(process_collection)
                    return method(r, process_collection)

            result = []
            collections = split_collection(self.num_of_processes, collection)
            processes = []
            for collection in collections:
                process = DecoratedProcess(collection)
                process.start()
                processes.append(process)
            for process in processes:
                result.extend(process.get_result())
            return result

        return decorated


parallel = Parallel()


class Test:
    def __init__(self, c):
        self.c = c
        pass

    @parallel.parallelize_method
    def some_function(self, collection):
        result = []
        for c in collection:
            # time.sleep(1)
            result.append(self.c[c])
        return result


# @execution_time_keeper
# def tes():
#     t = Test(['a', 'b', 'c', 'd', 'e', 'r'])
#     print(t.some_function([1] * 10000))

# tes()