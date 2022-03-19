const top_100_coins = [
    {
        "id": 1,
        "name": "Bitcoin",
        "symbol": "BTC",
        "slug": "bitcoin",
        "is_active": 1,
        "status": "active",
        "rank": 1
    },
    {
        "id": 1027,
        "name": "Ethereum",
        "symbol": "ETH",
        "slug": "ethereum",
        "is_active": 1,
        "status": "active",
        "rank": 2
    },
    {
        "id": 825,
        "name": "Tether",
        "symbol": "USDT",
        "slug": "tether",
        "is_active": 1,
        "status": "active",
        "rank": 3
    },
    {
        "id": 1839,
        "name": "BNB",
        "symbol": "BNB",
        "slug": "bnb",
        "is_active": 1,
        "status": "active",
        "rank": 4
    },
    {
        "id": 3408,
        "name": "USD Coin",
        "symbol": "USDC",
        "slug": "usd-coin",
        "is_active": 1,
        "status": "active",
        "rank": 5
    },
    {
        "id": 4172,
        "name": "Terra",
        "symbol": "LUNA",
        "slug": "terra-luna",
        "is_active": 1,
        "status": "active",
        "rank": 6
    },
    {
        "id": 52,
        "name": "XRP",
        "symbol": "XRP",
        "slug": "xrp",
        "is_active": 1,
        "status": "active",
        "rank": 7
    },
    {
        "id": 2010,
        "name": "Cardano",
        "symbol": "ADA",
        "slug": "cardano",
        "is_active": 1,
        "status": "active",
        "rank": 8
    },
    {
        "id": 5426,
        "name": "Solana",
        "symbol": "SOL",
        "slug": "solana",
        "is_active": 1,
        "status": "active",
        "rank": 9
    },
    {
        "id": 5805,
        "name": "Avalanche",
        "symbol": "AVAX",
        "slug": "avalanche",
        "is_active": 1,
        "status": "active",
        "rank": 10
    },
    {
        "id": 4687,
        "name": "Binance USD",
        "symbol": "BUSD",
        "slug": "binance-usd",
        "is_active": 1,
        "status": "active",
        "rank": 11
    },
    {
        "id": 6636,
        "name": "Polkadot",
        "symbol": "DOT",
        "slug": "polkadot-new",
        "is_active": 1,
        "status": "active",
        "rank": 12
    },
    {
        "id": 74,
        "name": "Dogecoin",
        "symbol": "DOGE",
        "slug": "dogecoin",
        "is_active": 1,
        "status": "active",
        "rank": 13
    },
    {
        "id": 7129,
        "name": "TerraUSD",
        "symbol": "UST",
        "slug": "terrausd",
        "is_active": 1,
        "status": "active",
        "rank": 14
    },
    {
        "id": 5994,
        "name": "Shiba Inu",
        "symbol": "SHIB",
        "slug": "shiba-inu",
        "is_active": 1,
        "status": "active",
        "rank": 15
    },
    {
        "id": 3890,
        "name": "Polygon",
        "symbol": "MATIC",
        "slug": "polygon",
        "is_active": 1,
        "status": "active",
        "rank": 16
    },
    {
        "id": 3717,
        "name": "Wrapped Bitcoin",
        "symbol": "WBTC",
        "slug": "wrapped-bitcoin",
        "is_active": 1,
        "status": "active",
        "rank": 17
    },
    {
        "id": 3635,
        "name": "Cronos",
        "symbol": "CRO",
        "slug": "cronos",
        "is_active": 1,
        "status": "active",
        "rank": 18
    },
    {
        "id": 4943,
        "name": "Dai",
        "symbol": "DAI",
        "slug": "multi-collateral-dai",
        "is_active": 1,
        "status": "active",
        "rank": 19
    },
    {
        "id": 3794,
        "name": "Cosmos",
        "symbol": "ATOM",
        "slug": "cosmos",
        "is_active": 1,
        "status": "active",
        "rank": 20
    },
    {
        "id": 6535,
        "name": "NEAR Protocol",
        "symbol": "NEAR",
        "slug": "near-protocol",
        "is_active": 1,
        "status": "active",
        "rank": 21
    },
    {
        "id": 2,
        "name": "Litecoin",
        "symbol": "LTC",
        "slug": "litecoin",
        "is_active": 1,
        "status": "active",
        "rank": 22
    },
    {
        "id": 1975,
        "name": "Chainlink",
        "symbol": "LINK",
        "slug": "chainlink",
        "is_active": 1,
        "status": "active",
        "rank": 23
    },
    {
        "id": 1958,
        "name": "TRON",
        "symbol": "TRX",
        "slug": "tron",
        "is_active": 1,
        "status": "active",
        "rank": 24
    },
    {
        "id": 7083,
        "name": "Uniswap",
        "symbol": "UNI",
        "slug": "uniswap",
        "is_active": 1,
        "status": "active",
        "rank": 25
    },
    {
        "id": 4195,
        "name": "FTX Token",
        "symbol": "FTT",
        "slug": "ftx-token",
        "is_active": 1,
        "status": "active",
        "rank": 26
    },
    {
        "id": 1831,
        "name": "Bitcoin Cash",
        "symbol": "BCH",
        "slug": "bitcoin-cash",
        "is_active": 1,
        "status": "active",
        "rank": 27
    },
    {
        "id": 3957,
        "name": "UNUS SED LEO",
        "symbol": "LEO",
        "slug": "unus-sed-leo",
        "is_active": 1,
        "status": "active",
        "rank": 28
    },
    {
        "id": 4030,
        "name": "Algorand",
        "symbol": "ALGO",
        "slug": "algorand",
        "is_active": 1,
        "status": "active",
        "rank": 29
    },
    {
        "id": 512,
        "name": "Stellar",
        "symbol": "XLM",
        "slug": "stellar",
        "is_active": 1,
        "status": "active",
        "rank": 30
    },
    {
        "id": 1966,
        "name": "Decentraland",
        "symbol": "MANA",
        "slug": "decentraland",
        "is_active": 1,
        "status": "active",
        "rank": 31
    },
    {
        "id": 4642,
        "name": "Hedera",
        "symbol": "HBAR",
        "slug": "hedera",
        "is_active": 1,
        "status": "active",
        "rank": 32
    },
    {
        "id": 4023,
        "name": "Bitcoin BEP2",
        "symbol": "BTCB",
        "slug": "bitcoin-bep2",
        "is_active": 1,
        "status": "active",
        "rank": 33
    },
    {
        "id": 1321,
        "name": "Ethereum Classic",
        "symbol": "ETC",
        "slug": "ethereum-classic",
        "is_active": 1,
        "status": "active",
        "rank": 34
    },
    {
        "id": 8916,
        "name": "Internet Computer",
        "symbol": "ICP",
        "slug": "internet-computer",
        "is_active": 1,
        "status": "active",
        "rank": 35
    },
    {
        "id": 3513,
        "name": "Fantom",
        "symbol": "FTM",
        "slug": "fantom",
        "is_active": 1,
        "status": "active",
        "rank": 36
    },
    {
        "id": 6210,
        "name": "The Sandbox",
        "symbol": "SAND",
        "slug": "the-sandbox",
        "is_active": 1,
        "status": "active",
        "rank": 37
    },
    {
        "id": 2280,
        "name": "Filecoin",
        "symbol": "FIL",
        "slug": "filecoin",
        "is_active": 1,
        "status": "active",
        "rank": 38
    },
    {
        "id": 328,
        "name": "Monero",
        "symbol": "XMR",
        "slug": "monero",
        "is_active": 1,
        "status": "active",
        "rank": 39
    },
    {
        "id": 6892,
        "name": "Elrond",
        "symbol": "EGLD",
        "slug": "elrond-egld",
        "is_active": 1,
        "status": "active",
        "rank": 40
    },
    {
        "id": 3077,
        "name": "VeChain",
        "symbol": "VET",
        "slug": "vechain",
        "is_active": 1,
        "status": "active",
        "rank": 41
    },
    {
        "id": 1274,
        "name": "Waves",
        "symbol": "WAVES",
        "slug": "waves",
        "is_active": 1,
        "status": "active",
        "rank": 42
    },
    {
        "id": 4256,
        "name": "Klaytn",
        "symbol": "KLAY",
        "slug": "klaytn",
        "is_active": 1,
        "status": "active",
        "rank": 43
    },
    {
        "id": 2416,
        "name": "Theta Network",
        "symbol": "THETA",
        "slug": "theta-network",
        "is_active": 1,
        "status": "active",
        "rank": 44
    },
    {
        "id": 6783,
        "name": "Axie Infinity",
        "symbol": "AXS",
        "slug": "axie-infinity",
        "is_active": 1,
        "status": "active",
        "rank": 45
    },
    {
        "id": 2011,
        "name": "Tezos",
        "symbol": "XTZ",
        "slug": "tezos",
        "is_active": 1,
        "status": "active",
        "rank": 46
    },
    {
        "id": 5665,
        "name": "Helium",
        "symbol": "HNT",
        "slug": "helium",
        "is_active": 1,
        "status": "active",
        "rank": 47
    },
    {
        "id": 1720,
        "name": "IOTA",
        "symbol": "MIOTA",
        "slug": "iota",
        "is_active": 1,
        "status": "active",
        "rank": 48
    },
    {
        "id": 4558,
        "name": "Flow",
        "symbol": "FLOW",
        "slug": "flow",
        "is_active": 1,
        "status": "active",
        "rank": 49
    },
    {
        "id": 1437,
        "name": "Zcash",
        "symbol": "ZEC",
        "slug": "zcash",
        "is_active": 1,
        "status": "active",
        "rank": 50
    },
    {
        "id": 1765,
        "name": "EOS",
        "symbol": "EOS",
        "slug": "eos",
        "is_active": 1,
        "status": "active",
        "rank": 51
    },
    {
        "id": 4847,
        "name": "Stacks",
        "symbol": "STX",
        "slug": "stacks",
        "is_active": 1,
        "status": "active",
        "rank": 52
    },
    {
        "id": 1518,
        "name": "Maker",
        "symbol": "MKR",
        "slug": "maker",
        "is_active": 1,
        "status": "active",
        "rank": 53
    },
    {
        "id": 4157,
        "name": "THORChain",
        "symbol": "RUNE",
        "slug": "thorchain",
        "is_active": 1,
        "status": "active",
        "rank": 54
    },
    {
        "id": 7186,
        "name": "PancakeSwap",
        "symbol": "CAKE",
        "slug": "pancakeswap",
        "is_active": 1,
        "status": "active",
        "rank": 55
    },
    {
        "id": 16086,
        "name": "BitTorrent (New)",
        "symbol": "BTT",
        "slug": "bittorrent-new",
        "is_active": 1,
        "status": "active",
        "rank": 56
    },
    {
        "id": 7278,
        "name": "Aave",
        "symbol": "AAVE",
        "slug": "aave",
        "is_active": 1,
        "status": "active",
        "rank": 57
    },
    {
        "id": 10791,
        "name": "eCash",
        "symbol": "XEC",
        "slug": "ecash",
        "is_active": 1,
        "status": "active",
        "rank": 58
    },
    {
        "id": 6719,
        "name": "The Graph",
        "symbol": "GRT",
        "slug": "the-graph",
        "is_active": 1,
        "status": "active",
        "rank": 59
    },
    {
        "id": 7080,
        "name": "Gala",
        "symbol": "GALA",
        "slug": "gala",
        "is_active": 1,
        "status": "active",
        "rank": 60
    },
    {
        "id": 3945,
        "name": "Harmony",
        "symbol": "ONE",
        "slug": "harmony",
        "is_active": 1,
        "status": "active",
        "rank": 61
    },
    {
        "id": 3602,
        "name": "Bitcoin SV",
        "symbol": "BSV",
        "slug": "bitcoin-sv",
        "is_active": 1,
        "status": "active",
        "rank": 62
    },
    {
        "id": 2563,
        "name": "TrueUSD",
        "symbol": "TUSD",
        "slug": "trueusd",
        "is_active": 1,
        "status": "active",
        "rank": 63
    },
    {
        "id": 2087,
        "name": "KuCoin Token",
        "symbol": "KCS",
        "slug": "kucoin-token",
        "is_active": 1,
        "status": "active",
        "rank": 64
    },
    {
        "id": 1376,
        "name": "Neo",
        "symbol": "NEO",
        "slug": "neo",
        "is_active": 1,
        "status": "active",
        "rank": 65
    },
    {
        "id": 2502,
        "name": "Huobi Token",
        "symbol": "HT",
        "slug": "huobi-token",
        "is_active": 1,
        "status": "active",
        "rank": 66
    },
    {
        "id": 3155,
        "name": "Quant",
        "symbol": "QNT",
        "slug": "quant",
        "is_active": 1,
        "status": "active",
        "rank": 67
    },
    {
        "id": 4066,
        "name": "Chiliz",
        "symbol": "CHZ",
        "slug": "chiliz",
        "is_active": 1,
        "status": "active",
        "rank": 68
    },
    {
        "id": 2694,
        "name": "Nexo",
        "symbol": "NEXO",
        "slug": "nexo",
        "is_active": 1,
        "status": "active",
        "rank": 69
    },
    {
        "id": 2130,
        "name": "Enjin Coin",
        "symbol": "ENJ",
        "slug": "enjin-coin",
        "is_active": 1,
        "status": "active",
        "rank": 70
    },
    {
        "id": 5567,
        "name": "Celo",
        "symbol": "CELO",
        "slug": "celo",
        "is_active": 1,
        "status": "active",
        "rank": 71
    },
    {
        "id": 6945,
        "name": "Amp",
        "symbol": "AMP",
        "slug": "amp",
        "is_active": 1,
        "status": "active",
        "rank": 72
    },
    {
        "id": 5632,
        "name": "Arweave",
        "symbol": "AR",
        "slug": "arweave",
        "is_active": 1,
        "status": "active",
        "rank": 73
    },
    {
        "id": 5034,
        "name": "Kusama",
        "symbol": "KSM",
        "slug": "kusama",
        "is_active": 1,
        "status": "active",
        "rank": 74
    },
    {
        "id": 3897,
        "name": "OKB",
        "symbol": "OKB",
        "slug": "okb",
        "is_active": 1,
        "status": "active",
        "rank": 75
    },
    {
        "id": 5647,
        "name": "Kadena",
        "symbol": "KDA",
        "slug": "kadena",
        "is_active": 1,
        "status": "active",
        "rank": 76
    },
    {
        "id": 131,
        "name": "Dash",
        "symbol": "DASH",
        "slug": "dash",
        "is_active": 1,
        "status": "active",
        "rank": 77
    },
    {
        "id": 1697,
        "name": "Basic Attention Token",
        "symbol": "BAT",
        "slug": "basic-attention-token",
        "is_active": 1,
        "status": "active",
        "rank": 78
    },
    {
        "id": 8857,
        "name": "Anchor Protocol",
        "symbol": "ANC",
        "slug": "anchor-protocol",
        "is_active": 1,
        "status": "active",
        "rank": 79
    },
    {
        "id": 1934,
        "name": "Loopring",
        "symbol": "LRC",
        "slug": "loopring",
        "is_active": 1,
        "status": "active",
        "rank": 80
    },
    {
        "id": 3330,
        "name": "Pax Dollar",
        "symbol": "USDP",
        "slug": "paxos-standard",
        "is_active": 1,
        "status": "active",
        "rank": 81
    },
    {
        "id": 6538,
        "name": "Curve DAO Token",
        "symbol": "CRV",
        "slug": "curve-dao-token",
        "is_active": 1,
        "status": "active",
        "rank": 82
    },
    {
        "id": 873,
        "name": "NEM",
        "symbol": "XEM",
        "slug": "nem",
        "is_active": 1,
        "status": "active",
        "rank": 83
    },
    {
        "id": 9903,
        "name": "Convex Finance",
        "symbol": "CVX",
        "slug": "convex-finance",
        "is_active": 1,
        "status": "active",
        "rank": 84
    },
    {
        "id": 3822,
        "name": "Theta Fuel",
        "symbol": "TFUEL",
        "slug": "theta-fuel",
        "is_active": 1,
        "status": "active",
        "rank": 85
    },
    {
        "id": 7653,
        "name": "Oasis Network",
        "symbol": "ROSE",
        "slug": "oasis-network",
        "is_active": 1,
        "status": "active",
        "rank": 86
    },
    {
        "id": 8677,
        "name": "Symbol",
        "symbol": "XYM",
        "slug": "symbol",
        "is_active": 1,
        "status": "active",
        "rank": 87
    },
    {
        "id": 1168,
        "name": "Decred",
        "symbol": "DCR",
        "slug": "decred",
        "is_active": 1,
        "status": "active",
        "rank": 88
    },
    {
        "id": 2700,
        "name": "Celsius",
        "symbol": "CEL",
        "slug": "celsius",
        "is_active": 1,
        "status": "active",
        "rank": 89
    },
    {
        "id": 5604,
        "name": "Secret",
        "symbol": "SCRT",
        "slug": "secret",
        "is_active": 1,
        "status": "active",
        "rank": 90
    },
    {
        "id": 3801,
        "name": "BORA",
        "symbol": "BORA",
        "slug": "bora",
        "is_active": 1,
        "status": "active",
        "rank": 91
    },
    {
        "id": 8646,
        "name": "Mina",
        "symbol": "MINA",
        "slug": "mina",
        "is_active": 1,
        "status": "active",
        "rank": 92
    },
    {
        "id": 5864,
        "name": "yearn.finance",
        "symbol": "YFI",
        "slug": "yearn-finance",
        "is_active": 1,
        "status": "active",
        "rank": 93
    },
    {
        "id": 2682,
        "name": "Holo",
        "symbol": "HOT",
        "slug": "holo",
        "is_active": 1,
        "status": "active",
        "rank": 94
    },
    {
        "id": 5692,
        "name": "Compound",
        "symbol": "COMP",
        "slug": "compound",
        "is_active": 1,
        "status": "active",
        "rank": 95
    },
    {
        "id": 2777,
        "name": "IoTeX",
        "symbol": "IOTX",
        "slug": "iotex",
        "is_active": 1,
        "status": "active",
        "rank": 96
    },
    {
        "id": 2634,
        "name": "XDC Network",
        "symbol": "XDC",
        "slug": "xinfin",
        "is_active": 1,
        "status": "active",
        "rank": 97
    },
    {
        "id": 2099,
        "name": "ICON",
        "symbol": "ICX",
        "slug": "icon",
        "is_active": 1,
        "status": "active",
        "rank": 98
    },
    {
        "id": 4279,
        "name": "SXP",
        "symbol": "SXP",
        "slug": "sxp",
        "is_active": 1,
        "status": "active",
        "rank": 99
    },
    {
        "id": 4705,
        "name": "PAX Gold",
        "symbol": "PAXG",
        "slug": "pax-gold",
        "is_active": 1,
        "status": "active",
        "rank": 100
    }
]