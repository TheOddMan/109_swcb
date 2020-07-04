import numpy as np
import matplotlib.pyplot as plt
from keras.engine.saving import model_from_json
from annoy import AnnoyIndex
import os
from keras.models import Model
from PIL import Image as pil_image
import json
import warnings
warnings.filterwarnings("ignore")


#讀取 AutoEncoder
def preparingLatentModel():

    with open(AEConfig, "r") as text_file:
        json_string = text_file.read()
        AE = model_from_json(json_string)
        AE.load_weights(AEWeightsName)


    # print(AE.summary())

    AE_output = AE.get_layer(AE_output_name).output
    latent_model = Model(inputs=AE.input, outputs = AE_output)

    # print(latent_model.summary())

    return latent_model

#將 ImgDir影像經過 Encoder的特徵 vector儲存在 index檔，以圖搜圖時會用這個檔案進行
def build_annoy_index(encoding_dim, num_trees, annoy_index_file, encodings):
    ann = AnnoyIndex(encoding_dim)
    for index, encoding in enumerate(encodings):
        ann.add_item(index, encoding)
    ann.build(num_trees)
    ann.save(annoy_index_file)
    print("Created Annoy Index Successfully")
    return ann



#將 ImgDir影像輸入 Encoder輸出特徵 vector  並將特徵 vector儲存在 index檔，以圖搜圖時會用這個檔案進行
def saveToAnnIndex():
    encoding_vectors = []
    count = 0

    #迭帶 ImageDir內的影像
    for root, _, files in os.walk(imageDir):
        for file in files:

            train_image = pil_image.open(os.path.join(root,file))

            #將影像縮放到與 02_01_AE.py訓練時的輸入層的 size一致，這樣才有辦法輸入至 Encoder
            train_image = train_image.resize(input_size, pil_image.ANTIALIAS)
            train_image = np.expand_dims(np.asarray(train_image),axis=0)

            #將 ImgDir影像輸入 Encoder輸出特徵
            pred = latent_model.predict(train_image)
            encoding_vectors.append(pred)
            count+=1
            print("Count :",count)

    print("Len of encoding vector :",len(encoding_vectors))


    encoding_vectors = np.array(encoding_vectors).reshape(len(encoding_vectors), AE_Output_Size)
    encoding_vector_length = AE_Output_Size

    #將特徵 vector儲存在 index檔
    build_annoy_index(encoding_vector_length, num_trees, annoy_file_name, encoding_vectors)


#將 ImgDir內的影像轉換成 vector後儲存至 .npy檔
#將 ImgDir內的影像名稱儲存至 .npy檔
def saveImg2np():
    imageNpys = None
    count = 0

    #迭帶 ImageDir內的影像
    for root, _, files in os.walk(imageDir):
        for file in files:

            train_image = pil_image.open(os.path.join(root,file))

            #將影像縮放至統一大小，這邊的大小與02_01_AE.py訓練時的輸入層的 size可以不用一致
            #這邊的大小主要是在顯示前十筆相似的影像時，十張影像的大小
            train_image = train_image.resize(search_size, pil_image.ANTIALIAS)
            train_image = np.expand_dims(np.asarray(train_image),axis=0)


            if imageNpys is None:
                imageNpys = train_image
            else:
                imageNpys = np.vstack([imageNpys,train_image])

            count += 1
            print("Count :",count)

    print("imageNpys shape :",imageNpys.shape)

    #儲存影像 vector
    np.save(imgNpy_file_name,imageNpys)

    imgNames = []

    count=0

    #迭帶 ImageDir內的影像
    for root, _, files in os.walk(imageDir):
        for file in files:
            imgNames.append(file)

            count += 1
            print("Count :",count)

    imgNames = np.asarray(imgNames)
    print("imgNames shape :",imgNames.shape)

    # 儲存影像名稱
    np.save(imgNpy_file_name.split(".")[0]+"_names.npy", imgNames)


