# Solver
The HA Proxy deny rule isn't great enough, we can generate a JSON web token by visiting `//api/v1/get_ticket`.
Looking at the `requirements.txt`, the `python-jwt` version is `3.3.3` which is still vulnerable to [CVE-2022-39227](https://github.com/advisories/GHSA-5p8v-58qm-c7fp).
We can use this [PoC](https://github.com/user0x1337/CVE-2022-39227) to generate new JSON token with role as administrator

```python
python3 cve_2022_39227.py -j <JWT-WEBTOKEN> -i "role=administrator"
```

Use the JSON token to get the flag

```bash
curl http://server:port/api/v1/flag -H "Authorizaton: <NEW_TOKEN>"
```
