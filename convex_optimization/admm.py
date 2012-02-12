"""
This module implements some of the ideas from the paper:

        Distributed Optimization and Statistical Learning via the Alternating Direction Method of Multipliers
        by Stephen Boyd, Neal Parikh, Eric Chu, Borja Peleato, Jonathan Eckstein

for the Disco framework.

Distributed Model Fitting
=========================

data is partitioned across the training examples
loss is additive: loss(A * x - b) = sum(loss(A[i] * x - b))
each task performs:

 minimize loss(A * x - b) + regularization(x)
 s.t.     x - z = 0

K is the number of input partitions
M is the number of examples
N is the number of features
A dimension is M * N
x dimension is N
b dimension is N

since M is very large, data is partitioned into K inputs, hence,
there are K instances of (x, y), hence,
there are 2 * K * N state variables (updated each iteration)
since the tasks share no state between jobs (iterations),
the state variables and possibly the problem data need to be reobtained each iteration

the state can be passed to the tasks as part of the job parameters, as long as K * N is small enough
if K * N becomes too large, then we need a way to either:

 a. distribute large params
 b. maintain state across iterations

(b) is more efficient, but messier

"""
from disco.core import Job, Params, RecordIter

class ADMM(Job):
    def map_reader(fd, url, size, params):
        i = Task.id
        z = params.z
        yi = params.y[i] + params.rho * (params.x[i] - z)
        for A, b in iter:
            xi = argmin(fi(x) + dot(yi, x - z) + (params.rho / 2.) * dot(x - z, x - z))
            yield str(i), (xi, yi)

    def reduce(iter, params):
        for n, (i, (xi, yi)) in enumerate(iter):
            zhat += xi + yi / float(params.rho)
        yield zhat / n

# first run a job to put records into A, b format
# and also calculate a first z

if __name__ == '__main__':
    params = Params(rho=1., z=0., objective=)

    while True:
        job = ADMM()
        results = job.wait()
        z = old_z
        params.z = list(RecordIter(job.results()))[0]
        if params.rho * sqrt(n) * pnorm(z - params.z, p=2) <= eta_conv:
            if sum(dot(xi - params.z, xi - params.z)
                   for xi, yi in RecordIter(results)) <= (eta_feas ** 2):
                break
