# CloudFormation Template for Recipe Image Processing

This repository contains a CloudFormation script and Lambda code for setting up an AWS architecture to upload recipe images to an S3 bucket, process them with Lambda, upload the resulting markdown to another S3 bucket, and then send them to Confluence. This README provides an overview of the contents of the `CloudFormation` subfolder.

## Contents

1. [CloudFormation Script (`cloudformation_template.yml`)](#cloudformation-script)
2. [Lambda Code](#lambda-code)

### CloudFormation Script

The CloudFormation script, `cloudformation_template.yml`, defines the AWS resources required for the recipe image processing workflow. Here's an overview of the key components and their functions:

- **Parameters:** This section allows you to specify input parameters for the CloudFormation stack. The parameters include the `LambdaCodeBucket` parameter, which is used to specify the S3 bucket containing the Lambda code.

- **Resources:** This section defines various AWS resources required for the workflow, including:
  - IAM User and Access Key for uploading images to S3.
  - S3 Bucket for input recipe images with event notifications.
  - SQS Queue for handling image notifications.
  - Lambda function (`Img2MdLambda`) for processing images.
  - Event source mapping for triggering the Lambda function.
  - S3 Bucket for storing markdown files.
  - Lambda function (`ConfluenceUploaderLambda`) for uploading to Confluence.
  - Event source mapping for triggering the Confluence uploader Lambda.
  - IAM Role with necessary permissions for Lambda functions.

### Lambda Code

The Lambda code for processing images and uploading to Confluence is included in this repository. You should upload the Lambda function code (as a ZIP file) to the S3 bucket specified in the `LambdaCodeBucket` parameter prior to running the CloudFormation template. Once uploded, fill in the Lambda's env vars with your details.

## Getting Started

To set up the recipe image processing workflow, follow these steps:

1. Upload the Lambda function code to the S3 bucket specified in the `LambdaCodeBucket` parameter.
2. Use AWS CloudFormation to deploy the `cloudformation_template.yml` script. You can use the AWS Management Console, AWS CLI, or any other method you prefer for CloudFormation deployment.
3. Configure the Lambda settings by filling in the env vars.
4. Once the stack is created and lambda's configured, the architecture will be set up, and images uploaded to the input S3 bucket will trigger the processing workflow.

## Additional Information

For more details on how this architecture works and its usage, refer to the CloudFormation script (`cloudformation_template.yml`) and the documentation for the Lambda functions.

If you encounter any issues or have questions, please feel free to open an issue or contact the repository owner for assistance.

Happy image processing! 📷🍽️

![Designer Template Vis](/cloudformation/images/cloudformation-template-designer.png)