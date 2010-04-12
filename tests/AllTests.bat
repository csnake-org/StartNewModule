@echo off
REM --------------
REM Run the tests
REM --------------

REM Add the src folder to the python path
@set PYTHONPATH=../src;
REM Run all tests
@python AllTests.py
REM Let us see the results
@pause
