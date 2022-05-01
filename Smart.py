from typing import final
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras.models import load_model

import matplotlib.image as mpimg
import numpy as np
import PIL
from PIL import Image
from scipy import ndimage, misc
import json
import math

class Smart():
    tfLite_Model = ''
    tf_Model=''

    def __init__(self, tflite_model, tf_model):
        self.tfLite_Model = tflite_model
        self.tf_Model = tf_model

    def getImageJson(self, imgJSON):
        imgLIST = json.loads(imgJSON)
        imgNP = np.array(imgLIST)
        #print("List:",imgLIST)
        #print("Numpy: ",imgNP)
        #print("Image array size: ", imgNP.shape)

        #imgIMG = Image.fromarray(imgNP.astype('uint'))#.resize(50,30,1))
        return imgNP

    def interfaceClassification(self, img):
        #print(img)
        if(img[0][0]==1):
            print("Colin with if",5,"will receive the medicine")
            return 5
        else:
            print("Id not found")
        #print("I got it!")
        return 404

    def reshape_image(self, img):
        #image = np.reshape(img.shape[0],img.shape[0])
        #img = np.array([[[1,2,3],[1,2,3]],[[1,2,3],[1,2,3]],[[1,2,3],[1,2,3]]])
        #print(img.shape)
        #img = self.groupedAvg(img)
        k = 5
        inicioI = 0
        finalI = k
        inicioJ = 0
        finalJ=k
        print(img.shape)
        if(img.shape[0]==50 and img.shape[1]==30): 
            return img
        image = np.zeros((img.shape[0],img.shape[1]),dtype='float32')
        newImage = np.zeros((50,37),dtype='float32')
        #Colo gray
        for i in range(0,img.shape[0]):
            for j in range(0,img.shape[1]):
                r,g,b= img[i][j]
                image[i][j] = int(0.2989*r + 0.5970*g + 0.1140*b)

        #Reshape
        controlI = image.shape[0]//newImage.shape[0]
        controlJ = image.shape[1]//newImage.shape[1]
        inicioI = 0
        finalI = controlI-1
        inicioJ = 0
        finalJ= controlJ-1
        for i in range(0,newImage.shape[0]):
            for j in range(0,newImage.shape[1]):
                #print("aqui",inicioI, finalI, inicioJ, finalJ)
                calculate = image[inicioI:finalI][inicioJ:finalJ].mean()
                if (math.isnan(calculate)):
                  calculate = newImage[i][j]
                newImage[i][j] = float(calculate)
                inicioJ = finalJ + 1
                finalJ=(controlJ*(j+1))-1
                if(inicioJ>=image.shape[1]): inicioJ = image.shape[1]-1
                if(finalJ>=image.shape[1] or inicioJ>finalJ): finalJ = image.shape[1]-1
            inicioI = finalI +1
            finalI = controlI*i -1#i + k
            inicioJ = 0
            finalJ=(controlJ*(j+1))-1

            if(inicioI>=image.shape[0]): inicioI = image.shape[0]-1
            if(finalI>=image.shape[0] or inicioI>finalI): finalJ = image.shape[0]-1
            
            if(inicioJ>=image.shape[1]): inicioJ = image.shape[1]-1
            if(finalJ>=image.shape[1] or inicioJ>finalJ): finalJ = image.shape[1]-1

        print(img.shape)
        print(newImage.shape)

        return newImage
    
    def groupedAvg(myArray, N=5):
        result = np.cumsum(myArray, 0)[N-1::N]/float(N)
        result[1:] = result[1:] - result[:-1]
        return result
    
    def interfaceTF(self, img):
        model = load_model(self.tf_Model)
        img1 = self.reshape_image(img)#Image.fromarray(img).resize((50,37,1))
        print("Image of interface", img1.shape)

        image = np.expand_dims(img1, axis=0)
        predictions_array = model.predict(image)
        predicted_label = np.argmax(predictions_array)
        return str(predicted_label)

    def interfaceTFLite(self, img):
        image = self.reshape_image(img) #Image.fromarray(img).resize((50,37,1))
        print("Image of interface", type(image))

        tflite_interpreter = tf.lite.Interpreter(model_path=self.tfLite_Model)
        input_details = tflite_interpreter.get_input_details()
        output_details = tflite_interpreter.get_output_details()
        
        tflite_interpreter.resize_tensor_input(input_details[0]['index'], (50,37)) #(322, 50,37, 1)
        tflite_interpreter.resize_tensor_input(output_details[0]['index'], (1, 7))
        tflite_interpreter.allocate_tensors()
        input_details = tflite_interpreter.get_input_details()
        output_details = tflite_interpreter.get_output_details()

        tflite_interpreter.set_tensor(input_details[0]['index'], image) #send the image here
        tflite_interpreter.invoke()
        tflite_model_predictions = tflite_interpreter.get_tensor(output_details[0]['index'])
        print("Prediction results shape:", tflite_model_predictions.shape)
        return tflite_model_predictions

    def plot_result(tflite_model_predictions, image):
        target_names = ['Ariel Sharon', 'Colin Powell', 'Donald Rumsfeld', 'George W Bush', 'Gerhard Schroeder', 'Hugo Chavez', 'Tony Blair']
        tflite_predicted_ids = np.argmax(tflite_model_predictions, axis=-1)
        tflite_predicted_labels = target_names[tflite_predicted_ids[0]]
        #tflite_label_id = np.argmax(label_batch_test, axis=-1)

        plt.imshow(image, cmap="gray")
        plt.title(tflite_predicted_labels.title(), color="black")
        plt.axis('off')

    def modelImg(img):
        return img.shape

    def run(self):
        filename = "model_conv2D.h5"
        TFLITE_MODEL = "tflite_models/model_conv2d.tflite"
        image = mpimg.imread("tflite_models/george.jpg")
        #self.reshape_image(image)
        #tflite_model_predictions = self.interfaceTFLite(image)
        tf_model_predictions = self.interfaceTF(image)
        print("Prediction: ", tf_model_predictions)
        #self.plot_result(tflite_model_predictions, image)

if __name__ == '__main__':
    Brain = Smart("tflite_models/model_conv2d.tflite", "tf_models/model_conv2D.h5")

    Brain.run()
