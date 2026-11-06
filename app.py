from flask import Flask, render_template 
app = Flask(__name__)
            
            
@app.route('/') 
def home(): 
    return render_template('index.html')
    
@app.route('/tribute') 
def tribute(): 
    return render_template('tribute.html')
     
@app.route('/cat_gallery') 
def cat_gallery(): 
    return render_template('cat_gallery.html')
    
@app.route('/cat_painting')
def cat_painting():
    return render_template('cat_painting.html')

@app.route('/balance_sheet')
def balance_sheet():
    return render_template('balance_sheet.html')

if __name__ == '__main__': app.run(debug=True)