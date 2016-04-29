# Query Service Low Level Design

## Contents
+ [About](#about)
+ [Classes](#classes)
+ [Resource Relationship](#resource-relationship)
  + [Asset](#asset)
  + [Offer](#offer)

## About
The query service enables the discovery of assets and their offers.

## Classes
+ assets
+ offers

## Resource Relationship

### Asset
An **asset** is searchable once it has been onboarded into a repository and the
index service has updated itself by getting these changes from the repository
service.

### Offer
An **asset** can have many **offers** assigned to it. Each offer will contain
a set of *rules* under which the **asset** can be used.

## Get asset offers
![](./images/sequence-get-asset-offers.png)

## Get assets licensors
![](./images/sequence-get-assets-licensors.png)
