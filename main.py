from flask import Flask, redirect, url_for, request
app = Flask(__name__)

@app.route('/success/<name>')
def success(name):
   return 'welcome %s' % name

@app.route('/user',methods = ['POST', 'GET'])
def login():
   if request.method == 'POST':
      user = request.form['nm']
      print(user)
      return redirect(url_for('success',name = user))
   else:
      user = request.args.get('nm')
      return redirect(url_for('success',name = user))

@app.route('/register',methods = ['POST'])
def register():
    user_name = request.form['name']
    password = request.form['password']
    if user_name == 'admin' and password == 'admin':
        return "ok",200
    else:
        return "Sorry Your login attempt has failed"
    

if __name__ == '__main__':
   app.run()