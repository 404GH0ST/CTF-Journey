# Solver
The website use memcached combined with Flask-session to handle cookie. There are no functionalities that potentially vulnerable other than the cookie in the website.

There's an article that shows how to exploit memcached with Flask-session [Memcached Command Injections at Pylibmc](https://btlfry.gitlab.io/notes/posts/memcached-command-injections-at-pylibmc/) to gain RCE.

We could follow along the article, and modify the system command. The cookie length if it's greater than 86 characters, it will be truncated to 86 characters.
But `cat /flag* >> /app/application/templates/index.html` is still triggered successfully and flag will be embedded in the webpage.
