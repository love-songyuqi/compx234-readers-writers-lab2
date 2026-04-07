"""
COMPX234 - Lab Assignment 2
Readers-Writers Problem using a Monitor in Python

Starter code
------------
Complete the TODO sections to implement a correct monitor solution.

Rules:
1. Multiple readers may read together if no writer is writing.
2. A writer must have exclusive access.
3. Use the monitor methods only to control access.

After you finish:
- test the program,
- rename this file to readers_writers.py if required by your instructor,
- commit your work to GitHub with meaningful commit messages.
"""

from __future__ import annotations

import random
import threading
import time


class ReadersWritersMonitor:
    """
    A monitor-style class that controls access to one shared resource.

    Suggested shared state:
    - active_readers: number of readers currently reading
    - active_writers: 0 or 1
    - waiting_writers: number of writers waiting (optional, but useful)
    """

    def __init__(self) -> None:
        self.lock = threading.Lock()
        self.condition = threading.Condition(self.lock)
        #共享状态计数器
        self.active_readers = 0 #当前正在读的读者数
        self.active_writers = 0 #当前正在写的写者数
        self.waiting_writers = 0 #等待的写者数

    def start_read(self, reader_id: int) -> None:
        """
        Called before a reader starts reading.
        Block the reader if a writer is writing.

        TODO:
        1. Acquire the condition using 'with self.condition:'.
        2. Wait while a writer is active.
        3. Increase active_readers.
        4. Print a useful log message.
        """
        with self.condition:
            # TODO: Replace 'pass' with your logic
            #1.用while循环等待：必须重新检查条件（作业要求禁止使用if）
            while self.active_writers>0;
                print(f"Reader{reader_id} is waiting to read(writer active)")
                self.condition.wait()#释放锁，等待唤醒
            #2.无写者，读者数+1
            self.active_readers+=1
            #3.打印符合要求的日志
            print（f"Reader{reader_id} starts reading.Active readers={self.active_readers}"）
            #4.唤醒其他等待的读者（支持多个读者同时读）
            self.condition.notify_all()

    def end_read(self, reader_id: int) -> None:
        """
        Called after a reader finishes reading.

        TODO:
        1. Decrease active_readers.
        2. Print a useful log message.
        3. If this was the last reader, wake waiting threads.
        """
        with self.condition:
            # TODO: Replace 'pass' with your logic
            #1.读者数-1
            self.active_readers-=1
            #2.打印日志
            print(f"Reader{reader_id} stops reading.Active reaers={self.active_readers}")
            #3.如果是最后一个读者，唤醒等待的写者
            if self.active_readers==0:
                self.condition.notify_all()

    def start_write(self, writer_id: int) -> None:
        """
        Called before a writer starts writing.
        Block the writer if any reader is reading or another writer is active.

        TODO:
        1. Increase waiting_writers before waiting (optional but recommended).
        2. Wait while active_readers > 0 or active_writers > 0.
        3. Update counters carefully when the writer can proceed.
        4. Print a useful log message.
        """
        with self.condition:
            # TODO: Replace 'pass' with your logic
            #1.可选：增加等待写者计数
            self.waiting_writer+=1
            #2.用while循环等待：有读者或有写者时，必须等待
            while self.active_readers>0 or self.active_writers>0:
                print(f"Writer{writer_id} is waiting to write(readers/writers active)")
                self.condition.wait()

    def end_write(self, writer_id: int) -> None:
        """
        Called after a writer finishes writing.

        TODO:
        1. Decrease active_writers.
        2. Print a useful log message.
        3. Wake waiting threads.
        """
        with self.condition:
            # TODO: Replace 'pass' with your logic
            #1.写者数-1（重置为0）
            self.active_writers=0
            #2.打印日志
            print(f"Writer{writer_id} stops writing")
            #3.唤醒所有等待线程：优先唤醒读者
            self.condition.notify_all()

# Donot Change this
class Reader(threading.Thread):
    def __init__(self, reader_id: int, monitor: ReadersWritersMonitor, rounds: int = 3) -> None:
        super().__init__()
        self.reader_id = reader_id
        self.monitor = monitor
        self.rounds = rounds

    def run(self) -> None:
        for _ in range(self.rounds):
            time.sleep(random.uniform(0.1, 0.7))  # stagger thread arrival

            print(f"Reader {self.reader_id} wants to read")
            self.monitor.start_read(self.reader_id)

            print(f"Reader {self.reader_id} is READING")
            time.sleep(random.uniform(0.3, 0.8))  # simulate reading

            self.monitor.end_read(self.reader_id)
            print(f"Reader {self.reader_id} finished reading")


# Donot Change this
class Writer(threading.Thread):
    def __init__(self, writer_id: int, monitor: ReadersWritersMonitor, rounds: int = 2) -> None:
        super().__init__()
        self.writer_id = writer_id
        self.monitor = monitor
        self.rounds = rounds

    def run(self) -> None:
        for _ in range(self.rounds):
            time.sleep(random.uniform(0.2, 0.9))  # stagger thread arrival

            print(f"Writer {self.writer_id} wants to write")
            self.monitor.start_write(self.writer_id)

            print(f"Writer {self.writer_id} is WRITING")
            time.sleep(random.uniform(0.4, 0.9))  # simulate writing

            self.monitor.end_write(self.writer_id)
            print(f"Writer {self.writer_id} finished writing")


def main() -> None:
    """
    Create the monitor and start the simulation.

    TODO ideas:
    - Create at least 3 readers and 2 writers.
    - Start all threads.
    - Join all threads.
    - Print a final message when the simulation is complete.
    """
    random.seed(42)#固定随机种子，方便复现结果

    monitor = ReadersWritersMonitor()

    # TODO: Create at least 3 Reader threads.
    readers = [
        Reader(reader_id=1, monitor=monitor),
        Reader(reader_id=2, monitor=monitor),
        Reader(reader_id=3, monitor=monitor)
    ]

    # TODO: Create at least 2 writer threads.
    writers = [
        Writer(writer_id=1, monitor=monitor),
        Writer(writer_id=2, monitor=monitor)
    ]

    all_threads = readers + writers

    # TODO: Start all threads
    for thread in all_threads:
        thread.start()

    # TODO: Wait for all threads to finish
    for thread in all_threads:
        thread.join()

    # TODO: Print final message that simulation completed
    print("\n All reader and writer threads have finished execution.Simulation complete!")


if __name__ == "__main__":
    main()
