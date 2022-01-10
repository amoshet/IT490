#!/usr/bin/python3.8
from frontendClient import backendClient
tester = backendClient()
variable = {'type' : "test"}
response = tester.call(variable)
print(response)
