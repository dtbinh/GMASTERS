#!/usr/bin/env python
from py4j.java_gateway import JavaGateway


def get_masters():
    gateway = JavaGateway()
    masters = gateway.entry_point.getMasters()
    return masters


def main():
    masters = get_masters()
    masters.loadParameters('samples/simulation.properties')

    print 'Starting simulation'
    step = 0

    while masters.is_running():
        print 'Step', step
        masters.step()
        step += 1


if __name__ == '__main__':
    main()
