## Asserts & Testing

One of the best advantages we can give ourselves when programming, is to share and reuse code as much as possible; that way, instead of solving old problems over and over, we can spend more time doing new science and less time reinventing old wheels. But, how can we be sure that a piece of code is working correctly, and being used the way it was intended? Asserts and testing help us check the quality of our code quickly and easily, leading to less bugs and more reliable programs.

For these examples, we're going to use a toy example from genomics. Consider: how well do the genomes `AC-G-` and `AC-AT` match? Let's define a simple scoring algorithm: compare the bases in the two genomes pair by pair; for every match, award 1 point; for every mismatch, subtract a point; and if one or both of the bases are `-` (representing a missing base), award 0 points. So, the example above would have a score of 1:

```
A A : +1
C C : +1
- - : +0
G A : -1
- T : +0
```

The function `matchScore` in the `genomics.matching` package is an attempt to implement this algorithm; maybe you wrote it yourself, or maybe you got it from someone else. In any case, let's try it out:

`myScript.py`:
```
import genomics.matching as matching

print matching.matchScore('AAA', 'AAA')
```

Which prints `3` - great! Seems to work as it should. But, what about:

`myScript.py`:
```
import genomics.matching as matching

# print matching.matchScore('AAA', 'AAA')

print matching.matchScore([True, {}, 7], [True, {}, 7])
```

A perfect match! But this is *nonsense* - `[True, {}, 7]` is not a meaningful genome - if this is what's getting plugged into our function, something has gone wrong. But, even though we're putting garbage in, we happen to get a completely unremarkable answer out - so in a bigger program, things would just keep going along, and we might never realize that nonsense was happening in the middle.

