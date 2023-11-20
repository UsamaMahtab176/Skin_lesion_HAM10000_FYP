# # Importing Required Libraraies
# import numpy as np
# import tensorflow as tf
# from skimage.io import imread
# from skimage.transform import resize
import pandas as pd



# df = pd.read_csv('C:\\Users\\DSC\\Desktop\\SkinAi\\app\\HAM10000_metadata.csv')

# # Loading the pre-trained model
# cnn_model = tf.keras.models.load_model('C:\\Users\\DSC\\Desktop\\SkinAi\\app\\CNN_FYP_Model96x96')

# labels_dict = {'akiec': 0, 'bcc': 1, 'bkl': 2, 'df': 3, 'mel': 4, 'nv': 5, 'vasc': 6}

# def prediction(path):
#     # Preprocessing the input_image according to model's requirements
#     image_size = (96, 96)
#     image_path=path
#     image = imread(image_path)
#     resized_img = resize(image, image_size)  # Resize to the model's input size
#     img_arr = np.array(resized_img)
#     img_arr = tf.expand_dims(img_arr,axis=0)

#     # Making predictions
#     predictions = cnn_model.predict(img_arr)

#     # Finding the predicted class
#     predicted_class = tf.argmax(predictions[0])
#     predicted_class = predicted_class.numpy().astype(int)

#     if predicted_class == 0:
#         disease = "Actinic keratosis (akiec)"
#         symptoms = '''Rough, scaly, or crusty skin patch or growth. 
#         Itching, burning, or tenderness in the affected area. 
#         Color variations, including pink, red, brown, or flesh-toned. 
#         The growth may be flat or raised, and it often feels dry.
#         '''
#         causes = '''
#             The primary cause of actinic keratosis is prolonged exposure to ultraviolet (UV) radiation from the sun or artificial sources like tanning beds. UV radiation can damage the DNA in your skin cells, leading to the development of these pre-cancerous growths.
#             '''
#         precautions = '''
#             Sun Protection: Protect your skin from the sun by wearing protective clothing, including long sleeves, hats, and sunglasses. Use sunscreen with a high SPF rating, and reapply it regularly when exposed to sunlight.
#             Limit Sun Exposure: Try to avoid direct sunlight during peak hours when UV radiation is strongest, typically between 10 a.m. and 4 p.m.
#             Regular Skin Checks: Perform self-examinations of your skin regularly to detect any changes, growths, or unusual patches. Consult a dermatologist if you notice any suspicious skin changes.
#             Seek Shade: When outdoors, seek shade under trees, umbrellas, or other structures to reduce your exposure to the sun.
#         '''
#         medications = '''
#             Topical Medications: Dermatologists often prescribe topical creams or gels that contain ingredients like imiquimod, fluorouracil, or diclofenac to help eliminate actinic keratosis lesions.

#             Cryotherapy: This involves freezing the affected skin with liquid nitrogen to destroy the AK lesions.

#             Curettage and Electrodessication: In this procedure, a dermatologist scrapes off the affected skin and then cauterizes the area.

#             Photodynamic Therapy (PDT): PDT involves applying a photosensitizing solution to the skin and then exposing it to a special light source to destroy the AK cells.

#             Laser Therapy: Lasers can be used to precisely target and remove actinic keratosis lesions.
#         '''
#     elif predicted_class ==1:
#         disease = "Basal cell carcinoma (bcc)"
#         symptoms = '''
#             A Pearly or Waxy Bump: BCC often appears as a flesh-colored or slightly pink, pearly bump. It may also have a translucent quality, like a drop of water on the skin.

#             A Flat, Scaly, or Crusted Area: Some BCCs may resemble a red or brown patch of skin that is flat, scaly, or crusty. It can be mistaken for a non-healing sore or eczema.

#             A Raised, Pink Growth: BCC can appear as a pink, raised growth that might bleed easily, form a crust, or develop an ulceration in the center.

#             Open Sore: In some cases, a BCC can develop into an open sore that doesn't heal, or it may heal and then return.
# '''
#         causes = '''
#         The primary cause of basal cell carcinoma is prolonged exposure to ultraviolet (UV) radiation from the sun or artificial sources like tanning beds. UV radiation damages the DNA in skin cells, leading to the development of cancerous growths.
#         '''

#         precautions = '''
#         Sun Protection: Protect your skin from the sun by wearing protective clothing, including wide-brimmed hats, long sleeves, and sunglasses. Use a broad-spectrum sunscreen with a high SPF rating and reapply it regularly when exposed to sunlight.

#         Seek Shade: Avoid direct sunlight during peak hours when UV radiation is strongest (typically between 10 a.m. and 4 p.m.).

#         Regular Skin Checks: Perform self-examinations of your skin regularly to detect any changes, unusual growths, or suspicious patches. Consult a dermatologist if you notice anything concerning.

#         Avoid Tanning Beds: Refrain from using tanning beds or sunlamps, as they emit harmful UV radiation.
# '''
#         medications = '''
#         Excision: Surgically cutting out the cancerous lesion.

