from pyqiwip2p import QiwiP2P
from pyqiwip2p.types import QiwiCustomer, QiwiDatetime
from Qiwikey import QIWI_PRIV_KEY
from db import getBillid, newBill, setRejectedStatus


def check_bill(chatid):
    p2p = QiwiP2P(auth_key=QIWI_PRIV_KEY)
    bill_data = getBillid(chatid)
    status = p2p.check(bill_id=bill_data).status
    print(status)
    if status == 'PAYED':
        return True
    else:
        return False


def QiwiPay(chatid, samount, parseAmount):
    p2p = QiwiP2P(auth_key=QIWI_PRIV_KEY)
    new_bill = p2p.bill(amount=samount, comment="avParser bill", lifetime=15)
    href = new_bill.pay_url
    bill_data = new_bill.bill_id
    newBill(bill_data, chatid, parseAmount)
    return href


def kill_bill(chatid):
    p2p = QiwiP2P(auth_key=QIWI_PRIV_KEY)
    bill_data = getBillid(chatid)
    setRejectedStatus(bill_data)
    p2p.reject(bill_id=bill_data)
