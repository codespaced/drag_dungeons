from collections import defaultdict
import random
from map_objects.point import Point
from pprint import pprint
from PIL import Image, ImageDraw, ImageFont
from kruskal import Graph


connector_regions = {
        Point(4, 1): {1, 14},
        Point(21, 1): {9, 15},
        Point(25, 1): {16, 9},
        Point(4, 2): {1, 14},
        Point(17, 2): {0, 15},
        Point(21, 2): {9, 15},
        Point(4, 3): {1, 14},
        Point(18, 3): {6, 15},
        Point(19, 3): {6, 15},
        Point(20, 3): {6, 15},
        Point(25, 3): {16, 9},
        Point(1, 4): {13, 14},
        Point(2, 4): {13, 14},
        Point(3, 4): {13, 14},
        Point(5, 4): {17, 1},
        Point(7, 4): {17, 1},
        Point(8, 4): {17, 1},
        Point(9, 4): {17, 1},
        Point(17, 4): {0, 6},
        Point(22, 4): {9, 18},
        Point(4, 5): {17, 13},
        Point(11, 5): {0, 17},
        Point(17, 5): {0, 6},
        Point(21, 5): {18, 6},
        Point(26, 5): {16, 11},
        Point(4, 6): {17, 13},
        Point(17, 6): {0, 6},
        Point(21, 6): {18, 6},
        Point(23, 6): {18, 11},
        Point(27, 6): {16, 11},
        Point(4, 7): {17, 13},
        Point(13, 7): {0, 7},
        Point(14, 7): {0, 7},
        Point(15, 7): {0, 7},
        Point(18, 7): {19, 6},
        Point(20, 7): {10, 6},
        Point(22, 7): {10, 18},
        Point(27, 7): {16, 11},
        Point(1, 8): {20, 13},
        Point(3, 8): {2, 13},
        Point(5, 8): {17, 2},
        Point(6, 8): {17, 2},
        Point(7, 8): {17, 2},
        Point(16, 8): {19, 7},
        Point(19, 8): {10, 19},
        Point(23, 8): {10, 11},
        Point(27, 8): {16, 11},
        Point(2, 9): {2, 20},
        Point(8, 9): {17, 2},
        Point(12, 9): {17, 7},
        Point(19, 9): {10, 19},
        Point(24, 9): {11, 3},
        Point(25, 9): {11, 3},
        Point(26, 9): {11, 3},
        Point(28, 9): {16, 3},
        Point(2, 10): {2, 20},
        Point(8, 10): {17, 2},
        Point(12, 10): {17, 7},
        Point(16, 10): {19, 7},
        Point(19, 10): {10, 19},
        Point(23, 10): {10, 3},
        Point(2, 11): {2, 20},
        Point(8, 11): {17, 2},
        Point(11, 11): {17, 5},
        Point(13, 11): {5, 7},
        Point(14, 11): {5, 7},
        Point(15, 11): {5, 7},
        Point(18, 11): {19, 4},
        Point(20, 11): {10, 4},
        Point(21, 11): {10, 4},
        Point(22, 11): {10, 4},
        Point(2, 12): {2, 20},
        Point(8, 12): {17, 2},
        Point(10, 12): {17, 5},
        Point(23, 12): {3, 4},
        Point(2, 13): {2, 20},
        Point(8, 13): {17, 2},
        Point(10, 13): {17, 5},
        Point(23, 13): {3, 4},
        Point(3, 14): {8, 2},
        Point(4, 14): {8, 2},
        Point(5, 14): {8, 2},
        Point(10, 14): {17, 5},
        Point(23, 14): {3, 4},
        Point(2, 15): {8, 20},
        Point(9, 15): {17, 12},
        Point(11, 15): {12, 5},
        Point(13, 15): {5, 21},
        Point(14, 15): {5, 21},
        Point(15, 15): {5, 21},
        Point(24, 15): {3, 21},
        Point(25, 15): {3, 21},
        Point(26, 15): {3, 21},
        Point(27, 15): {3, 21},
        Point(28, 15): {3, 21},
        Point(2, 16): {8, 20},
        Point(6, 16): {8, 12},
        Point(12, 16): {12, 21},
        Point(17, 16): {4, 21},
        Point(23, 16): {4, 21},
        Point(2, 17): {8, 20},
        Point(6, 17): {8, 12},
        Point(19, 17): {4, 21},
        Point(21, 17): {4, 21},
        Point(3, 18): {8, 20},
        Point(4, 18): {8, 20},
        Point(5, 18): {8, 20},
        Point(12, 18): {12, 21}
    }
# so we can draw our map at the end
original = connector_regions.copy()
joined_region_points = defaultdict(set)

