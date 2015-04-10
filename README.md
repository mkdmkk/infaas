Inference-as-a-Service (INFaaS)
======
# Overview
Inference-as-a-Service (INFaaS) a cloud form of a situation inference platform which provides a core set of common functionality required to develop various context-aware apps.
Currently INFaaS utilizes scikit-learn for inference algorithms and MongoDB for data management.

# Installation
1. Clone the project, INFaaS, from the Git repository.
2. Install the dependencies: Django, MongoDB, scikit-learn, numpy

I recommend you to use PyCharm for IDE.

# APIs

## Contexts Management
### Retrieve Contexts
* Signature: [GET] {YOUR_BASE_URL}/api/contexts
* URL Parameters
    * query: a MongoDB query statement for retrieving contexts
    * limit: the number of contexts to retrieve
* Example) [GET] {YOUR_BASE_URL}/api/contexts?limit=100
## Save Contexts
* Signature: [POST] {YOUR_BASE_URL}/api/contexts
* POST Body: A JSON form of data
    * Structure: {“source”, “type”, “time”, “data”}
## Delete Contexts
* Signature: [DELETE] {YOUR_BASE_URL}/api/contexts
* POST Body: A MongoDB query statement for deleting searched contexts

## Domains Management
### Retrieve Domains
* Signature: [GET] {YOUR_BASE_URL}/api/domains
### Save Domains
* Signature: [POST] {YOUR_BASE_URL}/api/domains
* POST Body: A JSON form of data
    * Structure: {“id”, “name”, “version”, “description”, “situations”}
### Delete Domains
* Signature: [DELETE] {YOUR_BASE_URL}/api/domains
* POST Body: A MongoDB query statement for deleting searched domains

## Solutions Management
### Retrieve Solutions
* Signature: [GET] {YOUR_BASE_URL}/api/solutions
### Save Solutions
* Signature: [POST] {YOUR_BASE_URL}/api/solutions
* POST Body: A JSON form of data
    * Structure: {“id”, “domain”, “alg”, “baseset”, “visibility”, “features”, “conf”}
### Delete Solutions
* Signature: [DELETE] {YOUR_BASE_URL}/api/solutions
* POST Body: A MongoDB query statement for deleting searched solutions

## Inference
* Signature: [DELETE] {YOUR_BASE_URL}/api/infer
* POST Body: ‘application’ specification
