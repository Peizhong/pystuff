import collections
import queue

Event = collections.namedtuple('Event', 'time proc action')

v = 1

while v < 5:
    v += 1
else:
    print('while else')


def taxi_process(ident, trips, start_time=0):
    #协程暂停, 等待调用方安排下一个事件
    time = yield Event(start_time, ident, 'leave garage')
    for t in range(trips):
        time = yield Event(time, ident, 'pick up passenger')
        time = yield Event(time, ident, 'drop off passenger')
    v = yield Event(time, ident, 'going home')
    print(v)
    # 最后抛出StopIteration异常


def run_taxi():
    taxi0 = taxi_process(0, 2, 0)
    # 出发
    r = next(taxi0)
    print(r)
    print('send next 1')
    r = taxi0.send(r.time+7)
    print(r)
    print('send next 2')
    r = taxi0.send(r.time + 10)
    print(r)
    print('send next 3')
    r = taxi0.send(r.time+7)
    print(r)
    print('send next 4')
    r = taxi0.send(r.time + 10)
    print(r)
    print('send next 5')
    r = taxi0.send(r.time+7)
    print(r)
    print('send next 6')
    r = taxi0.send(r.time + 10)
    print(r)
    print('send next 7')
    r = taxi0.send(r.time + 10)
    print(r)


def compute_duration(previous_action):
    if 'pick up' in previous_action:
        return 10
    elif 'drop off' in previous_action:
        return 2
    return 1


class Simulator:
    def __init__(self, procs_map):
        self.events = queue.PriorityQueue()
        self.procs = dict(procs_map)

    def run(self, end_time):
        for _, proc in sorted(self.procs.items()):
            first_event = next(proc)
            self.events.put(first_event)
        sim_time = 0
        while sim_time < end_time:
            if self.events.empty():
                print('**end of events')
                break
            current_event = self.events.get()
            sim_time, proc_id, previous_action = current_event
            print('get: ', proc_id, sim_time, previous_action)
            active_proc = self.procs[proc_id]
            next_time = sim_time + compute_duration(previous_action)
            try:
                next_event = active_proc.send(next_time)
            except StopIteration:
                del self.procs[proc_id]
            else:
                self.events.put(next_event)
        else:
            # while条件正常结束
            msg = 'end of simulation {} events pending'.format(
                self.events.qsize())


taxis = {
    0: taxi_process(0, 3, 0),
    1: taxi_process(1, 2, 4),
    2: taxi_process(2, 3, 5)
}

if __name__ == '__main__':
    sim = Simulator(taxis)
