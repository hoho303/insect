from flask import Flask, request, render_template, send_file
import io
from PIL import Image
import requests
from tensorflow.python.keras.models import load_model
from tensorflow.python.keras.applications import imagenet_utils
from tensorflow.python.keras.preprocessing.image import img_to_array
from tensorflow.python.keras.preprocessing.image import load_img
import os
import numpy as np

app = Flask(__name__, template_folder='',static_folder="")
model = load_model('insect2.h5')
labels = ['AchatinaFulice', 'BoxelderBug', 'CabbageLooper', 'ColoradoPotatoBeetle', 'CottonwoodBorerBeetle',
          'CucumberBeetle', 'Cutworm', 'EpilachnaVigintioctopunctata', 'FleaBeetle', 'Grasshoppers',
          'GrayHairstreakButterfly', 'MediterraneanFruitFly', 'NezaraViridula', 'Riptortus', 'SquashBug']


def loadImage(imageInsect):
    if imageInsect.mode != 'RGB':
        imageInsect = imageInsect.convert('RGB')
    image = imageInsect.resize((200, 200))
    image = img_to_array(image)
    image = np.expand_dims(image, 0)
    image = imagenet_utils.preprocess_input(image)
    image = image / 255
    return image


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/detect', methods=['GET', 'POST'])
def upload():
    return render_template('search.html')

@app.route('/uploadFileByUrl', methods=['GET'])
def upload_file_by_url():
    url = request.args.get('url')
    filename = url.split('/')[-1]
    r = requests.get(url, allow_redirects=True)
    open(filename, 'wb').write(r.content)
    image = Image.open(filename)
    image = loadImage(image)
    predicts = model.predict(image)
    print(predicts)
    pred = np.argmax(predicts)
    if predicts[0][pred] > 0.7:
        os.remove(filename)
        return labels[pred]
    return "Con này không co"


@app.route('/uploadFileByImage', methods=['GET', 'POST'])
def upload_file_by_image():
    if request.method == 'POST':
        try:
            image = request.files["file"].read()
            image = Image.open(io.BytesIO(image))
            image = loadImage(image)
            predicts = model.predict(image)
            print(predicts)
            pred = np.argmax(predicts)
            if predicts[0][pred] > 0.7:
                return str(pred)
            return "Con này không co"
        except:
            return "Thí chủ có File không ?"

@app.route('/getImage',methods=['GET', 'POST'])
def return_files_tut():
	folder = request.args.get("id")
	file = request.args.get("file")
	try:
		return send_file('image/'+folder+'/'+file+'.jpg', attachment_filename='t.jpg')
	except Exception as e:
		return str(e)

@app.route('/download', methods=['GET', 'POST'])
def download():
    return send_file('insect.apk', attachment_filename='insect.apk')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port="5000")
