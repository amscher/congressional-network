congressional-network
=====================

CS 224w Network Analysis Project

Congressman.py
--------------
- Defines the Congressman class, and is used to ingest all the info about a congressman...


Bill.py
-------
- Defines the Bill class and is used to ingest all the info we need about a Bill.


CongressmenData.py
-----------------
- Generates the data/legislator-data.json filed described below
- dataMapFromFile(): allows you to retrieve a map with thomas ids as keys and Congressman objects as values.
- Functions that allow you to add more data per congressman to the data/legislator-data.json file.


data/legislator-data.json
--------------------------
To reload this file run..
  python CongressmenData.py
  python CommiteeNetworkData.py

This file contains a lot of the calculated info we need for each legislator...
You can access each legislator's infor using their thomas id.
One legislators info looks like this...
  "00414": {
    "committeesMap": {
      "HSAP15": 3,
      "HSAP02": 1,
      "HSAP": 4,
      "HSAP10": 2
    },
    "name": "Rodney P. Frelinghuysen",
    "num_leader_roles": 0,
    "num_terms": 10,
    "committee_pagerank": 0.0036348023504737975,
    "party": "Republican",
    "bills": [
      "hr2103",
      "hr2104",
      "hr4870",
      "hjres91",
      "hr2609",
      "hr712",
      "hjres76"
    ],
    "thomas_id": "00414",
    "num_success_bills": 2
  }
-committeesMap: is a dict of the committee ids that they are a part of, along with
their rank in that commitee. Rank == 1, means they are the chair of that committee.
-num_terms: number of terms in office total
-committee_pagerank: this is the page rank score for the legislator in the directed graph
where nodes are legislators, and edges go from legislators to the chair of a committee they are a member.
-bills: the bills that they have sponsored
-num_success_bills: the number of bills that they've sponsored that have been enacted

The rest is pretty self explanatory



data/bill-data.json
-------------------
This file synthesizes a lot of the info that we need for bills, and makes it much
faster to ingest the data than called readBills all the time.
Each bill can be indexed by it's id, and one bill object looks like this...
  "s2040": {
    "status": "PASS_OVER:SENATE",
    "committees": [
      "SLIA"
    ],
    "bill_type_id": "s",
    "num_voting_rounds": 1,
    "bill_id": "s2040",
    "introduced_at": "2014-02-25",
    "num_passed_rounds": 1,
    "cosponsors": [
      "01896",
      "00250"
    ],
    "introduced_month": 2,
    "sponsor": "00250"
  }
-committees: the list of committees that the bill was referred to
-cosponsors: list of thomas ids of cosponsors
-sponsor: thomas id of sponsor
The rest is pretty self explanatory


data/committee-data.json
------------------------
This file synthesizes a lot of the info that we need about a commiteee.
Each committee can be indexed by it's thomas id, and one committee object looks like this...
  "HSAG": {
    "name": "HSAG",
    "numbills": 429,
    "bill_success_rate": 0.013986013986013986,
    "bill_outcomm_rate": 0.11655011655011654,
    "btwnness_score": 216.55789961314116,
    "chair": "",
    "thomas_id": "House Committee on Agriculture"
  }
-bill_success_rate: the percentage of successful bills of the bills referred to that committee in the 112th congress
-bill_outcomm_rate: the percentage of bills reported out of committee out of the bills referred to that
committee in the 112th congress
-btwnness_score: The betweenness centrality of the committee in a graph where the committees are nodes
and the edges are shared members.




