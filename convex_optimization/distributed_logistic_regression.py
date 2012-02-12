from disco.core import Job, Params, RecordIter

class LogisticRegress(Job):
    def map_reader(fd, url, size, params):
        i = Task.id
        z = params.z
        y = params.y[i] + params.rho * (params.x[i] - z)
        for A, b in iter:
            x = ...
            yield str(i), (x, y)

    def reduce(iter, params):
        for n, (i, (x, y)) in enumerate(iter):
            zhat += x + y / float(params.rho)
            yield i, (x, y)
        oob.put('z', zhat / n)

if __name__ == '__main__':
    params = Params(rho=1., z=0)

    while True:
        job = LogisticRegress(params=params)
        results = job.wait()
        for i, (x, y) in RecordIter(job.wait()):


