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

### Changes Wanted
I want to enhance the front-end by using async filters in angular. I am open to any other suggestions as well!