# tracks our joined regions
joined_regions = set()

def place_junction(point, start_region=0, next_region=0):
    # if point in joined_regions:
    #     print(f'uh-oh {point} already in joined_regions {joined_regions[point]}')
    #     return
    joined_region_points[point] = (start_region, next_region)
    joined_regions.add(next_region)
    print(f'Junction placed at {point}, region {start_region} connected to {next_region}')

def get_unconnected_regions():
    ''' returns a set of unjoined regions '''
    regions = set()
    for r1, r2 in connector_regions.values():
        regions.add(r1)
        regions.add(r2)
    return [region for region in regions if region not in joined_regions]

def rebuild_adjacent_regions():
    ''' returns a dictionary of sets 
        {region0: {region1, region2, ...}}
        key is region
        value is set of integers representing adjacent_regions
    '''
    adjacent_regions = defaultdict(set)
    for r1, r2 in connector_regions.values():
        adjacent_regions[r1].add(r2)
        adjacent_regions[r2].add(r1)
    return adjacent_regions

def get_neighbor_connectors():
    # get list of all connectors for each region pair
    # {(r1, r2):[Point(x,y), Point(x,y), ...]}
    neighbor_connectors = defaultdict(list)
    for connector, regions in connector_regions.items():
        region_pair = (min(regions), max(regions))
        neighbor_connectors[region_pair].append(connector)
    return neighbor_connectors



def main():
    random.seed('TEST')
    start_region = 0
    next_region = 0

    # [region1, region2, ...]
    unconnected_regions = get_unconnected_regions()
    neighbor_connectors = get_neighbor_connectors()

    while unconnected_regions:
        adjacent_regions = rebuild_adjacent_regions()

        regions = adjacent_regions.get(start_region, None)

        i = 0
        # no unconnected regions from current start_region
        while not regions:
            print(f'no adjacent_regions to {start_region}')
            if i > 100:
                print('Failed to find a valid start_region')
                break
            # find a new start_region
            start_region = random.choice(list(joined_regions))
            print(f'Trying region {start_region}')
            regions = adjacent_regions.get(start_region, None)
            i += 1

        next_region = random.choice(list(regions))

        # if next_region is already connected, move on
        while next_region in joined_regions:
            # remove from regions so we don't try it more than once
            regions.remove(next_region)
            if not regions:
                print('regions is empty')
                break
            else:
                next_region = random.choice(list(regions))
                print(f'trying {next_region} for next')


        print(f'start_region: {start_region}, next: {next_region}')

        pair = min(start_region, next_region), max(start_region, next_region)
        open_connectors = neighbor_connectors[pair]
        if not open_connectors:
            print('something went wrong')
            continue
        junction = random.choice(open_connectors)
        place_junction(junction, start_region, next_region)
        
        if start_region in unconnected_regions:
            unconnected_regions.remove(start_region)
        else:
            print(f'start_region {start_region} not in unconnected_regions')                

        #prep for next round
        start_region = next_region

        # remove things
        for connector in open_connectors:
            del connector_regions[connector]
        
def min_spanning_tree(points):
    v = len(get_unconnected_regions())
    g = Graph(v)
    for point, (r1, r2) in points.items():
        g.addEdge(point, r1, r2, 1)
    g.KruskalMST()
    #g.print()
    return g.result

def draw(data, original, scale = 5):
    padding = scale * 2
    image = Image.new('RGB', (max_x() * scale + padding, max_y() * scale + padding), '#333')
    draw = ImageDraw.Draw(image)
    
    fnt = ImageFont.truetype('consola.ttf', 10)

    for p, (r1, r2) in original.items():
        if p in data:
            bgcolor = '#ccc'
            color = '#000'
        else:
            bgcolor = '#444'
            color = '#fff'
        x0, y0, x1, y1 = p.x * scale, p.y * scale, p.x * scale + scale, p.y * scale + scale
        draw.rectangle([x0, y0, x1, y1], bgcolor)
        # point
        draw.text((x0 + 1, y0 + 2), f'({p.x}, {p.y})', font=fnt, fill=color)
        # regions
        draw.text((x0 + 1, y0 + 12), f'{r1}, {r2}', font=fnt, fill=color)
    image.save('map.jpg')
    
def max_x():
    return max(p.x for p in connector_regions)

def max_y():
    return max(p.y for p in connector_regions)

if __name__ == '__main__':
    # main()
    # min_spanning_tree(joined_region_points)
    print(len(get_unconnected_regions()))
    result = min_spanning_tree(connector_regions)
    data = [point for point, _, _, _ in result]
    draw(data, original, 50)
