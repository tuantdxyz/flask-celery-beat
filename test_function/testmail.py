from flask import Flask, request, render_template
from flask_mail import Mail, Message

app = Flask(__name__)

# 465(SSL),587(TLS)
## configuration of gmail --> test ok
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'mailserverpg01@gmail.com'
## use the app password created for gmail
## https://myaccount.google.com/security
app.config['MAIL_PASSWORD'] = 'iyyvfyricnzsoruf'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_DEFAULT_SENDER'] = 'mailserverpg01@gmail.com'

## configuration of fptmail --> test ok
# app.config['MAIL_SERVER'] = 'mail.fpt.com.vn'
# app.config['MAIL_PORT'] = 587
# app.config['MAIL_USERNAME'] = 'FPT.einvoice.OnPrem@fpt.com.vn'
# app.config['MAIL_PASSWORD'] = 'Admin@12345'
# app.config['MAIL_USE_TLS'] = True
# app.config['MAIL_USE_SSL'] = False
# app.config['MAIL_DEFAULT_SENDER'] = 'FPT.einvoice.OnPrem@fpt.com.vn'

# instantiating the mail service only after the 'app.config' to avoid error
mail = Mail(app)


@app.route("/sendmail", methods=['GET', 'POST'])
def home():
    try:
        # if it is a post request
        if request.method == 'POST':
            sender = app.config['MAIL_DEFAULT_SENDER']
            recipient = 'tun320xx@gmail.com'
            message = 'hello kitty'
            subject = 'title kitty'

            # inputing the message in the correct order
            msg = Message(subject, sender=sender, recipients=[recipient])
            msg.body = message
            mail.send(msg)
            return "message Sent"
        # return render_template('mail.html')
    except Exception as e:
        print(e)
        return None


if __name__ == '__main__':
    # for app to run and debug to True
    app.run(debug=True)
