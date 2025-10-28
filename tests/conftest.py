
import os

from ragger_bitcoin import createRaggerClient, RaggerClient
from ragger.backend import RaisePolicy
from ragger.backend.interface import BackendInterface
from ragger.conftest import configuration
import ledger_bitcoin._base58 as base58
from ledger_bitcoin.common import sha256
from ledger_bitcoin import Chain
from pathlib import Path
from test_utils import segwit_addr
from test_utils.fixtures import *
from typing import List
import random


###########################
### CONFIGURATION START ###
###########################

# You can configure optional parameters by overriding the value of ragger.configuration.OPTIONAL_CONFIGURATION
# Please refer to ragger/conftest/configuration.py for their descriptions and accepted values

MNEMONIC = "glory promote mansion idle axis finger extra february uncover one trip resource lawn turtle enact monster seven myth punch hobby comfort wild raise skin"
configuration.OPTIONAL.CUSTOM_SEED = MNEMONIC
configuration.OPTIONAL.BACKEND_SCOPE = "function"


@pytest.fixture
def additional_speculos_arguments(request) -> List[str]:
    # if the --speculos_port argument is given, instruct ragger to use the given port
    # instead of using a dynamically allocated port
    speculos_port = request.config.getoption("--speculos_port")
    if speculos_port is None:
        return []
    else:
        return ["--api-port", str(speculos_port)]

#########################
### CONFIGURATION END ###
#########################
TESTS_ROOT_DIR = Path(__file__).parent

# Pull all features from the base ragger conftest using the overridden configuration
pytest_plugins = ("ragger.conftest.base_conftest", )

random.seed(0)  # make sure tests are repeatable

# Make sure that the native client library is used with, as speculos would otherwise
# return a version number < 2.0.0 for the app
os.environ['SPECULOS_APPNAME'] = f'Syscoin Test:{get_app_version()}'



# Node-backed RPC fixtures and helpers removed; test suite is node-free


def seed_to_wif(seed: bytes):
    assert len(seed) == 32

    double_sha256 = sha256(sha256(b"\x80" + seed))
    return base58.encode(b"\x80" + seed + double_sha256[:4])


wallet_count = 0


def testnet_to_regtest_addr(addr: str) -> str:
    """Convenience function to reencode addresses from testnet format to regtest one (bech32 prefix is different)"""
    hrp, data, spec = segwit_addr.bech32_decode(addr)
    if hrp is None:
        return addr  # bech32m decoding failed; either legacy/unknown address type, or invalid address
    if (hrp != "tsys"):
        raise ValueError("Not a valid testnet bech32m string")
    return segwit_addr.bech32_encode("bcrt", data, spec)


@pytest.fixture
def client(bitcoin_network: str, backend: BackendInterface) -> RaggerClient:
    if bitcoin_network == "main":
        chain = Chain.MAIN
    elif bitcoin_network == "test":
        chain = Chain.TEST
    else:
        raise ValueError(
            f'Invalid value for BITCOIN_NETWORK: {bitcoin_network}')

    backend.raise_policy = RaisePolicy.RAISE_CUSTOM
    backend.whitelisted_status = [0x9000, 0xE000]
    return createRaggerClient(backend, chain=chain, debug=True, screenshot_dir=TESTS_ROOT_DIR)
