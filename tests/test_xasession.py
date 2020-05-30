import pytest

from xing import Xing


@pytest.mark.parametrize("demo", [True, False], ids=["demo-server", "real-server"])
def test_login_success(demo, caplog):
    Xing.login()
    assert "login success" in caplog.text
    Xing.disconnect()


@pytest.mark.parametrize(
    "params",
    [{"id_": "WRONG"}, {"pw": "WRONG"}, {"cert_pw": "WRONG"}],
    ids=["invalid_id", "invalid_pw", "invalid_cert_pw"],
)
@pytest.mark.parametrize("demo", [True, False], ids=["demo-server", "real-server"])
def test_login_fail(params, demo, caplog):
    Xing.login(**params, demo=demo)
    if not (demo is True and "cert_pw" in params):
        assert "login fail" in caplog.text
    # avoid invalidation of certificate
    Xing.disconnect()
    Xing.login()
    Xing.disconnect()


@pytest.mark.parametrize(
    "params", [{"id_": "WRONG"}, {}], ids=["invalid_account", "valid_acconut"]
)
@pytest.mark.parametrize("demo", [True, False], ids=["demo-server", "real-server"])
def test_get_account_sanity_checks(params, demo):
    Xing.login(demo=demo)
    account_count = Xing.get_account_count()
    assert account_count > 0
    for i in range(account_count):
        account_number = Xing.get_account(i)
        Xing.get_account_name(account_number)
        Xing.get_account_detail_name(account_number)
        Xing.get_account_nickname(account_number)
    Xing.disconnect()
