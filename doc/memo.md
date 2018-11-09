#GET friends/list
https://developer.twitter.com/en/docs/basics/cursoring
### cursoring
大きな結果をページ番号をつける、カーサリングという技術を使用している。
これにより、GETメソッドのレスポンスの結果を前後に動ける手段を提供している。

cursor はページを行き来するための手段。
### time 1
cursor -1 
return 

cursorパラメータのデフォルト値は -1。
cursorのパラメータが定められたHTTPリクエストのレスポンスは、
以下を含む。 
* previous_cursor
* next_cursor
* previous_cursor_str
* next_cursor_str.

TwitterAPIにおける大抵のIDの値がそうであるように
、"_str"の値 は、大きな整数値をサポートしていない(e.g. JavaSript)
言語のために提供されている。

[In]
# convert json-string to python-dictionary
dic = json.loads(response.text)
dic.keys
[Out]
['ids', 'next_cursor', 'next_cursor_str', 'previous_cursor', 'previous_cursor_str']

着目すべきは next_cursor と previous_cursor の値 