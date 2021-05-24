This is a simple piece of code that writes out a normalized csv file (per some rules) from what it is given.
Assumptions made: 
- data will fit in memory
- input header structure should match output header structure
- Can key off those input headers being standardized (i.e. if you give this a header with 'TIMESTAMP' vs 'Timestamp' it won't work.)
- Lots of cleanup could be done
- Wrote one test to show what I was thinking in terms of test strategy, but it was faster to just focus on writing and testing by hand iteratively because data sizes of sample data were small

# Build / Install
It just uses the python3 standard libraries, so if you have python3 available it should work. Tested on Mac OS X 11.3.1.

# Running it
It takes input on stdin and outputs on stdout
python3 normalizer.py < input.csv > output.csv

# Running tests:
Ran out of time to write more detailed tests, but this is how you run what's there
python3 -m unittest test_normalizer.py
