
## Sales Dialer

To run test cases

```
|-- salesapi
    |-- tests
        |-- tests_billing
            |-- utils
                |-- constant.py
```


```bash
    Go to salesapi/tests/tests_billing/utils/constant.py file
    Put login credential
    Put workspace information
```
To change test data for test cases
```bash
    Navigate to
    salesapi/tests/tests_billing/utils/test_data.py
    Change test data as per the requirments of cases
```


Run test cases using command
```
|-- salesapi
    |-- tests
        |-- tests_billing
            |--tests_campaign_call
                |--TestCases

```

```bash
pytest salesapi/tests/tests_billing/tests_campaign_call/test_campaign_call_billing.py::TestCampaignCall -v
```



