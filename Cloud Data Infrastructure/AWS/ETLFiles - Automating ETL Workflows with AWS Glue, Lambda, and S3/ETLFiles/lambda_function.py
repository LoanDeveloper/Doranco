import json
import boto3
import os

    def lambda_handler(event, context):
        glue = boto3.client('glue')
        job_name = 'MyETLJob'  # Replace with your Glue job name

        # Start the Glue job
        response = glue.start_job_run(JobName=job_name)

        return {
            'statusCode': 200,
            'body': json.dumps('Glue job started successfully: {}'.format(response['JobRunId']))
        }
