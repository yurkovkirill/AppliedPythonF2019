#!/usr/bin/env python
# coding: utf-8
from time import time


class LRUCacheDecorator:

    def __init__(self, maxsize, ttl):
        '''
        :param maxsize: максимальный размер кеша
        :param ttl: время в млсек, через которое кеш
                    должен исчезнуть
        '''
        # TODO инициализация декоратора
        #  https://www.geeksforgeeks.org/class-as-decorator-in-python/
        self.maxsize = maxsize
        self.ttl = ttl

        self.cached = {}
        self.results_times = {}

    def __call__(self, func):

        def wrapper(*args, **kwargs):
            cur_time = time()

            packet = tuple((args, str(kwargs)))

            if packet in self.cached:
                if self.ttl is not None:
                    if (cur_time - self.results_times[packet]) < self.ttl:  # если есть возвратим из кеша
                        self.results_times[packet] = cur_time

                        return self.cached[packet]
                    else:
                        result = func(*args, **kwargs)
                        self.cached[packet] = result
                        self.results_times[packet] = cur_time
                else:
                    self.results_times[packet] = cur_time

                    return self.cached[packet]
            else:
                while len(self.cached) >= self.maxsize:
                    del_key = min(self.results_times, key=lambda pdel_key: self.results_times[pdel_key])
                    # берем самым малым result_times
                    del self.results_times[del_key]
                    del self.cached[del_key]

                result = func(*args, **kwargs)
                self.cached[packet] = result
                self.results_times[packet] = cur_time

            return result

        return wrapper
