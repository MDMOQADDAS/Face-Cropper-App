from flask import *  
app = Flask("Face Cropeer App")  
 
@app.route('/')  
def home():  
    return render_template("index.html")  
 
@app.route('/crop', methods = ['POST'])  
def success():  
    if request.method == 'POST':
        name=request.form.get("name")
        email=request.form.get("email")
        message=request.form.get("message")  
        f = request.files['file']  
        f.save(f.filename)  
        import cv2
        import numpy
        #cv2.imwrite("myimage.jpg" , photo)
        #----------------------
        try:
            img = cv2.imread(f.filename)
            face_croper = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
            #--------------------------------
            crop_area = face_croper.detectMultiScale(img)
            x1 = crop_area[0][0]
            y1 = crop_area[0][1]
            x2  = x1 + crop_area[0][2]
            y2 = y1 +crop_area[0][3]
            #---------------------------------
            crop_image = img[y1:y2 , x1:x2]
            cv2.imwrite("Face_Cropped_image.jpg" , crop_image)
            #------------------ For mail
            import smtplib
            import imghdr
            from email.message import EmailMessage

            Sender_Email = "SENDER@GMAIL.COM"
            Reciever_Email = email
            Password = "SENDER@PASSWORD" #input('Enter your email account password: ')

            newMessage = EmailMessage()                         
            newMessage['Subject'] = message
            newMessage['From'] = Sender_Email                   
            newMessage['To'] = Reciever_Email                   
            newMessage.set_content('Thanks For choosing!!') 

            with open('Face_Cropped_image.jpg', 'rb') as f:
                image_data = f.read()
                image_type = imghdr.what(f.name)
                image_name = f.name

            newMessage.add_attachment(image_data, maintype='image', subtype=image_type, filename=image_name)

            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                
                smtp.login(Sender_Email, Password)              
                smtp.send_message(newMessage)
            return render_template("success.html") 
        except :
            return template_rendered("err.html")
        finally:
            home()
         
  
if __name__ == '__main__':  
    app.run(debug = True)  