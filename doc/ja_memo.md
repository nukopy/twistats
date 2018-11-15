# API reference index
[Twitter REST API 日本語版](http://westplain.sakuraweb.com/translate/twitter/Documentation/REST-APIs/Public-API/REST-APIs.cgi)

<!-- TOC depthFrom:1 depthTo:6 withLinks:1 updateOnSave:1 orderedList:0 -->

- [API reference index](#api-reference-index)
- [Basics](#basics)
	- [Authentication：認証関連](#authentication認証関連)
- [Accounts and users](#accounts-and-users)
	- [Create and manage lists](#create-and-manage-lists)
		- [Lists：リストとは？](#lists)
		- [API](#api)
	- [Follow, search, and get users](#follow-search-and-get-users)
		- [Following API](#following-api)
		- [Terminology：用語の注意 friendsとfollowers](#terminology用語注意-friendsfollowers)
		- [API](#api)
	- [Manage account settings and profile](#manage-account-settings-and-profile)
		- [overview](#overview)
		- [API](#api)
	- [Mute, block and report users](#mute-block-and-report-users)
		- [overview](#overview)
		- [API](#api)
	- [Subscribe to account activity](#subscribe-to-account-activity)
		- [API](#api)
		- [API](#api)
- [3. Tweets](#3-tweets)
	- [Curate a collection of Tweets](#curate-a-collection-of-tweets)
		- [Collections：Collectionとは？](#collectionscollection)
		- [API](#api)
	- [Filter realtime Tweets](#filter-realtime-tweets)
		- [API](#api)
		- [API](#api)
	- [Get Tweet timelines](#get-tweet-timelines)
		- [API](#api)
		- [API](#api)
	- [Get batch historical Tweets](#get-batch-historical-tweets)
		- [API](#api)
		- [API](#api)
	- [Post, retrieve and engage with Tweets](#post-retrieve-and-engage-with-tweets)
		- [API](#api)
		- [API](#api)
	- [Sample realtime Tweets](#sample-realtime-tweets)
		- [API](#api)
		- [API](#api)
	- [Search Tweets](#search-tweets)
		- [API](#api)
		- [API](#api)
	- [Tweet compliance](#tweet-compliance)
		- [API](#api)
		- [API](#api)
- [Direct Messages](#direct-messages)
	- [Buttons](#buttons)
	- [Custom profiles](#custom-profiles)
	- [Customer feedback cards](#customer-feedback-cards)
	- [Direct Messages](#direct-messages)
	- [Quick Replies](#quick-replies)
	- [Sending and receiving events](#sending-and-receiving-events)
	- [Typing indicator and read receipts](#typing-indicator-and-read-receipts)
	- [Welcome Messages](#welcome-messages)
- [Media](#media)
	- [Upload media](#upload-media)
- [Trends](#trends)
	- [Get locations with trending topics](#get-locations-with-trending-topics)
	- [Get trends near a location](#get-trends-near-a-location)
- [Geo](#geo)
	- [Get information about a place](#get-information-about-a-place)
	- [Get places near a location](#get-places-near-a-location)
- [Ads](#ads)
	- [Analytics](#analytics)
	- [Audiences](#audiences)
	- [Campaign Management](#campaign-management)
	- [Creatives](#creatives)
	- [Measurement](#measurement)
- [Metrics](#metrics)
	- [Get Tweet engagement](#get-tweet-engagement)

<!-- /TOC -->

# Basics
## Authentication：認証関連
* GET oauth/authenticate  
* GET oauth/authorize  
* POST oauth/access_token  
* POST oauth/invalidate_token  
* POST oauth/request_token  
* POST oauth2/invalidate_token  
* POST oauth2/token  


# Accounts and users
## Create and manage lists
### Lists：リストとは？
「リスト」は、ユーザーによって選ばれたTwitterアカウントのグループである。ユーザーは自身のリストを作成したり、他のユーザーが作成したリストを見ることができる。リストのタイムラインはリストに含まれるユーザーのツイートのみ表示される。
<!-- A list is a curated group of Twitter accounts. You can create your own lists or subscribe to lists created by others for the authenticated user. Viewing a list timeline will show you a stream of Tweets from only the accounts on that list. For general information on lists, see Using Twitter lists in the help center. -->

### API
* GET lists/list  
* GET lists/members  
* GET lists/members/show  
* GET lists/memberships  
* GET lists/ownerships  
* GET lists/show  
* GET lists/statuses  
* GET lists/subscribers  
* GET lists/subscribers/show  
* GET lists/subscriptions  
* POST lists/create  
* POST lists/destroy  
* POST lists/members/create  
* POST lists/members/create_all  
* POST lists/members/destroy  
* POST lists/members/destroy_all  
* POST lists/subscribers/create  
* POST lists/subscribers/destroy  
* POST lists/update  

## Follow, search, and get users
### Following API
Following APIにより、プログラムからユーザーのフォロー・検索を行うことができ、ユウーザーの情報を得ることができる。
<!-- The following API endpoints can be used to programmatically follow users, search for users, and get user information: -->
* Friends and followers(GETメソッド)  
    * GET followers/ids  
    * GET followers/list  
    * GET friends/ids  
    * GET friends/list  
    * GET friendships/incoming  
    * GET friendships/lookup  
    * GET friendships/no_retweets/ids  
    * GET friendships/outgoing  
    * GET friendships/show  

* POST friendships(POSTメソッド)  
    * POST friendships/create  
    * POST friendships/destroy  
    * POST friendships/update  

* Get user info(GETメソッド)  
    * GET users/lookup  
    * GET users/search  
    * GET users/show  
    * GET users/suggestions  
    * GET users/suggestions/:slug  
    * GET users/suggestions/:slug/members  

### Terminology：用語の注意 friendsとfollowers
用語の混乱を防ぐために、APIエンドポイントにおける`freiends`と`followers`の定義を下記に示す。
<!-- To avoid confusion around the term "friends" and "followers" with respect to the API endpoints, below is a definition of each: -->

* friends = フォロー  
`friends`は、ユーザーがフォローしているユーザーである。いわゆるフォロー/フォロワーのフォローのことである。つまり、`GET friends/ids`エンドポイントは、特定ユーザー（API使用者）のフォローのリスト（正確にはフォローのIDのリスト）を返す。
<!-- Friends - we refer to "friends" as the Twitter users that a specific user follows (e.g., following). Therefore, the GET friends/ids endpoint returns a collection of user IDs that the specified user follows. -->

* followers = フォロワー
`followers`は、ある特定のユーザーをフォローしているユーザーのことである。いわゆるフォロー/フォロワーのフォロワーのことである。つまり、`GET followers/ids`エンドポイントは、特定ユーザー（API使用者）のフォロワーのリスト（正確にはフォロワーのIDのリスト）を返す。
<!-- Followers - refers to the Twitter users that follow a specific user. Therefore, making a request to the GET followers/ids endpoint returns a collection of user IDs for every user following the specified user. -->

### API
* GET followers/ids  
* GET followers/list  
* GET friends/ids  
* GET friends/list  
* GET friendships/incoming  
* GET friendships/lookup  
* GET friendships/no_retweets/ids  
* GET friendships/outgoing  
* GET friendships/show  
* GET users/lookup  
* GET users/search  
* GET users/show  
* GET users/suggestions  
* GET users/suggestions/:slug  
* GET users/suggestions/:slug/members  
* POST friendships/create  
* POST friendships/destroy  
* POST friendships/update  

## Manage account settings and profile
### overview
適切な認証により、アプリケーションではユーザーのアカウント・プロフィールの設定の読み書きができる。全ての設定をAPIですることはできルわけではないことに注意。
<!-- With proper authorization your application can read and update a user's account and profile settings. Not all settings are exposed via the API. See the API reference for details. -->

### API
* GET account/settings  
* GET account/verify_credentials  
* GET saved_searches/list  
* GET saved_searches/show/:id  
* GET users/profile_banner  
* POST account/remove_profile_banner  
* POST account/settings  
* POST account/update_profile  
* POST account/update_profile_background_image (deprecated)  
* POST account/update_profile_banner  
* POST account/update_profile_image  
* POST saved_searches/create  
* POST saved_searches/destroy/:id  

## Mute, block and report users
### overview
API経由でブロックやミュートができる。
<!-- Your app can mute, block and report users for the authenicated user. For general information on reporting viloations on Twitter see How to report violations in the help center. -->

### API
* GET blocks/ids  
* GET blocks/list  
* GET mutes/users/ids  
* GET mutes/users/list  
* POST blocks/create  
* POST blocks/destroy  
* POST mutes/users/create  
* POST mutes/users/destroy  
* POST users/report_spam  

## Subscribe to account activity
### API
### API
* Enterprise Account Activity API  
* Premium Account Activity API  


# 3. Tweets
## Curate a collection of Tweets
### Collections：Collectionとは？
コレクションとは、編集可能なツイートのグループである。ユーザーが直接選んだツイートや、collection API経由でプログラムにより取得したツイートのグループである。コレクションは公開のもので、それぞれコレクション自身のWebページがある。簡単にWebサイトやアプリケーションに組み込むことができる。
<!-- A collection is an editable group of Tweets hand-selected by a Twitter user or programmatically managed via collection APIs. Each collection is public and has its own page on twitter.com, making it easy to share and embed in your website and apps. -->
* Create and edit a collection using TweetDeck  
TweetDeck supports adding Tweets to a collection by simply dragging a Tweet into a collection column.  
* View a collection on Twitter.com
Each collection has a public URL on Twitter.com. Share a collection with others by including it in a Tweet, email, or other share method.

Example: https://twitter.com/NYTNow/timelines/576828964162965504

* Embed a collection in your website or app
Embed a collection on your website using an HTML markup snippet generated by publish.twitter.com.

### API
* GET collections/entries  
* GET collections/list  
* GET collections/show  
* POST collections/create  
* POST collections/destroy  
* POST collections/entries/add  
* POST collections/entries/curate  
* POST collections/entries/move  
* POST collections/entries/remove  
* POST collections/update  

## Filter realtime Tweets
### API
### API
* PowerTrack API  
* PowerTrack Rules API  
* Replay API  
* POST statuses/filter  

## Get Tweet timelines
### API
### API
* GET statuses/home_timeline  
* GET statuses/mentions_timeline  
* GET statuses/user_timeline  

## Get batch historical Tweets
### API
### API
* Historical PowerTrack  

## Post, retrieve and engage with Tweets
### API
### API
* GET favorites/list  
* GET statuses/lookup  
* GET statuses/oembed  
* GET statuses/retweeters/ids  
* GET statuses/retweets/:id  
* GET statuses/retweets_of_me  
* GET statuses/show/:id  
* POST favorites/create  
* POST favorites/destroy  
* POST statuses/destroy/:id  
* POST statuses/retweet/:id  
* POST statuses/unretweet/:id  
* POST statuses/update  
* POST statuses/update_with_media (deprecated)  

## Sample realtime Tweets
### API
### API
* Decahose stream  
* GET statuses/sample  

## Search Tweets
### API
### API
* Enterprise search APIs  
* Premium search API  
* Standard search API  

## Tweet compliance
### API
### API
* GET compliance/firehose  


# Direct Messages
## Buttons
Buttons

## Custom profiles
DELETE custom_profiles/destroy.json
Send a Direct Message with custom profile
GET custom_profiles/:id
GET custom_profiles/list
POST custom_profiles/new.json

## Customer feedback cards
GET feedback/events.json
GET feedback/show/:id.json
POST feedback/create.json

## Direct Messages
API Reference
API Reference

## Quick Replies
Options Quick Reply

## Sending and receiving events
DELETE direct_messages/events/destroy
GET direct_messages/events/list
GET direct_messages/events/show
POST direct_messages/events/new (message_create)

## Typing indicator and read receipts
POST direct_messages/indicate_typing
POST direct_messages/mark_read

## Welcome Messages
DELETE direct_messages/welcome_messages/destroy
DELETE direct_messages/welcome_messages/rules/destroy
PUT direct_messages/welcome_messages/update
GET direct_messages/welcome_messages/list
GET direct_messages/welcome_messages/rules/list
GET direct_messages/welcome_messages/rules/show
GET direct_messages/welcome_messages/show
POST direct_messages/welcome_messages/new
POST direct_messages/welcome_messages/rules/new

# Media
## Upload media
GET media/upload (STATUS)
POST media/metadata/create
POST media/subtitles/create
POST media/subtitles/delete
POST media/upload
POST media/upload (APPEND)
POST media/upload (FINALIZE)
POST media/upload (INIT)


# Trends
## Get locations with trending topics
GET trends/available
GET trends/closest

## Get trends near a location
GET trends/place


# Geo
## Get information about a place
GET geo/id/:place_id

## Get places near a location
GET geo/reverse_geocode
GET geo/search


# Ads
## Analytics
Asynchronous Analytics
Auction Insights
Reach and Average Frequency
Synchronous Analytics

## Audiences
Audience API
Audience Intelligence
Global Opt Out
Insights
Keyword Insights
Real-Time Audience API
Tailored Audience Changes
Tailored Audience Permissions
Tailored Audiences

## Campaign Management
Accounts
Authenticated User Access
Bidding Rules
Campaigns
Content Categories
Features
Funding Instruments
IAB Categories
Line Item Apps
Line Item Placements
Line Items
Media Creatives
Promotable Users
Promoted Accounts
Promoted Tweets
Reach Estimate
Recommendations
Scheduled Promoted Tweets
Targeting Criteria
Targeting Options
Targeting Suggestions
Tax Settings
User Settings

## Creatives
Account Media
Cards Fetch
Draft Tweets
Image App Download Cards
Image Conversation Cards
Image Direct Message Cards
Media Library
Poll Cards
Preroll Call To Actions
Scheduled Tweets
Tweets
Video App Download Cards
Video Conversation Cards
Video Direct Message Cards
Video Website Cards
Website Cards

## Measurement
App Event Provider Configurations
App Event Tags
App Lists
Conversion Attribution
Conversion Event
Web Event Tags


# Metrics
## Get Tweet engagement
POST insights/engagement
