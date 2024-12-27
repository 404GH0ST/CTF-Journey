# Solution

The secret is based on the md5sum of the current UTC time when the app is deployed.
I have create a secret to generate a valid cookie.

The website uses Yamale 3.0.8 which is an old version. There is an RCE vulnerability affecting Yamale before 4.0.0 [Github Issue + PoC](https://github.com/23andMe/Yamale/issues/167).

Just create a schema with reverse shell code in the name content and validate an object based on the schema to trigger the RCE.
