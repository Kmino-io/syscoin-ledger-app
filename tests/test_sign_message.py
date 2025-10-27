import pytest

from ledger_bitcoin.exception.errors import DenyError
from ledger_bitcoin.exception.device_exception import DeviceException
from ragger.navigator import Navigator
from ragger.firmware import Firmware
from ragger.error import ExceptionRAPDU
from ragger_bitcoin import RaggerClient
from .instructions import message_instruction_approve, message_instruction_approve_long, message_instruction_reject


def test_sign_message(navigator: Navigator, firmware: Firmware, client: RaggerClient, test_name: str):
    msg = "The Times 03/Jan/2009 Chancellor on brink of second bailout for banks."
    path = "m/44'/1'/0'/0/0"
    result = client.sign_message(msg, path, navigator,
                                 instructions=message_instruction_approve(firmware),
                                 testname=test_name)

    assert result == "IOBm68KnZfgm/1wH+NXhhxd/q9wlv3cGIqeDWDSBaUh4dmLh6jl2WM8z4EEonuiEE2ZIpGXGB4K9E81YMCxeLrQ="


def test_sign_message_64bytes(navigator: Navigator, firmware: Firmware, client: RaggerClient, test_name: str):
    # Version 2.2.2 introduced a bug where signing a 64 bytes message would fail; this test is to avoid regressions
    msg = "a" * 64
    path = "m/44'/1'/0'/0/0"
    client.sign_message(msg, path, navigator,
                        instructions=message_instruction_approve(firmware, save_screenshot=False),
                        testname=test_name)


def test_sign_message_accept(navigator: Navigator, firmware: Firmware, client: RaggerClient, test_name: str):
    message = "Hello world!"

    res = client.sign_message(
        message,
        "m/84'/1'/0'/0/0",
        navigator,
        instructions=message_instruction_approve(firmware),
        testname=test_name
    )

    assert res == 'H1XIhWCVbzW+wirwjJcaCFVDpkKgeQkBQf7fj8Kvp2LQGYbHfD4+eC8QLvJDa7QZrEJgiUaaOiV5GNWdLpt/Gig='


def test_sign_message_accept_long(navigator: Navigator, firmware: Firmware, client: RaggerClient, test_name: str):
    # Test with a long message that is split in multiple leaves in the Merkle tree
    message = "The root problem with conventional currency is all the trust that's required to make it work. The central bank must be trusted not to debase the currency, but the history of fiat currencies is full of breaches of that trust. Banks must be trusted to hold our money and transfer it electronically, but they lend it out in waves of credit bubbles with barely a fraction in reserve. We have to trust them with our privacy, trust them not to let identity thieves drain our accounts. Their massive overhead costs make micropayments impossible."

    res = client.sign_message(
        message,
        "m/84'/1'/0'/0/8",
        navigator,
        instructions=message_instruction_approve_long(firmware),
        testname=test_name
    )

    assert res == 'IE8NixU4TXDAqLwqq3hnw6vQN4gLr0S73CG1IfkYA3OKDDrzcTXStKgrXe5LpQn5JdpC0z1/YbYqoQxm0pMiklM='


def test_sign_message_reject(navigator: Navigator, firmware: Firmware, client: RaggerClient, test_name: str):
    with pytest.raises(ExceptionRAPDU) as e:
        client.sign_message("Anything", "m/44'/1'/0'/0/0",
                            navigator,
                            instructions=message_instruction_reject(firmware),
                            testname=test_name
                            )

    assert DeviceException.exc.get(e.value.status) == DenyError
    assert len(e.value.data) == 0


def test_sign_message_accept_non_ascii(navigator: Navigator, firmware: Firmware, client: RaggerClient, test_name: str):
    # Test with a message that contains non ascii char
    message = "Hello\nworld!"

    res = client.sign_message(
        message,
        "m/84'/1'/0'/0/8",
        navigator,
        instructions=message_instruction_approve(firmware),
        testname=test_name
    )

    assert res == 'ICC4xaqf21g/L40RC0r973k70Im3/KvS6Wx31j6vVwDiF0Od+tt3VF5kaPvpxveSzG3qNwzJmR4ZppA0Wy62iyk='


def test_sign_message_accept_too_long(navigator: Navigator, firmware: Firmware, client: RaggerClient, test_name: str):
    # Test with a message that is too long to be displayed
    message = "The root problem with conventional currency is all the trust that's required to make it work. The central bank must be trusted not to debase the currency, but the history of fiat currencies is full of breaches of that trust. Banks must be trusted to hold our money and transfer it electronically, but they lend it out in waves of credit bubbles with barely a fraction in reserve. We have to trust them with our privacy, trust them not to let identity thieves drain our accounts. Their massive overhead costs make micropayments impossible. The root problem with conventional currency is all the trust that's required to make it work. The central bank must be trusted not to debase the currency, but the history of fiat currencies is full of breaches of that trust. Banks must be trusted to hold our money and transfer it electronically, but they lend it out in waves of credit bubbles with barely a fraction in reserve. We have to trust them with our privacy, trust them not to let identity thieves drain our accounts. Their massive overhead costs make micropayments impossible. The root problem with conventional currency is all the trust that's required to make it work. The central bank must be trusted not to debase the currency, but the history of fiat currencies is full of breaches of that trust. Banks must be trusted to hold our money and transfer it electronically, but they lend it out in waves of credit bubbles with barely a fraction in reserve. We have to trust them with our privacy, trust them not to let identity thieves drain our accounts. Their massive overhead costs make micropayments impossible."

    res = client.sign_message(
        message,
        "m/84'/1'/0'/0/8",
        navigator,
        instructions=message_instruction_approve(firmware),
        testname=test_name
    )

    assert res == 'IJ6WzABGS1N+Ug1UP28YK+u9NbCmXPDZ/S1kF6FMLJ+Nc7YWC1GudI7xV9q52gF84T7UvvBIYBfYSF66hRkYqyE='


def test_sign_message_hash_reject(navigator: Navigator, firmware: Firmware, client: RaggerClient, test_name: str):
    with pytest.raises(ExceptionRAPDU) as e:
        client.sign_message("Hello\nworld!",
                            "m/44'/1'/0'/0/0",
                            navigator,
                            instructions=message_instruction_reject(firmware),
                            testname=test_name
                            )

    assert DeviceException.exc.get(e.value.status) == DenyError
    assert len(e.value.data) == 0
