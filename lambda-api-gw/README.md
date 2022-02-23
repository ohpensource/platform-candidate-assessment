# Movies Database API on Lambda with DynamoDb

## Exercise

So what do we want you to do?

### Deploy an API using Lambda an API Gateway with DynamoDb as the data store

Obviously that's not all we want you to do but it's a starting point. What you push back to the repository should be deployable in any AWS account with minimal changes. And if you want to use something other than API Gateway that's fine with us.

As this is a exercise for a devops role these are the things we're interested in:

#### Primary Focus

* infrastructure as code
    * your choice (but we do all our provisioning with Terraform or Cloudformation)

#### Secondary Focus

* automated deployments (ci/cd)
    * deploying your code automatically is foundational to devops
    * Bitbucket repositories come with built-in pipeline functionality
* scalability and availability
    * microservices should scale automatically
    * microservices should not be affected if a container stops responding
* observability
    * logs, traces and metrics are important for managing an application at scale
    * knowing when things go wrong is just as crucial
* security
    * as a financial organization we don't want just anyone to be able to access our applications
    * we also have strict risk/compliance rules so we need to be sure that third party code is safe/secure
* automated testing
    * knowing your infrastucture has deployed correctly

We realize this is a lot of stuff to implement when all you start with is  a basic python app - but you don't (and shouldn't) have to re-invent the wheel. Terraform Registry has a lot of modules that will help you out. Even so - we're not expecting you to implement everything - focus on what you think is important and go for quality over quantity.

As you can probably tell this is an exercise heavy on the "ops". If you want to show your dev skills, the API is only partially implemented, and probably not well coded in the first place. Feel free to extend and improve.

And lastly, if that wasn't enough, be creative and show us something we haven't thought of.

## Additional Info for the Exercise

### Lambda application

The app directory contains a partially implemented (python) API that queries a DynamoDb table that has been populated with a bunch of movies titles and related info.

The packages folder contains a script to create the necessary packages zip that should be used to create the required Lambda Layer.

#### Handler and Runtime

Because this is a flask application the handler should be specified as ```mvdb.app``` not ```lambda_handler```.
Application has been tested on runtime python3.8.

#### Environment Variables

* REGION
    * optional - if deploying to eu-west-1
    * AWS region where the API is deployed
* TABLE_NAME
    * required
    * the name of the dynamodb table

### DynamoDb Config

#### Table Configuration

The API is expecting the dynamodb table to have the following attributes:

* Partition key
    * year (number)
* Sort key
    * title (string)

#### Populate with movie data

Edit 'movies_load_data.py' with the deployed table name. Run the script to upload the data to dynamodb.

## Feedback

If you'd like to give us feedback on how we can improve this Candidate Assessment or problems/issues you ran into, either tell us in the interview or as part of PR.