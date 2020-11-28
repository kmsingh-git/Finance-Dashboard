# Finance-Dashboard

I was teaching myself Dash Plotly, as well as some finance, and CSS.
This dashboard represents a milestone in that journey. Feel free to copy the code.

<p> The link for the website is https://finance-dashboard-kms.herokuapp.com/

# Bonus - Simulating Dice Rolls

If you play around with the Simulating Dice Rolls Tab, you can see both the Central Limit Theorem and the Weak Law of Large Numbers at work:
- [CPT]: If you increase the number of dice to say 20, since you're plotting the distribution of the SUM of these dice (which are iid discrete random variables), their histogram looks like a bell curve (A nice visual proof of CPT that states the sum of 20 iid random variables will approximately follow the Normal distribution - technically you need at least 30 but for many common distributions such as this one, you see an approximation to Normal distribution sooner)
- [Weak Law of Large Numbers]: If you keep the number of dice to 2 (works at higher dice too but hard to see), and increase the number of rolls to say 5000, you'll see that the histogram approaches the mean of the VECTOR random variable that's 1-hot encoded for the sum of 2 dice.
  - [Verbose]: In other words, imagine a random variable that is an 11 element vector. The specialty of this random variable is that exactly one elment will be 1 and the rest have to be 0. To connect this to the 2 dice roll, say the first element corresponds a 2 rolling on the 2 dice sum, the second element corresponds to a 3 rolling on the 2 dice sum, and so on until the eleventh element, which corresponds to 12 rolling on the 2 dice sum. From high school math, we can come up with the Probability of each of these values occuring. For example, P(first element is 1 aka 2 occurs on the dice) = 1/36. P(second element is 1 aka 3 occurs on the dice) = 2/36. Similarly P(eleventh element is 1 aka 12 occurs on the dice) = 1/36. Also, the Expected value of this random variable is simply a vector of eleven elements such that the i^th element is the Probability that the i^th element is 1. If you visualize this Expected value on a graph, you will see it has a nice pyramid like structure. By rolling the 2 dice 5000 times say, and dividing the counts vector by 5000 (which I didn't do in the graph but that's just a scaling term that will not affect the shape of the graph), you can observe that the graph has the same pyramid shape and in fact the corresponding elements (count of ith term/5000) is very close to the corresponding probability.
