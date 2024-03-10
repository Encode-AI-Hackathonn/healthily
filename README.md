# Healthily Project
AI Hackathon by Encode 8-10 March 2024 Canary Wharf.

## Team members
Giulio, Varun, Timur, Nistha, Mesbah

## Description
We used the Healthily DOT platform API to match users with appropriate services based on their symptoms. We tried to rebalance the knowledge asymmetry between patient and healthcare professional by creating a UI (chat app) where the user interacts with the Healthily Smart Symptom Checker, answering questions. At the end of the Symptom Checking, the user receives:
- A consultation report with the overall triage and possible causes for the reported symptoms.
- A list of the five nearest NHS organisations providing services related to the possible cause of the symptoms. For each organisation, the name, address, distance from the user's location and list of relevant services are given.
- es. Symptom Checker determines that the possible cause of the cold is a covid infection --> the user is given the list of the nearest 5 pharmacies/hospitals to test for covid.

The following APIs have been used:
- Healthily Smart Symptom Checker API
- NHS Service Search API - organisations (version2)

## Requirements
- requirements.txt for pip dependencies
- create a .env file with the APIs tokens and keys: HEALTHILY_KEY, HEALTHILY_TOKEN, 
NHS_PK, NHS_SK
