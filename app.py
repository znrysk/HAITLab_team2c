from flask import Flask, request, render_template
from flask_mail import Mail, Message
from lsq_linear import calc

app = Flask(__name__, static_folder='./templates/images') 

app.config['MAIL_SERVER'] = '公開用'
app.config['MAIL_PORT'] = "公開用"
app.config['MAIL_USERNAME'] = "公開用"
app.config['MAIL_PASSWORD'] = "公開用"
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

mail = Mail(app)

@app.route('/')
def test1():
    return render_template('index.html')

@app.route('/input')
def test2():
    return render_template('checkbox.html')

@app.route('/result', methods=['POST','GET'])
def result():
    if request.method == 'POST':
      food_id_list_str = request.form.getlist('food')
      food_id_list = []
      for food_id_str in food_id_list_str:
        food_id_list.append(int(food_id_str))
      result = calc(food_id_list)[0]
      result2 = calc(food_id_list)[1]
      return render_template("result.html",result = result,result2 = result2)
    else :
      food_id_list_str = request.args.getlist('food')
      food_id_list = []
      for food_id_str in food_id_list_str:
        food_id_list.append(int(food_id_str))
      result = calc(food_id_list)[0]
      result2 = calc(food_id_list)[1]
      return render_template("result.html",result = result,result2 = result2)

@app.route('/team')
def team():
    return render_template('team.html')

@app.route('/contact_us')
def contact():
    return render_template('contact.html')

@app.route('/send_message',methods=['GET','POST'])
def send_message():
    if request.method == "POST":
      email = request.form['email']
      firstName = request.form['firstName']
      lastName = request.form['lastName']
      name = firstName + lastName
      message = request.form['message']

      msg = Message(
          subject = f"Mail from {name}", body=f"Name: {name}\nE-Mail: {email}\n\n\n{message}",
          sender = email, recipients=['haitlabteam2c@gmail.com'])
      # mail.body = email + message

      mail.send(msg)

      success = "Message sent. Thank you!"

    return render_template("contact_success.html", success=success)


if __name__ == "__main__":
  app.run()
