"""
Lecture 7: Cloud computing

To do computation in the cloud, we need:

0. An account / security credentials

1. A place to store data

2. A way to do computations.

=== Getting started ===

You need an AWS account.

Be careful about signing up for AWS!
All services cost money!

Examples:
- https://www.reddit.com/r/aws/comments/oe2don/a_storyi_did_a_mistake_in_our_aws_account_that/
- https://www.reddit.com/r/aws/comments/g1ve18/i_am_charged_60k_on_aws_without_using_anything/
- https://www.reddit.com/r/aws/comments/1906h1t/do_you_have_an_aws_horror_story/

The other thing that can happen is that resources improperly configured can get hacked and compromised very quickly:

- https://www.reddit.com/r/aws/comments/vb27pu/is_someone_using_my_ec2_instance_for_crypto/
- https://securitylabs.datadoghq.com/articles/tales-from-the-cloud-trenches-ecs-crypto-mining/
- https://www.reddit.com/r/aws/comments/119admy/300k_bill_after_aws_account_hacked/

I haven't personally used this, but I recommend signing up for an educational account through something like AWS Educate:

https://aws.amazon.com/education/awseducate/

UC Davis also has something called AggieCloud that we will be using for the purposes of today's lecture.

https://cloud.ucdavis.edu/aggiecloud

This is available to researchers & administrators -- for example if you are involved in research with a faculty member, you can get them to sign up for an AggieCloud account using research funding.

=== Some general advice before we begin ===

Warning:
Everything is going to be more difficult than you think it is!
:)

A lot of AWS (and other cloud providers -- Azure, Google Cloud)
is very complicated with endless configuration options, settings, and
setup to get things to work.

Some people expect it to "just work" -- it won't!
Managing stuff in the cloud has a steep learning curve, for two main reasons:

- Target audience:
  Services are targeted to expert industrial users who have a lot of experience
  and support in getting what they want. They often care more about features
  and configurability.
  "It's possible to get it to work and be eficient and reliable" matters more,
  not "It works out of the box without any problems".

  Imagine you are working at a company, if you need to spend 1 day to get your
  app to work that's not a big deal, what you care is that you can configure it
  programmatically and that it is performant and reliable.

- Security:
  Everything has to balance usability with security. There are all sorts of
  hoops we have to jump through to make sure we are a trusted user and not
  a malicious bot that is trying to access our service. We will see some
  examples of this below.

=== 0. Account security credentials ===

Once you have an AWS account, you access your resources in two primary ways:

- Through the web interface

- Through the CLI (shell).
  This is also typically how you would access AWS instances through Python.

  https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html

First let's try running this.

    aws s3 ls

This is supposed to list all S3 buckets associated with your account. What happens?

The problem:
-

Assuming you have an AWS account, you would then go here:

    https://portal.aws.amazon.com/

And select IAM to create a new user.
(Show how this works)

Once you have a user, you can go to "Security credentials"
for that user.

There are a number of ways to log in and set up credentials, but let's try the one
that AWS suggested above:

    aws configure

What does it ask for?

We can create an "access key" to get this to work
and get our credentials configured.
Once we have done this:

    aws s3 ls

What do we see?

=== 1. Storing data ===

S3 (Simple Storage Service) is one of Amazon's oldest services.

Let's try a few commands:

    aws s3 help

(what do we see?)

API reference:

    https://docs.aws.amazon.com/AmazonS3/latest/API/Type_API_Reference.html

Major commands:

    ls
    aws s3 ls
    aws s3 ls s3://119-test-bucket-2

    mb
    aws s3 mb s3://test-bucket-3
    aws s3 ls

    cp
    aws s3 cp file.txt s3://119-test-bucket-2/file.txt
    aws s3 ls s3://119-test-bucket-2

    rb

We have to prefix files with s3:// for this to work.

Did it work?
Let's check!

Go to:

    https://console.aws.amazon.com/

=== Exercise ===

Exercise:
Create a Python function that lists all the S3 buckets available and puts them into
a list.
"""

import subprocess

def list_s3_buckets():
    # Capture stdout
    # result = subprocess.run(["aws", "s3", "ls"], check=True, stdout=subprocess.PIPE)
    # TODO
    raise NotImplementedError

# Uncomment to run
# list_s3_buckets()