#         Curettage and Electrodessication: Scraping away the tumor and then cauterizing the area.

#         Mohs Surgery: A specialized technique that removes the cancer layer by layer until no cancer cells remain.

#         Laser Surgery: Using lasers to remove the cancerous tissue.

#         Topical Medications: For superficial BCCs, topical creams or gels containing imiquimod or fluorouracil may be prescribed.

#         Radiation Therapy: In cases where surgery isn't possible, radiation therapy may be used.

# '''
#     elif predicted_class ==2:
#         disease = "Benign keratosis like lesions (bkl)"

#         symptoms = '''
#         Waxy or Stuck-on Appearance: BKL lesions may appear as if they are stuck onto the skin and have a waxy or translucent quality.

#         Brown or Light Brown Color: They are often brown or light brown in color, and their color may be uniform or vary.

#         Irregular Borders: BKL lesions may have irregular or well-defined borders.

#         Variable Size: They can range in size from small to larger growths.

#         Flat or Raised: BKL lesions may be flat against the skin or slightly raised.

# '''
#         causes = '''
#         The exact cause of BKL is not always clear, but they are generally considered benign skin growths. Some BKL lesions may be associated with other skin conditions, sun exposure, or genetics.
# '''
#         precautions = '''
#         Sun Protection: Protect your skin from the sun by wearing protective clothing and using sunscreen when spending time outdoors.

#         Regular Skin Checks: Perform self-examinations of your skin regularly to detect any changes, unusual growths, or suspicious patches.

#         Consult a Dermatologist: If you notice any changes in the appearance of skin lesions or growths, consult a dermatologist for a professional evaluation.
# '''
#         medications = '''
#         Biopsy: A small sample of the lesion is removed and examined under a microscope to determine its nature.

#         Cryotherapy: The lesion is frozen using liquid nitrogen to remove it.

#         Electrodessication and Curettage: The lesion is scraped away with a curette, and the base is cauterized.

#         Laser Therapy: Laser treatment may be used to remove certain types of lesions.

# '''

#     elif predicted_class ==3:
#         disease = "Dermatofibroma (df)"
#         symptoms = '''
#         Firm Bump: Dermatofibromas often present as small, firm, raised bumps on the skin. They may feel like hard nodules under the skin's surface.

#         Brownish Color: They are usually brownish in color, but the hue can range from light brown to dark brown or even reddish-brown.

#         Dimple or Depression: When you press on a dermatofibroma, it may dimple or create a depression in the center. This is known as the "buttonhole" sign.

#         Itching or Tenderness: Some dermatofibromas may cause itching or tenderness, although many are asymptomatic.

# '''
#         causes = '''
#         The exact cause of dermatofibroma is not well-understood, but it is generally considered a benign skin growth. They can sometimes develop at the site of a minor injury or insect bite, which may suggest that trauma or irritation could be a triggering factor.

# '''

#         precautions = '''
#         Sun Protection: Protect your skin from the sun by wearing protective clothing and using sunscreen when spending time outdoors.

#         Regular Skin Checks: Perform self-examinations of your skin regularly to detect any changes, unusual growths, or suspicious patches.

#         Consult a Dermatologist: If you notice any changes in the appearance of skin lesions or growths, consult a dermatologist for a professional evaluation.

# '''
#         medications = '''
#         Excision: Surgically cutting out the dermatofibroma.

#         Cryotherapy: Freezing the lesion with liquid nitrogen to remove it.

#         Laser Therapy: Using lasers to remove the lesion.
# '''
#     elif predicted_class ==4:
#         disease = "Melanoma (mel)"
#         symptoms = '''
#         Mole Changes: Melanomas often develop from existing moles but can also appear as new moles. Changes in the size, shape, color, or texture of a mole can be a warning sign.

#         Irregular Borders: Melanomas typically have irregular, notched, or blurred borders, unlike regular moles, which often have smooth, well-defined borders.

#         Asymmetry: If you draw a line through the middle of the lesion, one half may not match the other half in terms of size, shape, or color.

#         Varied Color: Melanomas can have multiple colors or uneven distribution of color within the lesion. Colors may include brown, black, red, blue, or white.

#         Diameter: Melanomas are often larger in diameter than a pencil eraser (about 6 mm or ¼ inch), but they can be smaller when first detected.

#         Evolution or Change: Any change in a mole's appearance, including itching, bleeding, or crusting, should be evaluated.

#         Elevation or Elevation: A melanoma may be raised or have an uneven surface.
# '''
#         causes = '''
#         The primary cause of melanoma is exposure to ultraviolet (UV) radiation from the sun or artificial sources like tanning beds. UV radiation can damage the DNA in melanocytes, leading to the development of cancerous cells.
#         '''

#         precautions = '''
#         Sun Protection: Wear protective clothing, including wide-brimmed hats and sunglasses, and use a broad-spectrum sunscreen with a high SPF rating. Reapply sunscreen regularly when exposed to sunlight.

