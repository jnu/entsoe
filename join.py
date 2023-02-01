import json
import os

import click


out = 'final'


@click.command()
@click.argument('paths', nargs=-1)
def join(paths: list[str]):
    lines = {}
    points = {}

    for path in paths:
        with open(path) as fh:
            d = json.load(fh)

        if not lines:
            lines = d['lines']
            points = d['points']
            continue

        lines['features'] += d['lines']['features']
        points['features'] += d['points']['features']

    os.makedirs(out, exist_ok=True)

    with open(os.path.join(out, 'entsoe_lines.geojson'), 'w') as fh:
        json.dump(lines, fh)

    with open(os.path.join(out, 'entsoe_points.geojson'), 'w') as fh:
        json.dump(points, fh)


if __name__ == '__main__':
    join()
