## TKOM - filtr pakietów HTTP

[![Build Status](https://travis-ci.org/LuXuryPro/tkom.svg?branch=master)](https://travis-ci.org/LuXuryPro/tkom)
[![Coverage Status](https://coveralls.io/repos/github/LuXuryPro/tkom/badge.svg?branch=master)](https://coveralls.io/github/LuXuryPro/tkom?branch=master)

## Install
```bash
pip install git+https://github.com/LuXuryPro/tkom
```

## Usage
```bash
http-filter -i input.txt 'url if method == "GET"'
http-filter -i input.txt 'method if host =~ "pl"'
```

## Update
```bash
pip install -U git+https://github.com/LuXuryPro/tkom
```