#         Avoid Tanning Beds: Refrain from using tanning beds or sunlamps, as they emit harmful UV radiation.

#         Regular Skin Checks: Perform self-examinations of your skin regularly to detect any changes, unusual moles, or suspicious patches.

#         Seek Shade: Avoid direct sunlight during peak hours when UV radiation is strongest (typically between 10 a.m. and 4 p.m.).

# '''
#         medications = '''
#         The primary treatment for melanoma is surgical removal. Depending on the stage and depth of the melanoma, additional treatments such as lymph node biopsy, immunotherapy, targeted therapy, chemotherapy, and radiation therapy may be recommended.

#         The prognosis of melanoma greatly depends on the stage at which it is diagnosed. Early detection is key to successful treatment. If you notice any changes in the appearance of moles or any suspicious skin growths, consult a dermatologist immediately for a professional evaluation and appropriate treatment recommendations.
# '''
#     elif predicted_class ==5:
#         disease = "Melanocytic nevi (nv)"
#         symptoms = '''
#         Color: Moles can be tan, brown, black, red, pink, or even the color of the surrounding skin.

#         Size: Moles can range in size from very small to larger growths.

#         Shape: Moles can be round, oval, or irregularly shaped.

#         Surface: The surface of moles may be smooth, raised, flat, or slightly elevated.

#         Edges: Moles typically have well-defined edges that separate them from the surrounding skin.
# '''
#         causes = '''
#         The development of moles is usually influenced by a combination of genetic factors and exposure to ultraviolet (UV) radiation from the sun.
# '''
#         precautions = '''
#         Regular Skin Checks: Perform self-examinations of your skin regularly to detect any changes in the appearance, size, color, or shape of moles.

#         Consult a Dermatologist: If you notice any changes in moles, such as sudden growth, changes in color, bleeding, itching, or pain, consult a dermatologist for professional evaluation.
# '''
#         medications = '''
#         Biopsy: A small sample of the mole is removed and examined under a microscope to determine its nature.

#         Excision: Surgically removing the mole for further evaluation or due to cosmetic reasons.

#         Laser Removal: Using lasers to remove moles.

#         Cryotherapy: Freezing the mole with liquid nitrogen to remove it.
# '''

#     elif predicted_class ==6:
#         disease = "Vascular lesions (vasc)"
#         symptoms = ''''
#         Strawberry Hemangiomas: These are raised, red, or purplish lesions that often appear shortly after birth. They can grow rapidly during the first few months of life and typically shrink or fade over time.

#         Port-Wine Stains: These are flat, reddish-purple birthmarks that usually appear on the face. They do not go away on their own and may darken over time.

#         Spider Angiomas: These are small, red, spider-like lesions that may have a central red spot surrounded by smaller blood vessels. They can appear on the skin's surface and may be associated with liver disease.

#         Pyogenic Granulomas: These are bright red, raised lesions that can bleed easily. They often appear on the hands, arms, or face.

#         Venous Malformations: These are blue, soft, compressible lesions that occur due to abnormal veins. They can sometimes cause pain or swelling.
#         '''
#         causes = '''
#         The exact causes of vascular lesions are not always clear. Some may result from genetic factors, while others may occur due to abnormal development of blood vessels in utero.
# '''
#         precautions = '''
#         Regular Skin Checks: Perform self-examinations of your skin regularly to detect any changes in the appearance of vascular lesions.

#         Consult a Dermatologist: If you notice any changes in vascular lesions or if they cause discomfort, consult a dermatologist or healthcare professional for evaluation.
# '''
#         medications = '''
#         Observation: In some cases, no treatment is necessary, and the lesion may fade or shrink on its own.

#         Laser Therapy: Laser treatment can be effective for reducing or removing vascular lesions. Different types of lasers are used depending on the characteristics of the lesion.

#         Surgery: Surgical removal may be considered for certain types of vascular lesions.

#         Medications: Some medications, such as beta-blockers, can be used to treat specific vascular lesions.
# '''
    
#     return disease,symptoms,causes,precautions,medications

# # path = 'D:\\fyp\\HAM10000_images\\ISIC_0024360.jpg'
# # pred = prediction(path)
# # print(pred)

# # print(df[df['image_id']=='ISIC_0024360'])
# # # print("Predicted class:", predicted_class)

# # image_size = (28, 28)
# # image_path='C:\\Users\\DSC\\Desktop\\SkinAi\\uploads\\ISIC_0024360.jpg'
# # image = imread(image_path)
# # resized_img = resize(image, image_size)  # Resize to the model's input size
# # img_arr = np.array(resized_img)
# # img_arr = tf.expand_dims(img_arr,axis=0)

# # # Making predictions
# # predictions = cnn_model2.predict(img_arr)

# # # Finding the predicted class
# # predicted_class = tf.argmax(predictions[0])
# # predicted_class = predicted_class.numpy().astype(int)

# # print(predicted_class)
metadata = pd.read_csv("C:\\Users\\DSC\\Desktop\\SkinAi\\app\\HAM10000_metadata.csv")
print(metadata.head)