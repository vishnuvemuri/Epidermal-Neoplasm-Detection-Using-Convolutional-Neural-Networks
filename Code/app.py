from flask import Flask, request, render_template, flash, redirect, url_for
from PIL import Image
import numpy as np
from tensorflow.keras.models import load_model
import base64
import io
import imghdr

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

model = load_model("C:/Users/dhanu/Desktop/Project/ResNet10.h5")
classes = {
    0: "actinic keratoses and intraepithelial carcinomae(Cancer)",
    1: "basal cell carcinoma(Cancer)",
    2: "benign keratosis-like lesions(Non-Cancerous)",
    3: "dermatofibroma(Non-Cancerous)",
    4: "melanocytic nevi(Non-Cancerous)",
    5: "pyogenic granulomas and hemorrhage(Can lead to cancer)",
    6: "melanoma(Cancer)",
}

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/", methods=["GET", "POST"])
def runhome():
    return render_template("home.html")

@app.route("/showresult", methods=["GET", "POST"])
def show():
    if request.method == "GET":
        flash('Please upload an image.', 'warning')
        return redirect(url_for("runhome"))

    if 'pic' not in request.files or request.files['pic'].filename == '':
        flash('No file selected.', 'warning')
        return redirect(request.url)
    
    pic = request.files["pic"]
    
    if not allowed_file(pic.filename):
        flash('INVALID FILE EXTENSION. Please upload an image file with extensions: .png, .jpg, .jpeg, .gif', 'warning')
        return redirect(request.url)

    img_bytes = pic.read()
    img_type = imghdr.what(None, img_bytes)
    if img_type not in ['jpeg', 'png', 'gif']:
        flash('Invalid image type. Please upload a valid image file (jpeg, png, gif)', 'warning')
        return redirect(request.url)

    inputimg = Image.open(io.BytesIO(img_bytes))
    if inputimg.mode != 'RGB':
        inputimg = inputimg.convert('RGB')
    inputimg = inputimg.resize((128, 128))
    img = np.array(inputimg).reshape(-1, 128, 128, 3)
    result = model.predict(img)
    result = result.tolist()
    max_prob = max(result[0])
    class_ind = result[0].index(max_prob)
    result = classes[class_ind]

    image_data = base64.b64encode(img_bytes).decode("utf-8")

    if class_ind == 0:
        info = "Actinic keratosis also known as solar keratosis or senile keratosis are names given to intraepithelial keratinocyte dysplasia. As such they are a pre-malignant lesion or in situ squamous cell carcinomas and thus a malignant lesion."
    elif class_ind == 1:
        info = "Basal cell carcinoma is a type of skin cancer. Basal cell carcinoma begins in the basal cells — a type of cell within the skin that produces new skin cells as old ones die off.Basal cell carcinoma often appears as a slightly transparent bump on the skin, though it can take other forms. Basal cell carcinoma occurs most often on areas of the skin that are exposed to the sun, such as your head and neck"
    elif class_ind == 2:
        info = "Benign lichenoid keratosis (BLK) usually presents as a solitary lesion that occurs predominantly on the trunk and upper extremities in middle-aged women. The pathogenesis of BLK is unclear; however, it has been suggested that BLK may be associated with the inflammatory stage of regressing solar lentigo (SL)1"
    elif class_ind == 3:
        info = "Dermatofibromas are small, noncancerous (benign) skin growths that can develop anywhere on the body but most often appear on the lower legs, upper arms or upper back. These nodules are common in adults but are rare in children. They can be pink, gray, red or brown in color and may change color over the years. They are firm and often feel like a stone under the skin. "
    elif class_ind == 4:
        info = "A melanocytic nevus (also known as nevocytic nevus, nevus-cell nevus and commonly as a mole) is a type of melanocytic tumor that contains nevus cells. Some sources equate the term mole with ‘melanocytic nevus’, but there are also sources that equate the term mole with any nevus form."
    elif class_ind == 5:
        info = "Pyogenic granulomas are skin growths that are small, round, and usually bloody red in color. They tend to bleed because they contain a large number of blood vessels. They’re also known as lobular capillary hemangioma or granuloma telangiectaticum."
    elif class_ind == 6:
        info = "Melanoma, the most serious type of skin cancer, develops in the cells (melanocytes) that produce melanin — the pigment that gives your skin its color. Melanoma can also form in your eyes and, rarely, inside your body, such as in your nose or throat. The exact cause of all melanomas isn't clear, but exposure to ultraviolet (UV) radiation from sunlight or tanning lamps and beds increases your risk of developing melanoma."
    else :
        info = "Please Upload the Skin Cancer Image, The Image Uploaded is not a Skin Cancer Image"

    return render_template("reults.html", result=result, info=info, inputimg=image_data)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
