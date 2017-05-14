# Indoor Health Monitor for Raspberry Pi

I made this because i have a couple of raspberry pi's with grovepi's
I don't have the same sensors for each one.

There are two main use cases.

* Record Data
    * Record data and look for trends.
    * When does the furnance kick on, what happens with dust when we vaccuum, etc.

* Alerting.
    * There is a gas leak
    * It is freakishly dusty

## Command Line Arguments

Two modes
1. Run in the background and poll all of the sensors writing to a sensor repo.
2. Test a sensor to see if it is working


Running the tests
python -m unittest discover -p '*_test.py'




## Configuration


settings.yaml



## Ideas for making this better

Write the data to AWS IOT

Add a rules engine dsl language like cloud custodian in order to author alerts
    Example
    policies:
    - name: dangerous-gas-levels
        resource: gas
        threshold: gt 50
        actions: pusheralert 

Take the same alerts and apply them to a mesh of sensors with more logic.
Like gas gt 50 and temp lt 30 or any gas gt 50


Senior Check in App
Mobile app that allows family members to say that they talked to Senior
ALso a way to register sensor.
An example would be a loudness sensor.  It would be super cool to see the loudness at a family members house to get an idea that they had watched tv that day.
Eventually train the data so it would know that you watched tv, etc.

Somethign like "Did you just watch tv?  from x to y?  You say yes, and the next time it records it.
That way you can get a feeling that your parent was watching tv, and is doing ok.
Kind of like a dashboard for your senior parents, with an activity log with sensor data and check in data.


## Python Testing Articles
[Pytest Asserts](https://docs.pytest.org/en/latest/assert.html)

[Mocking External APIs in Python](https://realpython.com/blog/python/testing-third-party-apis-with-mocks/)

[Python Mock Gotchas](http://alexmarandon.com/articles/python_mock_gotchas/)

[Python Patch Decorators](http://www.voidspace.org.uk/python/mock/patch.html#where-to-patch)

[Python Testing Tools](https://wiki.python.org/moin/PythonTestingToolsTaxonomy)

[Python Unit Testing with Mock - Part One](https://dev.to/mistermocha/python-unit-testing-with-mock---part-one)

[Python Unit Testing with Mock - Part Two](https://dev.to/mistermocha/python-unit-testing-with-mock---part-two)

[Python Mock Documentation](https://docs.python.org/3/library/unittest.mock.html)

