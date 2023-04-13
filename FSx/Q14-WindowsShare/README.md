# Q14-WindowsShare

## Question

```
A data processing facility wants to move a group of Microsoft Windows servers to the AWS Cloud. 
Theses servers require access to a shared file system that can integrate with the facility's existing Active Directory (AD) infrastructure for file and folder permissions. 
The solution needs to provide seamless support for shared files with AWS and on-premises servers and allow the environment to be highly available. 
The chosen solution should provide added security by supporting encryption at rest and in transit. 
The solution should also be cost-effective to implement and manage. 

Which storage solution would meet these requirements?

A. AN AWS Storage Gateway file gateway joined to the existing AD domain

B. An Amazon FSx for Windows File Server file system joined to the existing AD domain

C. An Amazon Elastic File System (Amazon EFS) file system joined to an AWS managed AD domain

D. An Amazon S3 bucket mounted on Amazon EC2 instances in multiple Availability Zones running Windows Server and joined to an AWS managed AD domain
```

## Answer

`B`


## Build the stack

```bash
sam build
sam deploy
```

## How to test:

## Cleanup

To delete the sample application that you created, use the AWS CLI. Assuming you used your project name for the stack name, you can run the following:

```bash
aws cloudformation delete-stack --stack-name Q14
```
