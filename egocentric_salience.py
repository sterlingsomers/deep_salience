import actr
import os
import pickle
import json
import time

min_max = {'view_left':[],
           'view_diagonal_left':[],
           'view_diagonal_right':[],
           'view_center':[],
           'view_right':[],
           'heading':[],
           'current_altitude':[]}




def access_by_key(key, list):
    '''Assumes key,vallue pairs and returns the value'''
    if not key in list:
        raise KeyError("Key not in list")

    return list[list.index(key)+1]


def similarity(val1, val2):
    '''Linear tranformation, abslute difference'''
    max_val = max(min_max[val1[0].lower()])
    min_val = min(min_max[val1[0].lower()])
    if val1 == None:
        return None
    val1 = val1[1]
    val2 = val2[1]
    #max_val = 4#max(map(max, zip(*feature_sets)))
    #min_val = 1#min(map(min, zip(*feature_sets)))
    print("max,min,val1,val2",max_val,min_val,val1,val2)
    val1_t = (((val1 - min_val) * (0 + 1)) / (max_val - min_val)) + 0
    val2_t = (((val2 - min_val) * (0 + 1)) / (max_val - min_val)) + 0
    #print("val1_t,val2_t", val1_t, val2_t)
    #print("sim returning", abs(val1_t - val2_t) * -1)
    #print("sim returning", ((val1_t - val2_t)**2) * - 1)
    #return float(((val1_t - val2_t)**2) * - 1)
    #return abs(val1_t - val2_t) * - 1
    #return 0
    #print("sim returning", abs(val1_t - val2_t) * - 1)
    #return abs(val1_t - val2_t) * -1
    print("sim returning", (abs(val1 - val2) * - 1)/max_val)
    return (abs(val1 - val2) * - 1)/max_val

    print("sim returning", abs(val1 - val2) / (max_val - min_val) * - 1)
    return abs(val1 - val2) / (max_val - min_val) * - 1


def compute_S(blend_trace, keys_list):
    '''For blend_trace @ time'''
    #probablities
    probs = [x[3] for x in access_by_key('MAGNITUDES',access_by_key('SLOT-DETAILS',blend_trace[0][1])[0][1])]
    #feature values in probe
    FKs = [access_by_key(key.upper(),access_by_key('RESULT-CHUNK',blend_trace[0][1])) for key in keys_list]
    chunk_names = [x[0] for x in access_by_key('CHUNKS', blend_trace[0][1])]

    #Fs is all the F values (may or may not be needed for tss)
    #They are organized by chunk, same order as probs
    vjks = []
    for name in chunk_names:
        chunk_fs = []
        for key in keys_list:
            chunk_fs.append(actr.chunk_slot_value(name,key))
        vjks.append(chunk_fs)

    #tss is a list of all the to_sum
    #each to_sum is Pj x dSim(Fs,vjk)/dFk
    #therefore, will depend on your similarity equation
    #in this case, we need max/min of the features because we use them to normalize
    max_val = 4#max(map(max, zip(*feature_sets)))
    min_val = 1#min(map(min, zip(*feature_sets)))
    n = max_val - min_val
    n = max_val
    #n = 1
    #this case the derivative is:
    #           Fk > vjk -> -1/n
    #           Fk = vjk -> 0
    #           Fk < vjk -> 1/n
    #compute Tss
    #there should be one for each feature
    #you subtract the sum of each according to (7)
    tss = {}
    ts2 = []
    for i in range(len(FKs)):
        if not i in tss:
            tss[i] = []
        for j in range(len(probs)):
            if FKs[i][1] > vjks[j][i][1]:
                dSim = -1/max(min_max[vjks[j][i][0].lower()])
            elif FKs[i][1] == vjks[j][i][1]:
                dSim = 0
            else:
                dSim = 1/max(min_max[vjks[j][i][0].lower()])
            tss[i].append(probs[j] * dSim)
        ts2.append(sum(tss[i]))

    #vios
    viosList = []
    viosList.append([actr.chunk_slot_value(x,'action') for x in chunk_names])
    #viosList.append([actr.chunk_slot_value(x,'altitude_change') for x in chunk_names])
    #viosList.append([actr.chunk_slot_value(x, 'diagonal_right_turn') for x in chunk_names])
    #viosList.append([actr.chunk_slot_value(x, 'right_turn') for x in chunk_names])
    #viosList.append([actr.chunk_slot_value(x, 'ascending') for x in chunk_names])
    #viosList.append([actr.chunk_slot_value(x, 'drop_action') for x in chunk_names])
    #compute (7)
    rturn = []
    for vios in viosList:
        results = []
        for i in range(len(FKs)):
            tmp = 0
            sub = []
            for j in range(len(probs)):
                if FKs[i][1] > vjks[j][i][1]:
                    dSim = -1/max(min_max[vjks[j][i][0].lower()])
                elif FKs[i] == vjks[j][i]:
                    dSim = 0
                else:
                    dSim = 1/max(min_max[vjks[j][i][0].lower()])
                tmp = probs[j] * (dSim - ts2[i]) * vios[j][1]#sum(tss[i])) * vios[j]
                sub.append(tmp)
            results.append(sub)

        print("compute S complete")
        rturn.append(results)
    return rturn

def reset_actr():

    model_name = 'egocentric-salience.lisp'
    model_path = '/Users/paulsomers/COGLE/deep_salience/'

    chunk_file_name = 'chunks.pkl'
    chunk_path = os.path.join(model_path,'data')

    actr.add_command('similarity_function',similarity)
    actr.load_act_r_model(os.path.join(model_path,model_name))
    actr.record_history("blending-trace")


    #load all the chunks
    allchunks = pickle.load(open(os.path.join(chunk_path,chunk_file_name),'rb'))
    for chunk in allchunks:
        actr.add_dm(chunk)

    for chunk in allchunks:
        for x, y in zip(*[iter(chunk)] * 2):
            #x, y[1]
            if not x == 'action' and not x == 'isa':
                if y[1] not in min_max[x]:
                    min_max[x].append(y[1])
    #print('asf')


def handle_observation(observation):
    '''observation should have chunk format'''

    chunk = actr.define_chunks(observation)
    actr.schedule_simple_event_now("set-buffer-chunk",
                                   ['imaginal', chunk[0]])
    actr.run(10)

    d = actr.get_history_data("blending-trace")
    d = json.loads(d)

    t = actr.get_history_data("blending-times")

    MP = actr.get_parameter_value(':mp')
    # #get t
    t = access_by_key('TEMPERATURE', d[0][1])
    # #the values
    # vs = [actr.chunk_slot_value(x,'value') for x in chunk_names]
    #
    factors = ['current_altitude', 'heading', 'view_left', 'view_diagonal_left', 'view_center', 'view_diagonal_right', 'view_right']
    # factors = ['needsFood', 'needsWater']
    result_factors = ['action']
    # result_factors = ['food','water']
    results = compute_S(d, factors)  # ,'f3'])
    for sums, result_factor in zip(results, result_factors):
        print("For", result_factor)
        for s, factor in zip(sums, factors):
            print(factor, MP / t * sum(s))

    print("actual value is", actr.chunk_slot_value('OBSERVATION0', 'ACTUAL'))

    print("done")


reset_actr()
start = time.time()
handle_observation(['isa','observation',
                    'current_altitude',['current_altitude',3],
                    'heading',['heading',5],
                    'view_left',['view_left',4],
                    'view_diagonal_left',['view_diagonal_left',4],
                    'view_center',['view_center',1],
                    'view_diagonal_right',['view_diagonal_right',2],
                    'view_right',['view_right',2]])
end = time.time()
print("time", end - start)