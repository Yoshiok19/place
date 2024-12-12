# Server-less r/place clone

 Server-less r/place clone. Uses AWS lambda, API Gateway, DynamoDB or Cassandra Keyspaces, EventBridge, 

  - Uses Lambda and API Gateway to hanlde socket events
  - Uses Elasticache (Redis OSS)
  - CloudFront to server static files (Can also use EC2 or run it locally using Node)
  - DynamoDB/Cassandra for persistent storage
  - EventBridge for scheduling
  - On a VPC with 3 subnets, an internet gateway and a NAT gateway.

 ## VPC Setup:

  - Default VPC starts with 3 subnets in 3 availability zones and an internet gateway.
1. Create a public NAT Gateway and place it on one of the subnets
2. Create one route table with rows:
  - 0.0.0.0/0     	  ->      Internet Gateway address
  - 172.31.0.0/16 ->      local
3. Create another route table with rows:
  - 0.0.0.0/0         ->      NAT Gateway address
  - 172.31.0.0/16 ->      local
    
4. Associate two subnets to the private route table (the route table with the NAT gateway mapping). These two subnets are private because the route table does not contain a mapping to the internet gateway.
5. Associate one subnet to the public route table (the route table with the Internet gateway mapping). This subnet is public.

Note: The NAT Gateway should be placed on the public subnet


 
