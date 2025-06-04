#!/usr/bin/env python
import sys
import warnings

from datetime import datetime

from stock_picker.crew import StockPicker

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

def run():
    """
    Run the crew.
    """
    inputs = {
        'sector': 'Technology'
    }
    
    result = StockPicker().crew().kickoff(inputs=inputs)
    
    # print result
    print('\n\n --- Final Decision ---')
    print(result.raw)
