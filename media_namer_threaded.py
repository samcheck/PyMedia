import logging
import os
import sys
from time import time
from queue import Queue
from threading import Thread

import videoLister
import media_rename
import scrapeTVDB

class RenameWorker(Thread):
    def __init__(self, queue):
        super(RenameWorker, self).__init__()
        self.queue = queue

    def run(self):
        while True:
            # Get the work from the queue and expand the tuple
            item, JWT = self.queue.get()
            media_rename.rename(item, JWT)
            self.queue.task_done()

def main():
    logging.basicConfig(filename='m_n_t.log',level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)

    in_path = ' '.join(sys.argv[1:]) # take args in from commandline
    num_workers = 16 # number of worker threads
    ts = time() # start time stamp
    JWT = scrapeTVDB.auth() # get auth token for the TVDB

    # Create a Queue to communicate with the worker threads
    queue = Queue()

    # Create worker threads
    for x in range(num_workers):
        worker = RenameWorker(queue)
        # Setting daemon to True will let the main thread exit even though the workers are blocking
        worker.daemon = True
        worker.start()

    # Put tasks into the queue as tuples
    for item in videoLister.videoDir(in_path):
        logger.info('Queueing {}'.format(os.path.abspath(item)))
        queue.put((item, JWT))

    # Causes the main thread to wait for the queue to finish processing all the tasks
    queue.join()
    logger.info('Took {}s'.format(time() - ts))

if __name__ == '__main__':
    main()
