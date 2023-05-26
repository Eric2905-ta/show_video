import time

import cv2
import psycopg2
from flask import Flask, Response, render_template

app = Flask(__name__)

def get_data():
    # Establish a connection to the PostgreSQL database
    conn = psycopg2.connect(
        host="localhost",
        port="5432",
        database="mydb",
        user="postgres",
        password="eric"
    )

    # Create a cursor object to interact with the database
    cur = conn.cursor()

    # Execute the SQL query to fetch data from the "testob" table
    cur.execute("SELECT * FROM testob WHERE state > 3")
    # Fetch all the rows returned by the query
    data = cur.fetchall()

    # Get number of persons in roid A
    cur.execute("SELECT COUNT(ID) AS NUMA FROM testob WHERE roid = 'A'")
    dataA = cur.fetchone()[0]

    # Get number of persons in roid B
    cur.execute("SELECT COUNT(ID) AS NUMB FROM testob WHERE roid = 'B'")
    dataB = cur.fetchone()[0]

    # Get number of persons in roid C
    cur.execute("SELECT COUNT(ID) AS NUMC FROM testob WHERE roid = 'C'")
    dataC = cur.fetchone()[0]

    # Get number of persons in roid D
    cur.execute("SELECT COUNT(ID) AS NUMD FROM testob WHERE roid = 'D'")
    dataD = cur.fetchone()[0]

    # Close the cursor and the database connection
    cur.close()
    conn.close()

    return data, dataA, dataB, dataC, dataD

def generate_messages(data):
    messages = []
    for element in data:
        message = f"ID {element[0]} in area {element[3]} needs support"
        messages.append(message)
    return messages

def gen():
    """Video streaming generator function."""
    cap = cv2.VideoCapture('static/videos/test_lab_2.mp4')

    # Read until video is completed
    while(cap.isOpened()):
      # Capture frame-by-frame
        ret, img = cap.read()
        if ret == True:
            img = cv2.resize(img, (0,0), fx=0.5, fy=0.5) 
            frame = cv2.imencode('.jpg', img)[1].tobytes()
            yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            time.sleep(0.1)
        else: 
            break



@app.route('/')
def index():
    # Get data from the database and the number of persons in each roid
    data, dataA, dataB, dataC, dataD = get_data()

    # Generate the messages
    messages = generate_messages(data)

    # Render the template with the messages and person counts
    return render_template('app.html', messages=messages, dataA=dataA, dataB=dataB, dataC=dataC, dataD=dataD)



        

@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run()
