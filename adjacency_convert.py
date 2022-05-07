import numpy as np

data = np.load('my_data.npz')
adj = data['adj']
attr = data['attr']

for i in range(100):
    with open('nodes', 'a') as fnodes:
        fnodes.write(str(i)+'\n')

for timestep in range(len(attr)):
    with open('stream_attributes/'+str(timestep), 'a') as fattr:
        for line in attr[timestep]:
            written_line = ""

            for value in line:
                written_line += str(value)+" "
            fattr.write(written_line+'\n')

for timestep in range(len(adj)):
    for i in range(1, len(adj[timestep])):
        for j in range(i):
            if adj[timestep][i][j] == 1:
                with open('stream_edges/'+str(timestep), 'a') as fp:
                    fp.write(str(i)+' '+str(j)+'\n')
                with open('stream_labels_positive_u/'+str(timestep), 'a') as fu:
                    fu.write(str(i)+'\n')
                with open('stream_labels_positive_v/'+str(timestep), 'a') as fv:
                    fv.write(str(j)+'\n')
            else:
                with open('stream_labels_negative_u/'+str(timestep), 'a') as fnegu:
                    fnegu.write(str(i)+'\n')
                with open('stream_labels_negative_v/'+str(timestep), 'a') as fnegv:
                    fnegv.write(str(j)+'\n')

