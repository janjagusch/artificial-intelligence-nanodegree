from pickle import load
from pandas import DataFrame

def main():

    with(open('benchmark.pkl', 'rb')) as f:
        benchmark = load(f)

    for a in benchmark.values():
        for b in a.values():
            b['solution'] = len(b['solution']) if b['solution'] is not None else None

    benchmark_by_problem = [DataFrame.from_dict(d).T for d in benchmark.values()]

    for b, name in zip(benchmark_by_problem, [k.replace(" ", "_").lower()+".csv" for k in benchmark.keys()]):
        b.to_csv(name)


if __name__ == '__main__':
    main()