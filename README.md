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
