# Wine Quality Prediction

Wine Test ML is a Apache Spark Machine learning model to predict the quality of wine based on certain properties.

## Installation

The prediction application comes inside a docker container if you would rather not install anything on your machine.

If you want to run it without Docker, you must install the following packages:

* [Java version 7 or later](https://www.oracle.com/java/technologies/javase/javase-jdk8-downloads.html)
* [Python 3.6+](https://www.python.org/downloads/release/python-386/)
* [Anaconda (for python)](https://www.anaconda.com/products/individual)
* [Apache Spark](http://spark.apache.org/downloads.html)

Required Python packages. Save this to requirements.txt and run `pip install -r requirements.txt`

```
numpy==1.19.4
pandas==1.1.5
py4j==0.10.9
pyspark==3.0.1
pyspark-stubs==3.0.0.post1
python-dateutil==2.8.1
pytz==2020.4
six==1.15.0
```

Follow this article to [install spark on Windows](https://medium.com/@GalarnykMichael/install-spark-on-windows-pyspark-4498a5d8d66c)



## Usage

Create a new directory with the CSV file that you want to run the prediction on and switch to that directory.

```bash
mkdir /data
cd /data
```
While inside this directory, run the following docker command to mount `/data` inside the container so that the application is able to access the CSV file.

:information_source: By default, this command will print only top 20 rows regardless of how many rows the input file has.

```bash
docker run --rm -v $(pwd):/data vaghanim/pyspark:1.0 <FileName.csv>
```

By default, the application return top 20 rows from the input file. User can choose to return specific number of rows by using the -o parameter.
The following argument will return 2000 rows.

```bash
docker run --rm -v $(pwd):/data vaghanim/pyspark:1.0 <FileName.csv> -o 2000
```


## License
[MIT](https://choosealicense.com/licenses/mit/)