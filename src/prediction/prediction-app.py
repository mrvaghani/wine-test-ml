from pyspark.sql import SparkSession
from pyspark.ml.evaluation import RegressionEvaluator
from pyspark.ml.regression import LinearRegressionModel
from pyspark.ml.feature import VectorAssembler
import sys
import os
import argparse


def readme():
	print("Usage:  643.py <filename>,  remember to mount the local directory if running in docker.")
	print("Usage:  and datafile must be in current directory.  ")
	print("Usage:  Windows: docker run --rm -v ""%cd%"":/data hp482/cs643:1 <filename> ")
	print("Usage:  PowerShell: docker run --rm  -v ${PWD}:/data hp482/cs643:1 <filename>")
	print("Usage:  Linux: docker run --rm -v $(pwd):/data hp482/cs643:1 <filename>")


def main():
	# TODO - Check if valid CSV file path
	input_file = sys.argv[1]


	spark = SparkSession \
		.builder \
		.master("local[*]") \
		.appName("cs643-prediction") \
		.getOrCreate()

	# TODO - This is how docker container file structure should be
	loaded_regression_model = LinearRegressionModel.load("/data/model/trained-model")

	# read dataset to predict
	input_dataset = spark.read.csv(input_file, header='true', inferSchema='true', sep=';')

	assembler = VectorAssembler(
		inputCols=[
			input_dataset.columns[1], input_dataset.columns[2], input_dataset.columns[3],
			input_dataset.columns[4], input_dataset.columns[5], input_dataset.columns[6],
			input_dataset.columns[7], input_dataset.columns[8], input_dataset.columns[9],
			input_dataset.columns[10]
		], outputCol="Attributes"
	)

	valid_output = assembler.transform(input_dataset)

	valid_finalized_data = valid_output.select("Attributes", input_dataset.columns[11])

	# predict the quality
	input_predictions = loaded_regression_model.transform(valid_finalized_data)

	data_eval = RegressionEvaluator(labelCol=input_dataset.columns[11], predictionCol="prediction", metricName="rmse")
	# r2 - coefficient of determination
	r2 = data_eval.evaluate(input_predictions, {data_eval.metricName: "r2"})
	print("\n\n\n")
	print("r2: %.3f" % r2)

	# Root Mean Square Error
	rmse = data_eval.evaluate(input_predictions)
	print("Root Mean Squared Error (RMSE): %g" % rmse)
	# Mean Square Error
	mse = data_eval.evaluate(input_predictions, {data_eval.metricName: "mse"})
	print("MSE: %g" % mse)
	# Mean Absolute Error
	mae = data_eval.evaluate(input_predictions, {data_eval.metricName: "mae"})
	print("MAE: %g" % mae)

	# Check if user provided how many rows to print
	if args.o is not None:
		input_predictions.show(int(args.o), truncate=False)
	else:
		input_predictions.show(truncate=False)


if __name__ == "__main__":
	my_parser = argparse.ArgumentParser(
		description='''This application requires a CSV file to predict wine quality. ''')
	my_parser.add_argument('path', type=str, help='The path to test data csv')
	my_parser.add_argument('-o', type=int, default=None, help='Number of rows to print')
	args = my_parser.parse_args()
	main()