In order to avoid absurd circumstances like these (which happen more often than you'd think), Python has things called asserts; they check that a certain condition is True, and if it isn't they cause the program to halt immediately and report what went wrong. Example:

`genomics/matching.py`:
```
  def matchScore(seqA, seqB):

    assert type(seqA) == str, 'First genome is not a string.'
    assert type(seqB) == str, 'Second genome is not a string.'

    ...
```

The asserts check that the sequences are actually strings, like we'd expect, before allowing execution to continue; if the condition is False, execution halts and the sentence at the end of the assert is reported.

If we re-run `myScript.py` now, we get:

```
Traceback (most recent call last):
  File "myScript.py", line 5, in <module>
    print matching.matchScore([True, {}, 7], [True, {}, 7])
  File "/Users/bill/Desktop/python-testing-master/genomics/matching.py", line 3, in matchScore
    assert type(seqA) == str, 'First genome was not a string'
AssertionError: First genome is not a string.
```

The assert has let Python catch the nonsense and let us know about it, rather than just happily pressing onwards. In general, asserts are tools to ensure our *assumptions have been respected*; every time you can make an assumption about the state of a function, put in an assert to make sure things are as you expect.

### Problem 1

> Add another `assert` to `matchScore` to check that the inputs make sense. Remember that the first step is always to think about what assumptions you expect to be True.


Finally, we need a way to easily check if the functions actually work properly. To do this, we need to write tests. Let's start by re-writing the very first thing we did, when we checked that `AAA` and `AAA` matched for 3 points, but this time, as an automated test:

`tests/matching_tests.py`
```
import genomics.matching as matching

def test_matchScore_spotcheck():
    '''
    matchScore('AAA', 'AAA') should return 3.
    '''

    score = matching.matchScore('AAA', 'AAA')

    assert score == 3, 'AAA and AAA should have matched for 3 points, but instead we got %i' % score
```

All test names should begin with `test_`, and the function itself should contain an assert statement that checks one piece of *behavior* of our function; we should have a test that examines every piece of behavior we can describe.

Run the test by going into the root directory of the project and doing `nosetests tests/*.py`. Our test makes sure that a simple example of counting matches is working correctly in `matchScore`. This one passes with no problems, as we expected:

```
.
----------------------------------------------------------------------
Ran 1 test in 0.000s

OK
```

Also note that in future, even if we change `matchScore` to another implementation, we can still run the tests to make sure we haven't broken anything - this is another key feature of testing: it allows us to quickly and automatically make sure we haven't broken stuff as we work.

### Problem 2

> Add a test to `tests/matching_tests.py` that checks that the correct answer is found when comparing `AC-G-` and `AC-AT`.

The last problem is an example of another reason why writing tests is so crucial - they help us spot our mistakes! If our answer to problem 2 was something like:

`tests/matching_tests.py`

```
...
def test_matchScore_another_spotcheck():
    '''
    matchScore('AC-G-', 'AC-AT') should return 1.
    '''

    score = matching.matchScore('AC-G-', 'AC-AT')

    assert score == 1, 'AC-G- and AC-AT should have matched for 1 point, but instead we got %i' % score
```

When we run the test suite now, we get:

```
.F
======================================================================
FAIL: matchScore('AC-G-', 'AC-AT') should return 1.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "//anaconda/lib/python2.7/site-packages/nose/case.py", line 197, in runTest
    self.test(*self.arg)
  File "/Users/bill/Desktop/projects/python-testing/tests/tests.py", line 19, in test_matchScore_another_spotcheck
    assert score == 1, 'AC-G- and AC-AT should have matched for 1 point, but instead we got %i' % score
AssertionError: AC-G- and AC-AT should have matched for 1 point, but instead we got 2

----------------------------------------------------------------------
Ran 2 tests in 0.001s

FAILED (failures=1)
```

Something isn't right with the implementation of `matchScore`. More immediately than worrying about future bugs or reusing code, testing lets us validate our code in a concrete, reproducible way, and ensure that it actually does what we think it does.

But so now - we need to fix our function so it passes the tests! The first test we wrote checked to make sure the correct matches were working - but what about mismatches? Let's add another test:

`tests/matching_tests.py`
```
...

def test_matchScore_spotcheck_penalties():
    '''
    check that penalties are counted correctly
    '''

    score = matching.matchScore('AAA', 'GGG')

    assert score == -3, 'AAA and GGG should have matched for -3 points, but instead we got %i' % score
```

If we run this, this latest test passes - apparently we're counting mismatches correctly. There's only one thing left to check:

`tests/matching_tests.py`
```
...

def test_matchScore_spotcheck_gaps():
    '''
    check that gaps are counted correctly
    '''

    score = matching.matchScore('---', '---')

    assert score == 0, '--- and --- should have matched for 0 points, but instead we got %i' % score
```

Now if we run this, this latest test fails, too! 

```
.F.F
======================================================================
FAIL: matchScore('AC-G-', 'AC-AT') should return 1.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "//anaconda/lib/python2.7/site-packages/nose/case.py", line 197, in runTest
    self.test(*self.arg)
  File "/Users/bill/Desktop/projects/python-testing/tests/tests.py", line 19, in test_matchScore_another_spotcheck
    assert score == 1, 'AC-G- and AC-AT should have matched for 1 point, but instead we got %i' % score
AssertionError: AC-G- and AC-AT should have matched for 1 point, but instead we got 2

======================================================================
FAIL: check that gaps are counted correctly
----------------------------------------------------------------------
Traceback (most recent call last):
  File "//anaconda/lib/python2.7/site-packages/nose/case.py", line 197, in runTest
    self.test(*self.arg)
  File "/Users/bill/Desktop/projects/python-testing/tests/tests.py", line 37, in test_matchScore_spotcheck_gaps
    assert score == 0, '--- and --- should have matched for 0 points, but instead we got %i' % score
AssertionError: --- and --- should have matched for 0 points, but instead we got 3

----------------------------------------------------------------------
Ran 4 tests in 0.001s

FAILED (failures=2)
```

Our implementation isn't counting gaps correctly. How can we fix this? Here's one way:

`genomics/matching.py`
```
def matchScore(seqA, seqB):

  score = 0

  for i in range(len(seqA)):

    if (seqA[i] == seqB[i]) and (seqA[i] != '-'):
      score += 1
    elif seqA[i] == '-' or seqB[i] == '-':
      score += 0
    elif seqA[i] != seqB[i]:
      score -= 1

  return score
```

Now if we run our test suite again, everything passes!

```
....
----------------------------------------------------------------------
Ran 4 tests in 0.001s

OK
```

By coding up our checks in reusable, automated tests, we can rerun them quickly and easily; instead of wondering and guessing if our functions are correct, we can just run the tests. Also, later, if we change our code, we can run the tests again to make sure we didn't break anything. For example, I could change `matchScore` like this:

`genomics/matching.py`
```
def matchScore(seqA, seqB):

  score = 0

  for i in range(len(seqA)):

    if seqA[i] == '-' or seqB[i] == '-':
      score += 0
    elif seqA[i] == seqB[i]:
      score += 1
    elif seqA[i] != seqB[i]:
      score -= 1

  return score
``` 

Without a test suite, I would have to sit and examine these changes carefully, and wonder if I got it right or not; instead, I can run my test suite again and in 0.001 seconds, I know with certainty that I haven't broken anything. In this way, writing tests dramatically lowers the cost of double checking our work - and work that is regularly double-checked will have less bugs and be more reliable.

### Bonus Round

### Bonus Round Problem 1

> In genomics, we often want the 'reverse complement' of a genome; to construct this, take a genome and do the following:
> - reverse the order of the characters
> - swap A for T, and G for C.
>
> So for example, ACCG becomes CGGT.
> Imagine the `matching.py` module contained a function called `reverseComplement`. This function should at least be able to get the above example right. Write a test in `matching_tests.py` that checks for this behavior; don't bother actually writing the `reverseComplement` function.

What you just did is an example of **test driven design** - writing down what we want our function to do by defining the tests that check that that's the case *first*. TDD has the great advantage of helping us fight confirmation bias when coding; if you write a function first, there's a great temptation to run it once, see that it superficially looks okay, and call it done. Having the tests in place forces you to check that all the expected behavior actually works.

### Bonus Round Problem 2

> Write the `reverseComplement` function, and make sure it passes the test you wrote in the last problem.
