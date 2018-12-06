# TopTweets
This repository is a tutorial for Twitter REST API.

You may use Git to clone the repository from GitHub and install it manually: 
```
git clone https://github.com/nukopy/TopTweets.git
cd TopTweets
```

## how to use

For using twipy, you need to register Twitter Application for OAuth sertification. After you did, you can use twipy.

### prepare API key

After you got API key, you should have 4 types of keys:

* CONSUMER_KEY
* CONSUMER_SECRET
* ACCESS_TOKEN
* ACCESS_SECRET

You need these keys when you use twipy for generate API instance. In the following,  .

config.ini

```config
[OAuth]
CONSUMER_KEY = **********
CONSUMER_SECRET = **********
ACCESS_TOKEN = **********
ACCESS_SECRET = **********
```

```python
from configparser import ConfigParser

config = ConfigParser()
config.read('config.ini')
section = 'OAuth'
CK = config.get(section, 'CONSUMER_KEY')
CS = config.get(section, 'CONSUMER_SECRET')
AT = config.get(section, 'ACCESS_TOKEN')
AS = config.get(section, 'ACCESS_SECRET')
api = twipy(CK, CS, AT, AS)

```

or

```python
import config

api = twipy(CS, CS, AT, AS)

```

or

```python
import os

```


