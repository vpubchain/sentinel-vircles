import pytest
import sys
import os
import re
os.environ['SENTINEL_ENV'] = 'test'
os.environ['SENTINEL_CONFIG'] = os.path.normpath(os.path.join(os.path.dirname(__file__), '../test_sentinel.conf'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
import config

from virclesd import VirclesDaemon
from vircles_config import VirclesConfig


def test_virclesd():
    config_text = VirclesConfig.slurp_config_file(config.vircles_conf)
    network = 'mainnet'
    is_testnet = False
    genesis_hash = u'000006e5c08d6d2414435b294210266753b05a75f90e926dd5e6082306812622'
    for line in config_text.split("\n"):
        if line.startswith('testnet=1'):
            network = 'testnet'
            is_testnet = True
            genesis_hash = u'00000478aace753a4709f7503b5b583456a5a8635e989d7f899eb000bbea9fd4'

    creds = VirclesConfig.get_rpc_creds(config_text, network)
    virclesd = VirclesDaemon(**creds)
    assert virclesd.rpc_command is not None

    assert hasattr(virclesd, 'rpc_connection')

    # Vircles testnet block 0 hash == 00000bafbc94add76cb75e2ec92894837288a481e5c005f6563d91623bf8bc2c
    # test commands without arguments
    info = virclesd.rpc_command('getblockchaininfo')
    info_keys = [
        'chain',
        'blocks',
        'headers',
        'difficulty'
    ]
    for key in info_keys:
        assert key in info
    assert info['chain'] is (is_testnet ? "testnet" : "main")

    # test commands with args
    assert virclesd.rpc_command('getblockhash', 0) == genesis_hash
