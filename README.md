# Birr - Simple URL shortening using WSGI

Birr, would be the sound of a URL redirection if one could hear it. :)

## Requirements

Python 2.7 and a
[WSGI](https://en.wikipedia.org/wiki/Web_Server_Gateway_Interface) capable
server will be needed to use Birr. But since it is a very simple code I would
think it can be easily ported to another server.

## Workings

Birr reads a configuration file, default name `shorturls.cfg`, and matches with
the query path, if the query path is found Birr will reply with a `303 See
Other` and redirects the browser. If not found, a `404 Not Found` with empty
body is issued.

The configuration file is defined as:

```
# This is a comment and will be ignored

shortA redirectionForShortA
shortB shortC redirectionForShortBandC
shortD shortE shortF redirectionForShortDandEandF

``` 

Each word is a short url for the last word in the configuration file. This
allows for multiple short urls to point to the same place. At least two words,
a shortcut and a target, need to be defined for a shortcut to work. Comments,
empty lines and lines with few than 2 words will be ignored.
 
 
## Technical Details
 
Bellow is the expected requests and responses in terms of HTTP from Birr. The
file `passenger_wsgi.py` handles the HTTP queries and redirection while
`parse_config.py` does the configuration parsing. The configuration parsing is
the equivalent of creating a dict in python where the keys point to the
redirection value. Like so:

```
# For a config like:
shortA shortB redirection

# It will be the same as:
# shortcuts = { 'shortA': 'redirection', 'shortB': 'redirection' }
```

It is possible to test Birr using the command line and check its behavior:

```
python -c 'import passenger_wsgi as p; import sys; p.application({"PATH_INFO": "/test"}, lambda x, y: sys.stdout.write(x + str(y) + "\n" ))'
```

* shortcut `/shortA` is found:

```
GET /shortA HTTP/1.1
Accept: */*
Accept-Encoding: gzip, deflate
Connection: keep-alive
Host: testhost
User-Agent: HTTPie/1.0.3


HTTP/1.1 303 See Other
Connection: Keep-Alive
Date: Wed, 27 Nov 2019 17:10:18 GMT
Keep-Alive: timeout=2, max=100
Location: redirectionForShortA
Server: Apache
Status: 303 See Other
Transfer-Encoding: chunked
Upgrade: h2
```

* shortcut `/notexistent` is not found:

```
GET /notexistent HTTP/1.1
Accept: */*
Accept-Encoding: gzip, deflate
Connection: keep-alive
Host: testhost
User-Agent: HTTPie/1.0.3


HTTP/1.1 404 Not Found
Connection: Keep-Alive
Content-Length: 0
Content-Type: text/plain
Date: Wed, 27 Nov 2019 17:12:51 GMT
Keep-Alive: timeout=2, max=100
Server: Apache
Status: 404 Not Found
Upgrade: h2
```
