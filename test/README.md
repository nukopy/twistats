## Agent.make_params(self, query, count)
Agent.make_params() returns params that is used HTTP request to Twitter REST API. 
Query is used when you do HTTP-requests. Count is a number of tweets.

___

### query that you are likely to use
query : description
___

#### word search
* word1 word2 : tweets that contain BOTH word1 and word2  
* word1 OR word2 : tweets that contain EITHER word1 or word2  
* word1 -word2 : contain word1 except word2  
* /*#word : hash-tag of word/*

#### word and time search
* word since:20XX-MM-DD : tweets after the time ex) word since:2015-02-23  
* word until:20XX-MM-DD : tweets before the time ex) word until:2015-02-23  

#### contents search
* word :) : tweets that contain word and positive contents  
* word :( : tweets that contain word and negative contents  
* word ? : tweets that contain word and question form

___

#### specific user search
* from:user : user's tweets
* to:user : tweets to user's (contain reply)
* @user : reply to user
___

#### about retweet
include:retweets : tweets that were retweet
exclude:retweets : tweets that were NOT retweet
___

#### filter
* word filter:links : contain word and links
* word filter:verified : contain word and were tweeted from verified-account
* word filter:images : contain word and images
* word filter:twimg : contain word and twi-images
* word filter:videos : contain word and videos
* word filter:media : contain word and media(images and videos)
* word filter:vine : contain word and vine
* word filter:news : contain word and were likely to be news
* word filter:safe : contain word and possibly_sensitive flag was 0(NOT adulty)
* word filter:periscope : contain word and broadcasted by periscope
* word filter:native_video : contain word and videos(periscope,vine and Twitter)
___

#### place
* word geocode:latitude,longitude,1km : tweets that contain word and were tweeted from place (unit: km, mi etc..)  
ex) cat geocode:37.78115,-122.39872,1mi (latitude:-90~90, longitude:-180)緯度：横線、経度：縦線
* word near:me : contain word and were tweeted near me
* word near:place - contain word and were tweeted near place  
ex) 猫 near:新潟
* word near:place within:10km - contain word and were tweeted within 10km from the location(unit: km, mi etc..)
___

#### retweets-faves number
* word min_retweets:number : contain word and were retweeted 100-or-more
* word min_faves:number : contain word and were "favorited" 100-or-more
* word min_replies:number : contain word and were replied 5-or-more
___

#### others
* word source:flantter : tweets that contain word and tweeted from flantter
* word lang:ja : contain word and language is Japanese(others ex) en)
* word list:user/listname :
* word card_name:animated_gif - contain word and GIF
___

### Example
* word filter:media exclude:retweets  
contain word and media(images and videos) and excluded retweets

* from:user filter:images min_faves:100  
user's tweet that contain images favorited by 100-or-more

* word filter:images min_faves:100 exclude:retweets  
contain word and images favorited by 100-or-more and excluded retweets

* word filter:images -filter:safe  
contain word and possibly_sensitive-flag is one(perhaps R-18)
