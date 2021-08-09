## 30day
```python
# check if the string is integer
int_str.isdigit()

# convenient iterate
for i, doc in enumerate(documents):
    pass

print(dir(rolls))


# Roll 10 dice
rolls = numpy.random.randint(low=1, high=6, size=10)
rolls   # array([4, 4, 3, 1, 5, 1, 5, 2, 1, 2])
rolls + 10
# At which indices are the dice less than or equal to 3?
rolls <= 3

xlist = [[1,2,3],[2,4,6],]
# Create a 2-dimensional array
x = numpy.asarray(xlist)
print("xlist = {}\nx =\n{}".format(xlist, x))
x[1, -1]

# What does 1 + 1 not equal 2
import tensorflow as tf
# Create two constants, each with value 1
a = tf.constant(1)
b = tf.constant(1)
# Add them together to get...
a + b
<tf.Tensor: shape=(), dtype=int32, numpy=2>

#$ Once you've had a little taste of DataFrames, for example, an expression like the one below starts to look appealingly intuitive:

# Get the rows with population over 1m in South America
df[(df['population'] > 10**6) & (df['continent'] == 'South America')]

```

Calc the blackjack scores

```python
def hand_total(hand):
    """Helper function to calculate the total points of a blackjack hand.
    """
    total = 0
    # Count the number of aces and deal with how to apply them at the end.
    aces = 0
    for card in hand:
        if card in ['J', 'Q', 'K']:
            total += 10
        elif card == 'A':
            aces += 1
        else:
            # Convert number cards (e.g. '7') to ints
            total += int(card)
    # At this point, total is the sum of this hand's cards *not counting aces*.

    # Add aces, counting them as 1 for now. This is the smallest total we can make from this hand
    total += aces
    # "Upgrade" aces from 1 to 11 as long as it helps us get closer to 21
    # without busting
    while total + 10 <= 21 and aces > 0:
        # Upgrade an ace from 1 to 11
        total += 10
        aces -= 1
    return total
```


## English

### words
- grumble
  - complain about something in a bad-tempered way.

