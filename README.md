# AWSRyanairCrawler

Web crawler app that collects price information from the Ryanair website. The app uses AWS Dynamodb to store information and can be executed for example on AWS ECS as a periodic task.

Standalone execution is possible as  follows, the  AWS access key needs IAM permissions to create tables in Dynamodb and put data into them.

```bash
docker run -it --rm -e FROM=BUD -e TO=BCN -e AWS_ACCESS_KEY_ID=XXX -e AWS_SECRET_ACCESS_KEY=YYY gdanii/fly bash /app/start.sh
```

For the (really simple) web GUI to work, an AWS Cognito Identity Pool registration is needed with read access for Dynamodb.