# xingapi_python
xingapi_pyton(hereinafter referred to as just xing) is xingapi wrapper of python version.
it's an api provided by eBest security.
I just implemented this just for fun and I'm not
responsible for any risk from using this.

# installation
## pip
`pip install -r requirements.txt`
## poetry
`poetry install`

# How to use
All you need is in the Xing object.
It's a singleton, so you don't need to
intantiate it. let's start from login

## Login to eBest security server
```python
from xing import Xing

# when Xing attempts login, it finds .secrets.json from {workingdir/.secrets.json}
# .secrets.json should have keys ID, PW, DEMO_PW, CERT_PW. if it can't find secret file, then
# it finds environment variables XING_ID, XING_PW, XING_DEMO_PW, XING_CERT_PW
Xing.login(demo=True)
```
```
05-31 19:07    xingapi.xing    INFO        connection check
05-31 19:07    xingapi.xing    WARNING     not yet connected
05-31 19:07    xingapi.xing    INFO        connect attempt: demo.ebestsec.co.kr:20001
05-31 19:07    xingapi.xing    INFO        login attempt
05-31 19:07    xingapi.com.XASession    INFO        login success
```

## Getting account information
```python
for i in range(Xing.get_account_count()):
    account_number = Xing.get_account(i)
    print(f'account_number: {account_number}')
    print(f'account_name: {Xing.get_account_name(account_number)}')
    print(f'account_detail_name: {Xing.get_account_detail_name(account_number)}')
    print(f'account_nickname: {Xing.get_account_nickname(account_number)}')
```
```
account_number: ****
account_name: ****
account_detail_name: 위탁
account_nickname: ****
```

## Using t8430 res
```python
Xing.request('t8430', {'gubun': '1'})
Xing.get('t8430', ['hname', 'shcode', 'expcode', 'etfgubun'], n=5)
```
```
	hname		shcode	expcode	        etfgubun
0	동화약품		000020	KR7000020008	0
1	KR모터스		000040	KR7000040006	0
2	경방		000050	KR7000050005	0
3	메리츠화재	000060	KR7000060004	0
4	삼양홀딩스	000070	KR7000070003	0
```