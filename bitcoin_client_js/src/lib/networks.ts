import type { Network } from 'bitcoinjs-lib';

// Syscoin-specific network parameters for bitcoinjs-lib
// Source: syscoin/src/kernel/chainparams.cpp (base58 prefixes) and chainparams.h (bech32 HRP)
// - Mainnet: P2PKH=63 (0x3f), P2SH=5 (0x05), WIF=128 (0x80), HRP='sys'
// - Testnet: P2PKH=65 (0x41), P2SH=196 (0xc4), WIF=239 (0xef), HRP='tsys'
// - BIP32: same as Bitcoin (xpub/xprv for mainnet, tpub/tprv for testnet)

export const syscoinMainnet: Network = {
  messagePrefix: '\x18Syscoin Signed Message:\n',
  bech32: 'sys',
  bip32: {
    public: 0x0488b21e, // xpub
    private: 0x0488ade4, // xprv
  },
  pubKeyHash: 63,
  scriptHash: 5,
  wif: 0x80,
};

export const syscoinTestnet: Network = {
  messagePrefix: '\x18Syscoin Signed Message:\n',
  bech32: 'tsys',
  bip32: {
    public: 0x043587cf, // tpub
    private: 0x04358394, // tprv
  },
  pubKeyHash: 65,
  scriptHash: 196,
  wif: 0xef,
};