#執行以圖搜圖涵式
def imageRetrieval(returnJson):

    #讀取影像輸入至 Encoder輸出的特徵
    ann = AnnoyIndex(AE_Output_Size)
    ann.load(annoy_file_name)



    #讀取要拿來搜尋的影像
    train_image = pil_image.open(imageToSearch)
    train_image_for_display = train_image.resize(search_size, pil_image.ANTIALIAS)
    train_image = train_image.resize(input_size, pil_image.ANTIALIAS)
    train_image = np.expand_dims(np.asarray(train_image),axis=0)

    #將要拿來搜尋的影像輸入至 Encoder輸出影像特徵
    #並進行以圖搜圖
    pred = latent_model.predict(train_image)
    pred = pred.reshape(AE_Output_Size)

    #搜尋前10筆最相似的影像
    nn_indices=ann.get_nns_by_vector(pred,10)

    imgNpy = np.load(imgNpy_file_name)
    imgNamesNpy = np.load(imgNpy_file_name.split(".")[0] + "_names.npy")




    if returnJson:

        imgNamesList = []

        for index in nn_indices:
            i = {'name':imgNamesNpy[index]}
            imgNamesList.append(i)

        return imgNamesList
    else:
        #顯示前10筆最相似的影像

        plt.figure(figsize=(18, 8))
        for i, index in enumerate(nn_indices,1):
            image = imgNpy[index]
            ax = plt.subplot(3,5,i+5,)
            plt.xticks([])
            plt.yticks([])
            ax.axis("off")
            ax.text(0.5, -0.1, imgNamesNpy[index].replace(".jpg",""), size=10, ha="center",
                          transform=ax.transAxes)
            plt.imshow(image)

        axSearch = plt.subplot(3,5,3,)
        plt.xticks([])
        plt.yticks([])
        axSearch.axis("off")
        axSearch.text(0.5,-0.1, imageToSearch, size=10, ha="center",
                 transform=axSearch.transAxes)
        plt.imshow(train_image_for_display)
        plt.show()



abPath = os.path.join("D:\\","XinYu","109_swcbProject_server","pyScripts")
# abPathImg = os.path.join("D:\\","XinYu","109_swcbProject_server")
abPathImg = os.path.join("D:\\","XinYu","109_swcbProject","swcb01","swcb01")

AEConfig = os.path.join(abPath,'modelAE.config')

AEWeightsName = os.path.join(abPath,'model-206-0.015-0.015_weight.hdf5')

AE_output_name = 'conv2d_6'

AE_Output_Size= 7 * 7 * 128

imageDir = os.path.join("..","images","1-5000","CCTV")

imgNpy_file_name = os.path.join(abPath,'imgNpyFiles','swcb_imgnpy_1_5000.npy')

annoy_file_name = os.path.join(abPath,'annoyFiles','swcb_latents_20trees.annoy.index')

input_size=(224,224)

search_size = (200,200)

num_trees = 20



latent_model = preparingLatentModel()

# 1 表示只執行將 ImgDir內的影像和影像名稱轉換成 .npy檔
# 2 表示只執行將 ImgDir內的影像輸入至 Encoder後輸出特徵 vector儲存在 .index檔
# 3 表示只執行以圖搜圖

from argparse import ArgumentParser
parser = ArgumentParser()
parser.add_argument("--qi", help="Query Image",required=False,type=str)
args = parser.parse_args()
# print(os.getcwd())
imageToSearch = os.path.join(abPathImg,"SearchImage",args.qi)

ExecCode = 4

if ExecCode == 1:
    saveImg2np()
elif ExecCode == 2:
    saveToAnnIndex()
elif ExecCode == 3:
    imageRetrieval(returnJson=False)
elif ExecCode == 4:

    result = imageRetrieval(returnJson=True)
    json_str = json.dumps(result)
    json_str = "{'Images':"+json_str+"}" #{'Images':[{'name':'xxx.jpg'},{'name':'yyy.jpg'}]}

    print(json_str)

    # print(os.getcwd())




