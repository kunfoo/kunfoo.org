# Python

## Builtins
- breakpoint()
    - put it anywhere in your code and start debugging

### functions
- bin(num)
- chr(num)
- dir(object)
- hex(num)
- len(obj)
- ord(char)
- sorted(iterable)

## Strings
```
"""multi
line
string"""
```
```
"multi\
 line\
 string"
```
```
a = "strings" "are" "automatically" "concatenated"
```
```
r"raw\nstring"
> 'raw\\nstring'
b"byte string \x3a\x2d\x29"
> b'byte string :-)'
u"unicode string \xe4\xf6\xfc\xdf"
> 'unicode string äöüß'
```

### format()
```
"{0} and {1}".format("apples", "bananas")
```
```
from math import pi
"pi is {:.3f}".format(pi)
> 'pi is 3.142'
```
```
"{0:_^11}".format("hello")
> '___hello___'
```
```
a = "apples"
b = "bananas"
f"{a} and {b}"
```

## Code Samples

### Make an http request
```python
import requests

url = "http://example.com:80/some/path.php"
params = {"p1":"value1", "p2":"value2"}
headers = {"User-Agent": "fake User Agent", "Fake header": "True value"}
cookies = {"PHPSESSID": "1234567890abcdef", "FakeCookie123": "456"}
proxies = {'http':'http://127.0.0.1:8080','https':'http://127.0.0.1:8080'}

#Regular Get requests sending parameters (params)
gr = requests.get(url, params=params, headers=headers, cookies=cookies, verify=False, allow_redirects=True)

code = gr.status_code
ret_headers = gr.headers
body_byte = gr.content
body_text = gr.text
ret_cookies = gr.cookies.items()
is_redirect = gr.is_redirect
is_permanent_redirect = gr.is_permanent_redirect
float_seconds = gr.elapsed.total_seconds() 10.231

#Regular Post requests sending parameters (data)
pr = requests.post(url, data=params, headers=headers, cookies=cookies, verify=False, allow_redirects=True, proxies=proxies)

#Json Post requests sending parameters(json)
pr = requests.post(url, json=params, headers=headers, cookies=cookies, verify=False, allow_redirects=True, proxies=proxies)

#Post request sending a file(files) and extra values
filedict = {"<FILE_PARAMETER_NAME>" : ("filename.png", open("filename.png", 'rb').read(), "image/png")}
pr = requests.post(url, data={"submit": "submit"}, files=filedict)
```
Shamelessly stolen from <https://book.hacktricks.xyz/misc/basic-python/web-requests>.
