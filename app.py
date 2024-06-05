from flask import Flask, request, render_template
from src.pipeline.prediction_pipeline import PredictPipeline, CustomData
import logging

app = Flask(__name__)
app.logger.setLevel(logging.DEBUG)

@app.route('/')
def home_page():
    return render_template("index.html")

@app.route("/predict", methods=["GET", "POST"])
def predict_datapoint():
    if request.method == "GET":
        return render_template("form.html")
    else:
        print("hello")
        data = CustomData(
            departure_time=request.form.get("departure time"),
            arrival_time=request.form.get("arrival time"),
            duration=request.form.get("Duration"),
            date=request.form.get("Date"),
            airline=request.form.get("Airline"),
            stops=request.form.get("stops"),
            flight_class=request.form.get("Class"),
            source=request.form.get("Source"),
            destination=request.form.get("Destination")
        )
        print("transforming data to dataframe...")
        final_data = data.get_data_as_dataframe()
        print("printing head data to dataframe...")
        print(final_data.head())
        predict_pipeline = PredictPipeline()


        pred = predict_pipeline.predict(final_data)

        result = round(pred[0], 2)

        return render_template("result.html", final_result=result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
