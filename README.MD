## Binance algo (TEMA) trading bot

### Description
Task was to recreate Triple EMA (TEMA) strategy that works same as [this script](https://www.fmz.com/strategy/363572). And since this indicator is repainting some improvements were made:
- Script checks bar only at first 10 seconds of 1 minute bar
- Signal prints, sent to telegram and saved to csv file if state was changed
- This script is also designed to work multithreaded, so it can be used for multiple pairs at once
- In ```/utils/func.py``` there is a function ```open_pos``` that can be used to open/close/modify long and short positions (already implemented for binance api), but it is not used in this script.

#### Rules:
- Checking for long if:
  - TEMA of open price < TEMA of close price

- Checking for short if:
  - TEMA of open price > TEMA of close price

- If current state changed from long to short or vice versa, then signal is printed, sent to telegram and saved to csv file.

    
#### Technologies used:
- *Python*
- *Binance API*
- *TA Lib Python*
- *Pandas*


#### Configuring:
- Install ```requirements.txt```.
- Change API key and secret for binance and telegram notifications in ```.env.dist```, rename it to ```.env```. 
- Run ```python tema_complete.py``` in ```/``` directory.


#### Contributing
Pull requests are welcome. For major changes please open an issue first to discuss what you would like to change.