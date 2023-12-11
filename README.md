# py-atomic-weights: Python Module for Standard atomic weights of the elements

## Features
* [IUPAC Atomic Weights](https://iupac.qmul.ac.uk/AtWt/) in `float` and `decimal.Decimal` formats

## Usage

```
pip install git+https://github.com/n-takumasa/py-atomic-weights
```

```py
>>> import atomic_weights as atw
>>> print(atw.Fe)
55.845
>>> print(atw.decimal.Fe)
55.845
>>> type(atw.Fe)
<class 'float'>
>>> type(atw.decimal.Fe)
<class 'decimal.Decimal'>
```
