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

## Getting help message for t0424
```
# or if you pass the as_json=True you'll get json format of t0424 res file 
print(Xing.help('t0424'))
```
```
주식잔고2(t0424)
t0424InBlock 기본입력 input
	accno 계좌번호 <class 'str'> 11
	passwd 비밀번호 <class 'str'> 8
	prcgb 단가구분 <class 'str'> 1
	chegb 체결구분 <class 'str'> 1
	dangb 단일가구분 <class 'str'> 1
	charge 제비용포함여부 <class 'str'> 1
	cts_expcode CTS_종목번호 <class 'str'> 22
t0424OutBlock 출력 output
	sunamt 추정순자산 <class 'int'> 18
	dtsunik 실현손익 <class 'int'> 18
	mamt 매입금액 <class 'int'> 18
	sunamt1 추정D2예수금 <class 'int'> 18
	cts_expcode CTS_종목번호 <class 'str'> 22
	tappamt 평가금액 <class 'int'> 18
	tdtsunik 평가손익 <class 'int'> 18
t0424OutBlock1 출력1 output occurs
	expcode 종목번호 <class 'str'> 12
	jangb 잔고구분 <class 'str'> 10
	janqty 잔고수량 <class 'int'> 18
	mdposqt 매도가능수량 <class 'int'> 18
	pamt 평균단가 <class 'int'> 18
	mamt 매입금액 <class 'int'> 18
	sinamt 대출금액 <class 'int'> 18
	lastdt 만기일자 <class 'str'> 8
	msat 당일매수금액 <class 'int'> 18
	mpms 당일매수단가 <class 'int'> 18
	mdat 당일매도금액 <class 'int'> 18
	mpmd 당일매도단가 <class 'int'> 18
	jsat 전일매수금액 <class 'int'> 18
	jpms 전일매수단가 <class 'int'> 18
	jdat 전일매도금액 <class 'int'> 18
	jpmd 전일매도단가 <class 'int'> 18
	sysprocseq 처리순번 <class 'int'> 10
	loandt 대출일자 <class 'str'> 8
	hname 종목명 <class 'str'> 20
	marketgb 시장구분 <class 'str'> 1
	jonggb 종목구분 <class 'str'> 1
	janrt 보유비중 <class 'float'> 10.2
	price 현재가 <class 'int'> 8
	appamt 평가금액 <class 'int'> 18
	dtsunik 평가손익 <class 'int'> 18
	sunikrt 수익율 <class 'float'> 10.2
	fee 수수료 <class 'int'> 10
	tax 제세금 <class 'int'> 10
	sininter 신용이자 <class 'int'> 10
```