from requests import Session
from game_sol import Map

MAP = 'http://94.237.63.93:35775/map'
UPDATE = 'http://94.237.63.93:35775/update'

s = Session()

while True:
    map_data = s.post(MAP).json()
    m = Map(width=map_data['width'], height=map_data['height'], tiles=map_data['tiles'], player=map_data['player'])

    seq = m.path_seq
    print(seq)

    for i, c in enumerate(seq):
        r = s.post(UPDATE, json={'direction': c})
        data = r.json()
        
        if i == len(seq) - 1:
            assert 'solved' in data
            assert data['solved']

            if 'flag' in data:
                print(data['flag'])
                exit(0)
