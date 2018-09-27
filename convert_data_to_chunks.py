
import os
import pickle
import numpy as np


possible_actions_map = {
            1: [[0, -1], [-1, -1], [-1, 0], [-1, 1], [0, 1]],
            2: [[-1, -1], [-1, 0], [-1, 1], [0, 1], [1, 1]],
            3: [[-1, 0], [-1, 1], [0, 1], [1, 1], [1, 0]],
            4: [[-1, 1], [0, 1], [1, 1], [1, 0], [1, -1]],
            5: [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1]],
            6: [[1, 1], [1, 0], [1, -1], [0, -1], [-1, -1]],
            7: [[1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0]],
            8: [[1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]
        }
action_map = {0:['left','down'],
                       1:['diagonal_left','down'],
                       2:['center','down'],
                       3:['diagonal_right','down'],
                       4:['right','down'],
                       5:['left','level'],
                       6:['diagonal_left','level'],
                       7:['center','level'],
                       8:['diagonal_right','level'],
                       9:['right','level'],
                       10:['left','up'],
                       11:['diagonal_left','up'],
                       12:['center','up'],
                       13:['diagonal_right','up'],
                       14:['right','up'],
                       15:['drop']}


def get_nextstep_altitudes(map_volume,drone_position,heading):
    canvas = np.zeros((5, 5, 3), dtype=np.uint8)
    slice = np.zeros((5, 5))
    drone_position_flat = [int(drone_position[1]), int(drone_position[2])]
    #get drone position - unknown altitude.




    # hiker_found = False
    # hiker_point = [0, 0]
    # hiker_background_color = None
    column_number = 0
    for xy in possible_actions_map[heading]:
        try:
            # no hiker if using original
            column = map_volume['vol'][:, drone_position_flat[0] + xy[0], drone_position_flat[1] + xy[1]]
            # for p in column:
            #     #print(p)
            #     #print(p == 50.0)
            #     if p == 50.0: # Hiker representation in the volume
            #         #print("setting hiker_found to True")
            #         hiker_found = True
            #
            # if hiker_found:
            #     val = self.original_map_volume['vol'][0][
            #         drone_position_flat[0] + xy[0], drone_position_flat[1] + xy[1]]
            #     hiker_background_color = self.original_map_volume['value_feature_map'][val]['color']
            #     # column = self.original_map_volume['vol'][:,drone_position_flat[0]+xy[0],drone_position_flat[1]+xy[1]]
        except IndexError:
            column = [1., 1., 1., 1., 1.]
        slice[:, column_number] = column
        column_number += 1
        # print("ok")
    # put the drone in
    # cheat
    corrected_slice = np.flip(slice,0)
    #one = np.count_nonzero(corrected_slice)
    two = np.count_nonzero(corrected_slice, axis=0)
    #three = np.count_nonzero(corrected_slice, axis=1)
    return two





def step_to_chunk(map_volume,drone_position,heading,action):
    #we have a volume.
    #we need the objects in drone's movemenet space
    altitudes = get_nextstep_altitudes(map_volume,drone_position,heading)
    #[left_altitude, diagonal_left, centre, diagonal_right, right]


    action_names = action_map[action]


    chunk = ['isa', 'decision','current_altitude',['current_altitude',int(drone_position[0])],
             'heading', ['heading',int(heading)],
             'view_left',['view_left',int(altitudes[0])],
             'view_diagonal_left',['view_diagonal_left',int(altitudes[1])],
             'view_center',['view_center',int(altitudes[2])],
             'view_diagonal_right',['view_diagonal_right',int(altitudes[3])],
             'view_right',['view_right',int(altitudes[4])],
             'action',['action',int(action)]]





    return chunk


    print("converting step")


# data_path = 'data'
#
# datafiles = os.listdir('data')
# all_chunks = []
# for file in [x for x in datafiles if '.tj' in x]:
#     path = os.path.join(data_path,file)
#     data = pickle.load(open(path,'rb'))
#     for episode in data:
#         for step in zip(data[episode]['vol'],data[episode]['drone_pos'],data[episode]['headings'],data[episode]['actions']):
#             all_chunks.append(step_to_chunk(step[0],step[1],step[2],step[3]))
#
#
# #we collect all the chunks, but don't need them all
# #we REALLY only need 1 of each possible combination (5^4?)
# #I assume we will not get every combination
# unique_chunks = []
# for x in all_chunks:
#     if not x in unique_chunks:
#         unique_chunks.append(x)
#
# #cull the chunks a bit more
# #altitude 4 seems useless information
# culled_chunks = []
# for chunk in unique_chunks:
#     if chunk[7][1] == 4 or \
#         chunk[9][1] == 4 or \
#         chunk[11][1] == 4 or \
#         chunk[13][1] == 4 or \
#         chunk[15][1] == 4:
#         continue
#     elif chunk[7][1] == 2 or \
#         chunk[9][1] == 2 or \
#         chunk[11][1] == 2 or \
#         chunk[13][1] == 2 or \
#         chunk[15][1] == 2:
#         continue
#     else:
#         culled_chunks.append(chunk)
#
# print(len(all_chunks))
# print(len(unique_chunks))
# print(len(culled_chunks))
#
# filename = 'chunks.pkl'
# file_path = os.path.join(data_path,filename)
# with open(file_path,'wb') as handle:
#     pickle.dump(culled_chunks,handle)


