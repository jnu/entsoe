import json
import os
import gzip

import click
import mapbox_vector_tile as mvt
import tile_tools as tt
import mercantile


def fixcoord(tile: mercantile.Tile, coord: list[int]):
    return tuple(tt.tilecoords2lnglat(tile, *coord))


def gettile(tilepath: str) -> mercantile.Tile:
    name, _ = os.path.splitext(os.path.basename(tilepath))
    z, x, y = name.lstrip('entsoe')
    return mercantile.Tile(int(x), int(y), int(z))


@click.command()
@click.argument('tilepath', type=str)
def parse(tilepath: str):
    # Decode the protobuf
    with gzip.open(tilepath, 'rb') as fh:
        pbf = fh.read()

    data = mvt.decode(pbf)

    # Parse tile coords from path
    tile = gettile(tilepath)

    # Fix coordinates for lines and points
    for f in data['lines']['features']:
        geo = f['geometry']
        if geo['type'] == 'LineString':
            geo['coordinates'] = [
                    fixcoord(tile, ll) for ll in geo['coordinates']]
        elif geo['type'] == 'MultiLineString':
            geo['coordinates'] = [
                    [fixcoord(tile, ll) for ll in line]
                    for line in geo['coordinates']]
        else:
            raise TypeError(f"don't know how to parse {geo['type']}")

    for f in data['points']['features']:
        geo = f['geometry']
        geo['coordinates'] = fixcoord(tile, geo['coordinates'])

    print(json.dumps(data))


if __name__ == '__main__':
    parse()
