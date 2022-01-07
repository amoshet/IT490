#! /usr/bin/python3.8
from DatabaseClient import databaseClient
tester = databaseClient()
variable = {'type' : "test"}
response = tester.call(variable)
print(response)
