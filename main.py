import os
import math
import numpy as np
import pandas as pd
import matplotlib.image as mpimg
from mpl_toolkits.mplot3d import Axes3D


from event_process import *
from Contrast_Maximization import contra_max


if __name__ == '__main__':
    '''
    event_path = './data/shapes_6dof.npy'
    row_event = np.load(event_path)
    event =row_event
    '''
    file_path = './data/bike.csv'
    data_frame = pd.read_csv(file_path)
    row_event = data_frame.to_numpy()
    #event = row_event[:, [1, 2, 0, 3]]
    event = row_event
    event[:,3]= (event[:, 3] - event[0, 3])


    #print(row_event.shape)
    rangeX, rangeY = 346, 260
    limit_up_rate = 4

    X = event[:, 0]
    Y = event[:, 1]
    P = event[:, 2]
    T = (event[:, 3] )

    # save path of results
    save_path = 'results/'
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    gen_events = []
    image = img1 = mpimg.imread('./data/2.60.png')
    event_num = 10000
    num = math.ceil(event.shape[0] / event_num)
    for k in range(int(num)):
        x = X[k * event_num:(k + 1) * event_num]
        y = Y[k * event_num:(k + 1) * event_num]
        p = P[k * event_num:(k + 1) * event_num]
        t = T[k * event_num:(k + 1) * event_num]

        t_min = np.min(t)
        t_ref = np.max(t)
        t_max = np.max(t)
        flow = contra_max(x, y, p, t, t_ref, rangeX, rangeY)
        flow = np.array([0, 0])


        initial_events = np.column_stack((x, y, p, t))

        def show_some_events(events,image,label):
            show_lines_on_image(events, image, label=label)
            show_events(events, color='y', label=label)

        def old_algorithm(flow, x, y, p, t, t_ref, rangeX, rangeY):
            ref, noise_events, nx, ny, main_events, mx, my = dist_main_noise(flow, x, y, p, t, t_ref, rangeX, rangeY)
            #show_ref(flow,x,y,p,t,t_ref,rangeX,rangeY)




            #plot_ref_image(ref)
            print(k + 1, '/', num, '. Noise events: ', nx.size, ', Main events: ',np.sum(np.abs(ref)) - nx.size)




            main_second_events,secondary_events, remaining_noise=separate_secondary_events(noise_events,main_events)




            result = count_events_within_distance(main_events,secondary_events,remaining_noise,3,0.001)
            print(result)

            main_secondary_third_events,third_events,remaining_noise3=separate_third_events(result,main_second_events,remaining_noise,m=4,n=3,l=2)

            #save_event(remaining_noise,save_path='results/',filename="remaining_noise.csv")
            # Show initial all events
            initial_events = np.column_stack((x, y, p, t))
            show_lines_on_image(initial_events, image, label='Raw')
            #show_lines(initial_events,t_ref,' All Events')
            #show_events(initial_events, color='r', label='Initial All Events')
            #show_lines(main_events,label=' Main Events')
            #show_lines(noise_events,label=' remaining_noise1')
            #show_events_with_image(initial_events,'./data/Ferriswheel_00_1.6.png')
            #show_two_kinds_of_events_with_image(main_events, noise_events, './data/2.60.png')

            #show_four_kinds_of_lines(main_events,secondary_events,third_events,remaining_noise3)
            #show_three_kinds_of_lines(main_events,secondary_events,remaining_noise,)
            x_center=100
            y_center=34
            size=10
            roi = (x_center - size / 2, x_center + size / 2, y_center - size / 2, y_center + size / 2)

            #show_lines_on_image(initial_events, image, label='main_secondary_third_events')
            show_lines(main_events, t_ref, label="main_secondary_third_events")
            #show_lines(main_second_events,t_ref, label="main_secondary_third_events")
            #show_lines(main_secondary_third_events,t_ref,label="main_secondary_third_events")

            #show_two_kinds_of_lines_with_local_part(main_events, noise_events, roi_bounds=roi)
            #show_three_kinds_of_lines_with_local_part(main_events, secondary_events, remaining_noise, roi_bounds=roi)
            #show_four_kinds_of_lines_with_local_part(main_events,secondary_events,third_events,remaining_noise3,label='Events',roi_bounds=roi)
            #show_some_events(initial_events,image,label="initial_events")
            #show_some_events(main_secondary_third_events,image,label='main_secondary_third_events')
            show_some_events(remaining_noise3,image,label='remaining_noise3')

            #show_some_events(noise_events,image,label='remaining_noise1')
            show_some_events(main_events,image,label='main_events')
            show_some_events(main_second_events,image,label='main_second_events')
            show_some_events(secondary_events,image,label='secondary_events')
            show_some_events(remaining_noise,image,label='remaining_events2')
            show_some_events(third_events, image, label='third_events')






            print(k)

        old_algorithm(flow, x, y, p, t, t_ref, rangeX, rangeY)
        def new_algorithm(flow, x, y, p, t, t_ref, rangeX, rangeY):
            (ref,main_events, mx, my,secondary_events, secondary_x,secondary_y,
             remaining_noise2, noise_x, noise_y,nx,ny,main_secondary_events)=dist_main_second_noise2(flow, x, y, p, t, t_ref, rangeX, rangeY)


            result = count_events_within_distance(main_events,secondary_events,remaining_noise2,4,0.001)


            main_secondary_third_events,third_events,remaining_noise3=separate_third_events(result,main_secondary_events,remaining_noise2,m=4,n=3,l=2)

            #show_some_events(secondary_events,image,label='secondary_events')
            #show_some_events(main_secondary_third_events,image,label='main_secondary_third_events')
            #show_lines(main_events, t_ref, label="main_secondary_third_events")
            #show_lines(main_secondary_events, t_ref, label="main_secondary_third_events")
            return main_secondary_third_events
            show_lines(main_secondary_third_events, t_ref, label="main_secondary_third_events")
            print(k)



        new_algorithm(flow, x, y, p, t, t_ref, rangeX, rangeY)