'''
Developer: Sharina Stubbs
Version: 1.0
Description: A web app written using Python, HTML, CSS, Pandas, GeoPy to take data within a CSV file
and add latitude and longitudinal data to each data point. Output is presented directly on the
web page, and as a downloadable file.
Last Updated: Sept 28, 2018
'''


from flask import Flask, render_template, request, send_file
from geopy.geocoders import Nominatim
import pandas
import datetime

app=Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/success_table", methods=['POST'])
def address_table():
    global filename
    if request.method=="POST":
        file=request.files['file']
        try:
            df=pandas.read_csv(file)
            gcoder=Nominatim()
            df["Coordinates"]=df["Address"].apply(gcoder.geocode)
            df["Latitude"]=df["Coordinates"].apply(lambda x: x.latitude if x != None else None)
            df["Longitude"] = df["Coordinates"].apply(lambda x: x.longitude if x != None else None)
            df=df.drop("Coordinates",1)
            filename=datetime.datetime.now().strftime("uploads/%Y-%m-%d-%H-%M-%S-%f"+".csv")
            df.to_csv(filename,index=None)
            return render_template("index.html", text=df.to_html(), btn='download.html')
        except:
            return render_template("index.html", text="Please make sure the file you are uploading is a CSV file, and that it has an Address column. Then, please try again!")

@app.route("/download-file/")
def download():
    return send_file(filename, attachment_filename='yourfile.csv', as_attachment=True)

if __name__ == "__main__":
    app.debug=True
    app.run()
