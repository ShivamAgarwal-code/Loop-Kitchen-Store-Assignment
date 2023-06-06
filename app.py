from threading import Thread
from flask import Flask, render_template, request
from flask import make_response
from query_db import trigger_report, get_final_report_status, deserialize_report

app = Flask(__name__, template_folder="templates")

reportID = 0
report_message = ''

@app.route('/', methods=['GET'])
def home():
    global reportID, report_message
    if(reportID > 0):
        report_message = "Latest report generated "+str(reportID) 
        return render_template('home.html', report_message=report_message)
    else:
        return render_template('home.html')

@app.route('/trigger_report/', methods=['GET','POST'])
def request_trigger_report():
    global reportID, report_message
    reportID += 1
    
    thread = Thread(target=trigger_report, args=(str(reportID),))
    thread.start()

    report_message = "Latest report generated "+str(reportID)
    return render_template('home.html', report_message=report_message)

@app.route('/check_report_status/', methods=['POST'])
def check_report_status():
    global report_message
    reportID = str(request.form['reportID'])
    try:
        is_complete = get_final_report_status(reportID)
    except Exception as e:
        return render_template("home.html", report_message = report_message, check_message="Report with ID "+str(reportID)+" is invalid!")

    if is_complete:
        df = deserialize_report(reportID)
        print(df)
        resp = make_response(df.to_csv())
        resp.headers["Content-Disposition"] = "attachment; filename=export"+str(reportID)+".csv"
        resp.headers["Content-Type"] = "text/csv"
        
        return resp
    else:
        return render_template("home.html", report_message = report_message, check_message = "Generation of report "+str(reportID)+" running")


if __name__ == '__main__':

    app.run(host='0.0.0.0', debug=True)
