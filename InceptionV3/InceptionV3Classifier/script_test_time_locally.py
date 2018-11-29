import requests
import matplotlib.pyplot as plt
import numpy as np


import classify_image

def tic():
    #Homemade version of matlab tic and toc functions
    import time
    global startTime_for_tictoc
    startTime_for_tictoc = time.time()

def toc():
    import time
    if 'startTime_for_tictoc' in globals():
        print("Elapsed time is " + str(time.time() - startTime_for_tictoc) + " seconds.")
    else:
        print("Toc: start time not set")


def toc_time():
    import time
    return time.time() - startTime_for_tictoc

with open('../InceptionV3Classifier/imagenet_synset_to_human_label_map.txt') as f:
    whole_labels = f.read().split("\n")

dict_labels = {}
for cll in whole_labels:
    if len(cll) >= 2:
        dict_labels[cll.split("\t")[0]] = cll.split("\t")[1]

        
number_images = 10

#url_base =  "https://inditexapp.azurewebsites.net/api/InceptionV3Classifier?img="
#url_base =  "http://localhost:7071/api/InceptionV3Classifier?img="

with open("./fall11_urls_first_2000.txt","r") as f:
    whole_file = f.read().split("\n")
    

ltime = []
for idx_image in range(number_images):
    cimage_url = whole_file[0].split("\t")[1]
    cimage_label = whole_file[0].split("\t")[0]
    print(cimage_url)
    
    tic()
    #url = url_base + cimage_url

    #r = requests.post(url)
    classify_image.run_inference_on_image(cimage_url)
    #dd  = r.json()
    ltime.append(toc_time())
    print(ltime)
    
    #print(idx_image, dict_labels[cimage_label.split("_")[0]], dd)
    
if False:
    """
    First attempt, in case that the graph needs to be generated again
    """
    ltime = [26.585001230239868, 5.283040523529053, 17.73598027229309, 2.593003749847412, 11.248939037322998, 2.8200619220733643, 16.670985221862793, 3.09599232673645, 11.502059698104858, 4.071980237960815, 5.934020519256592, 9.711987972259521, 3.0849857330322266, 9.33296251296997, 14.225001096725464, 2.841944694519043, 11.897971153259277, 8.175994634628296, 9.545000314712524, 9.329044342041016, 3.074040412902832, 16.126007795333862, 7.4029624462127686, 11.5600426197052, 3.250026226043701, 10.976969957351685, 3.347991943359375, 7.9989013671875, 16.665969133377075, 12.187048435211182, 3.6619510650634766, 9.953018426895142, 4.9029927253723145, 7.4029929637908936, 19.406497955322266, 3.731994390487671, 18.588664293289185, 9.653867244720459, 6.47782039642334, 19.050623893737793, 3.897918462753296, 19.40959143638611, 3.9949188232421875, 13.648678302764893, 3.9149134159088135, 11.525783777236938, 16.96566653251648, 12.292791366577148, 16.960097551345825, 4.2869017124176025]

plt.plot(ltime,'x-')
plt.xlabel("Attempt")
plt.ylabel("Time in seconds")
plt.title("Average time per classification = %1.2f s and standard deviation %1.2f\n%s "%(np.mean(ltime), np.std(ltime), whole_file[0].split("\t")[1]))
plt.savefig("test_average_time_b" + ".png", dpi=600)
plt.show()

