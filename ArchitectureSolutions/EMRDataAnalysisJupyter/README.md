# EMRDataAnalysisJupyter

This stack create a simple EMR cluster and install Hadoop / Spark an Livy in order to demonstrate running some Jupyter Notebook


## Build the stack

```bash
sam build
sam deploy
```

The [notebook](notebook.ipynb) is taken from [rahulomble/Exploratory-Data-Analysis](https://github.com/rahulomble/Exploratory-Data-Analysis)

## How to test:

Open the EMR console

## Cleanup

To delete the sample application that you created, use the AWS CLI. Assuming you used your project name for the stack name, you can run the following:

```bash
aws cloudformation delete-stack --stack-name EMRDataAnalysisJupyter
```
