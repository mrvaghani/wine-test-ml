from pyspark.ml.feature import VectorAssembler
from pyspark.ml.regression import LinearRegression
from pyspark.ml.regression import LinearRegressionModel
from pyspark.sql import SparkSession
import shutil


if __name__ == "__main__":
	
	spark = SparkSession\
        .builder\
        .appName("wine-training")\
        .getOrCreate()

	
	dataset = spark.read.csv('/data/TrainingDataset.csv',header='true', inferSchema='true', sep=';')
	validationdataset = spark.read.csv('/data/ValidationDataset.csv',header='true', inferSchema='true', sep=';')

	dataset.printSchema()
	validationdataset.printSchema()
	print("Rows: %s" % dataset.count())
	print("Rows: %s" % validationdataset.count())
	
	
	# We want everything except quality
	# attr_columns = [c for c in dataset.columns if c != 'quality']
	
	# create and configure the assembler
	#assembler = VectorAssembler(inputCols=attr_columns, outputCol="Attributes")
	
	assembler = VectorAssembler(inputCols=[dataset.columns[1], dataset.columns[2], dataset.columns[3], dataset.columns[4], dataset.columns[5], dataset.columns[6], dataset.columns[7], dataset.columns[8], dataset.columns[9],dataset.columns[10] ], outputCol = 'Attributes')
	
		
	output = assembler.transform(dataset)


	data_final = output.select("Attributes",dataset.columns[11] )
	data_final.show()

	valid_output = assembler.transform(validationdataset)

	valid_data_final = valid_output.select("Attributes",validationdataset.columns[11] )
	valid_data_final.show()
	

	# Split training data into 80% and 20%
	train_data,test_data = data_final.randomSplit([0.8,0.2])
	regressor = LinearRegression(featuresCol = 'Attributes', labelCol = dataset.columns[11] )

	# Train using training data 
	regressor = regressor.fit(train_data)

	pred = regressor.evaluate(test_data)

	# Predict the model
	pred.predictions.show()

	predictions = regressor.transform(valid_data_final)
	predictions.show()

	# Save the model so that we can export it for later use
	regressor.write().overwrite().save("trained-model")

	path_drv = shutil.make_archive("trained-model", format='zip', base_dir="trained-model")
	shutil.unpack_archive("trained-model.zip", "trained-model-sample",format='zip',)

	loadedRegressor = LinearRegressionModel.load("trained-model-sample/trained-model")
	predictions = loadedRegressor.transform(valid_data_final)
	print(loadedRegressor.numFeatures)
	predictions.show()

	spark.stop()
