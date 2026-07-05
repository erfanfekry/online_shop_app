import http


conn = http.client.HTTPSConnection("api.sms.ir")
payload = "{\n  \"mobile\": \"9921056926\",\n  \"templateId\": 130765,\n"\
"\"parameters\": [\n    {\n      \"name\": \"FULLNAME\",\n      \"value\": \"Asgar\"\n    },"\
"\n{\n        \"name\":\"CODE\",\n        \"value\":\"123456\"\n    }\n  ]\n}"
headers = {
    'Content-Type': 'application/json',
    'Accept': 'text/plain',
    'x-api-key': 'CUbdri4GHW2nmfbt7WqYMRZ5Gx5nz3SRy1POOJfIPCbCf2xu'
}
conn.request("POST", "/v1/send/verify", payload, headers)
res = conn.getresponse()
data = res.read()





