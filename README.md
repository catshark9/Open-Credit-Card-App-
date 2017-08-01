# App for Credit Card Churners
Find app hosted [here](credit-cards.98he2uhpu4.us-east-2.elasticbeanstalk.com)

This app collects data daily via web scrapers developed in R. 
The are then placed in a DynamoDB collection. 

A list of all cards can be retrieved in JSON format at http://credit-cards.98he2uhpu4.us-east-2.elasticbeanstalk.com/CurrentCards/CurrentValue.
The cards are ranked by their calculated dollar value. I used the conversion rates provided by thepointsguy.com monthly valuations. 

### Headers/Variables Collected
* Program
* CardName
* Issuer
* Link
* IntroOffer
* Cash
* Points
* Nights
* Credit
* FeeWaived1stYr
* Fee
* Spend
* img
* Rate
* business
* Value
* Date

### Assumptions

The formula for Value is:

(Points) x (Rate) + Cash + StatementCredit + (150) x (Number of Free Nights) - AF x {0 if waived first year, 1 if not}

* Points is the introductory points/miles rewards
* The rate is what [thepointsguy.com would pay for miles or points from a given reward program.](https://thepointsguy.com/2017/07/july-2017-monthly-valuations/)  For the ones he did not specify, I gave a rate of .01 per point. 
* Cash is the introductory cash rewards
* Number of nights is how many nights are given as introductory bonus
* I multiplied nights by 150 because that is typically what I would try and pay for a night. 
* If the fee is waived the first year, I didn't subtract it. If it is paid immediately, I subtracted it. I did not take into account that you might lose your points if you cancel before the second year. I based this off gaining your rewards and then closing your account before anniversary.

So for example Club Carlson:

* Points: 85,000
* Rate: .04
* Fee: 75, not waived
* Current Value = 85000(.04) - 75 = 265

### Changes Wanted
I want to enhance the front-end by using async filters in angular. I am open to any other suggestions as well!
