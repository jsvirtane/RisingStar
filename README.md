# Rising Star Pre-assingment
Project is a pre-assignment for [Vincit Rising Star-program] (https://vincit.hire.trakstar.com/jobs/b8f3e8bc4bd54b5da23950e7f222d427).

## Installation
You need Python 3 installed on your machine to run this project. [Virtual environment] (https://docs.python.org/3/tutorial/venv.html) is recommended. 

1. Open Python interpreter
2. Install requirements with package manager [pip] (https://pip.pypa.io/en/stable/)
```bash
pip install -r requirements.txt
```
3. Import Crypto.py file
```python
from Crypto import * 
```

## Usage
```python
# Initialize coin (Bitcoin for now) and date range 
Bitcoin = Crypto()

#Get date and value of the highest volume during selected range
Bitcoin.top_volume_24h()

#Get longest bearish trend during selected range (bearish = price of day N is lower than price of day N-1)
Bitcoin.longest_bear()

#Find best days to buy and sell between selected range for optimal profit
Bitcoin.check_optimal_dates()

#Update range of days
Bitcoin.update_range()
```

## Author
© Jami Virtanen


