# Introduction 
This repository contains setup guides for the [Ticketpilot](www.ticketpilot.ai) application. Setting up 
Ticketpilot on your premises requires access to the private rwai container registry - you should make sure you have access before 
starting any of these guides.

### Currently available

[Minimal-install](minimal-install/doc/mininal-install.md) explains how to set up a minimal installation of ticketpilot including 
the core module _tp_api_ (including outward facing api and database) and an LLM connection, enabling simple use cases such as 
ticket summarization.


### Under construction
Setting up additional modules such as:
- Document extraction, pii detection
- Hybrid vector/semantic search
  - automated data ingestion
- Custom classifiers i.e. text sentiment analysis