"""
=== Full S3 API ===

There's also something called the S3 API which offers a lot more options.
We can use it like so:

    aws s3api help

    aws s3api list-buckets

    aws s3api get-object --bucket 119-test-bucket-2 --key file.txt /dev/stdout

What happens when we do the following?

    aws s3api get-object --bucket some-other-bucket --key file.txt /dev/stdout

=== Troubleshooting (a digression on cloud policies) ===

Everything in the cloud is about security.
There is something called a "policy" which is attached to any cloud resource.
It basically tells you who can do what with the resource:

- Who (principal)
- Can do (allow or deny)
- What (action)
- On what (resource)

Some examples:
https://docs.aws.amazon.com/AmazonS3/latest/userguide/example-bucket-policies.html

Through the console:

    https://console.aws.amazon.com/

There's a nice tool we can use here:

    https://aws.amazon.com/blogs/aws/aws-policy-generator/

    example-policy.json

Also useful:

    aws iam list-users

As with everything else, we can also access these through the S3 API:

    aws s3api get-bucket-policy --bucket 119-test-bucket-2

=== How S3 works ===

S3 uses something called "blob storage".
What is blob storage?

https://en.wikipedia.org/wiki/Object_storage

Blob storage is usually contrasted with two other types of storage:

- File storage

- Page or block storage

And can also be contrasted with:

- DB storage

    DynamoDB:
    https://aws.amazon.com/dynamodb/

    RDS:
    https://aws.amazon.com/rds/

    Aurora:
    https://aws.amazon.com/rds/aurora/

How big can an S3 file storage be?

- Up to 5 TB!

    https://stackoverflow.com/questions/37880961/aws-dynamodb-over-aws-s3

Keep in mind,
you pay for the storage you use.
So storing a 5 TB file for a long period of time is probably not a good idea.
"""

def dont_run_this():
    with open("bigfile.txt", "w") as f:
        for i in range(100_000_000):
            # Save new line to file
            f.write(f"{i}\n")

    # Upload to S3
    # aws s3 cp bigfile.txt s3://119-test-bucket-2/bigfile.txt
    subprocess.run(["aws", "s3", "cp", "bigfile.txt", "s3://119-test-bucket-2/bigfile.txt"], check=True)

"""
=== 2. Doing computations ===

The last part of the lecture we can do a short demo of doing computations.

Compute is available in AWS through different means, but the most popular are:

- EC2 (Elastic Compute Cloud)

- Lambda

We will cover EC2. Try this:

    aws ec2 help

    aws ec2 describe-instances

Generally to create an instance the process is:

- We create the instance online on the web interface
    (Warning - we need to remember to delete it or we will be charged $$$)

- We select the various settings for the instance
    (Warning - some settings can be expensive)

- We then access the instance through the CLI, typically by SSH into the instance
  directly.

In the console again:

    https://console.aws.amazon.com/

=== How EC2 Works ===

Some people are surprised to learn that EC2 are basically just virtual machines.
It's like having a computer running linux, it doesn't have any other fancy setup
beyond that.

An important distinction is between virtual machines & real machines.
You can actually pay more in EC2 to get a real, physical machine dedicated to yourself
(but it costs a lot more!)
We may see this in the settings above while setting EC2 up based on the "instance type".

Nowadays some people want more programmatic options where for example, you
create a computation in the cloud that is just a Python function.

Or, you might want a computation that is triggered by an event, for example,
- every time an order comes in, run your function
- every day at 6am, run your function

Terms:
- This is sometimes known as event-driven or asycnchronous programming
- Also related to serverless computing and microservices

For these use cases you can use AWS Lambda.

However I would put a general word of advice against structuring too much using
microservices.
It tends to be more expensive to break up your app into various sub-computations
and will be cheaper just to run a monolithic EC2 instance.

There was a famous post about this from Prime Video
(now taken down, but available thanks to the Internet Archive):

    Back to the Monolith: Why Did Amazon Dump Microservices?
    https://nordicapis.com/back-to-the-monolith-why-did-amazon-dump-microservices/

    Scaling up the Prime Video audio/video monitoring service and reducing costs by 90%
    https://web.archive.org/web/20240717095641/https://www.primevideotech.com/video-streaming/scaling-up-the-prime-video-audio-video-monitoring-service-and-reducing-costs-by-90

And just for fun:

    https://www.youtube.com/watch?v=y8OnoxKotPQ

The general takehome point is that microservices are good for convenience
and separation of concerns, but can introduce complexity
into your application and performance overheads.
Sometimes, just managing your own compute is faster and better.
"""
