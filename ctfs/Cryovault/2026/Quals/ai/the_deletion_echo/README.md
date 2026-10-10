d3va

The Deletion Echo
A regression service says a deletion request was fulfilled by exact retraining. Recover the deleted records and their private labels. Submit one record-id:label string per deleted record, sorted as ASCII strings, as a JSON list. Then run:

python3 unlock.py '["record-...:0", "record-...:3", ...]'
