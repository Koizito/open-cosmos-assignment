# DataCosmos Backend Challenge Project

## Introduction

You will need to build a service which can store, parse and offer access to data points received from an external source.

We expect you to spend around 10 hours total on this project.

Candidates are free to use any available open-source software as long as its license allows free commercial use.

There is no restriction about the environment the binary must run in.

There is no restriction on the programming language to be used.

## Objective

Create a service which can 

- fetch the data exposed by the server included as a binary with the project files - see below for details on how to run the server
- store this in a persistent data store - there are no requirements on which type of data store to use, you may choose
- implement and apply the business rules around these data which are described below
- allow access to the stored data from the service with some filters described below - there are no requirements around the method of access, you may choose

Create a solution that you consider as close to production-ready as possible. Focus on quality rather than quantity.

## Running the Data Server

The command

```
./data-server --port 28462
```

will start the server listening (insecurely, i.e. no TLS) for `GET` requests on port `28462`.

Each `GET` request will return either

- a 200 response containing a single data point, whose format is given below
- a 404 response if no data point is currently available

## Data Format

### From Data Server

Each successful "message" from the server contains JSON data in the format

```
{
    "time": int         // UNIX timestamp in seconds
    "value": []number   // the data value, byte encoded
    "tags": []string    // a set of tags associated with the value
}
```

The value is a little-endian byte encoding of a float32.

## When Accessed From Service

Users who will access data from the service require those data to be provided in the format, 
and include at least as much information, as follows

```
[
    {
        "time": string     // ISO8601 timestamp
        "value": number    // the 
    },
    // ...
]
```

## Business Rules

Data whose timestamp is "too old" should be treated as invalid and discarded. "Too old" means the data are timestamped more than 1 hour previous to the current time.

The server does some basic analysis on the data, and adds tags which both describe the data & possibly the outcomes of the analysis. Data internal to the system are tagged
with "system" and should be discarded. If the server believes the data to be inaccurate, it will tag those data points with "suspect". 
Potentially inaccurate data should be discarded.

It must be possible for an administrator of the service, but not necessarily the end user of the service (/API), to discover which data points have been discarded and why they were discarded

## Data Filtering

Users of the service who access the data must be able to filter the data by start and/or end times. All of these filters must be optional.

In other words, users must be able to access

- all data points
- data points generated after a certain datetime
- data points generated before a certain datetime
- data points generated within a set datetime range

## Expected output

Candidates are expected to: 

- Provide the source code (link to a public repository or packed into some kind of archive)
- Include clear instructions on how to execute this code
- Prepare a short presentation (~10 minutes) about the solution used, the approach taken, the main challenges and next steps
