from web3 import Web3
import os
import time
import random
from dotenv import load_dotenv
import sys
import platform

def clear_terminal():
    os.system('cls' if platform.system() == 'Windows' else 'clear')

def show_banner():
    clear_terminal()
    print("\033[1;36m" + "=" * 70)
    print(f"{'BACTIAR 291':^70}")
    print(f"{'BLACKHOLE TESTNET BOT':^70}")
    print("=" * 70)
    print(f"{'FITUR: Auto Swap | Auto Liquidity | Auto Lock | Auto Claim Fees':^70}")
    print("=" * 70 + "\033[0m")
    print("\033[1;33mMemulai bot...\033[0m\n")

load_dotenv()
PRIVATE_KEY = os.getenv('PRIVATE_KEY')
ADDRESS = Web3.to_checksum_address(os.getenv('ADDRESS'))

w3 = Web3(Web3.HTTPProvider('https://api.avax-test.network/ext/bc/C/rpc'))
account = w3.eth.account.from_key(PRIVATE_KEY)

class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    RESET = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

ROUTER = Web3.to_checksum_address('0x1B6814F3227a246F62bC47b148b3d288Dbc85715')
BLACK  = Web3.to_checksum_address('0xa981371a120b0e1bbdcd0abab1ed509c1084fe5f')
USDC   = Web3.to_checksum_address('0xdbd50be1580d9fda08a410e5ec023170166016ee')
BTCB   = Web3.to_checksum_address('0x1de9527f1638e3c1876cf390eb1389ab2bfde949')
SUPER  = Web3.to_checksum_address('0x2d65b197f04109724dfac2ec74775190eac7af7d')
PAIR_USDC  = Web3.to_checksum_address('0x1e08f83d4133d9f8337430d71e46ffea21c32201')
PAIR_BTCB  = Web3.to_checksum_address('0xe01ff66dbd8d8f16845ca96345ba59f20a258db2')
PAIR_SUPER = Web3.to_checksum_address('0xfa01e6325ad1012b6f855d09a862ea3dba7ef5da')
LOCK_CONTRACT = Web3.to_checksum_address('0x4854B431d864A7A9bEeD0033A1ec26c3Dc792F06')
INCENTIVE_CONTRACT = Web3.to_checksum_address('0x643d0a3E9e95474EF5Ad4213DaAD2e3BB52298ba')

# ABIs
ERC20_ABI = [
    {"constant": True, "inputs": [{"name": "owner", "type": "address"}], "name": "balanceOf", "outputs": [{"name": "", "type": "uint256"}], "type": "function"},
    {"constant": True, "inputs": [{"name": "owner", "type": "address"}, {"name": "spender", "type": "address"}], "name": "allowance", "outputs": [{"name": "", "type": "uint256"}], "type": "function"},
    {"constant": True, "inputs": [], "name": "decimals", "outputs": [{"name": "", "type": "uint8"}], "type": "function"}
]

ROUTER_ABI = [
    {
        "name": "swapExactTokensForTokens",
        "type": "function",
        "inputs": [
            {"name": "amountIn", "type": "uint256"},
            {"name": "amountOutMin", "type": "uint256"},
            {"name": "routes", "type": "tuple[]", "components": [
                {"name": "pair", "type": "address"},
                {"name": "from", "type": "address"},
                {"name": "to", "type": "address"},
                {"name": "stable", "type": "bool"},
                {"name": "concentrated", "type": "bool"},
                {"name": "receiver", "type": "address"}
            ]},
            {"name": "to", "type": "address"},
            {"name": "deadline", "type": "uint256"}
        ],
        "outputs": [{"name": "amounts", "type": "uint256[]"}],
        "stateMutability": "nonpayable"
    },
    {
        "name": "addLiquidity",
        "type": "function",
        "inputs": [
            {"name": "tokenA", "type": "address"},
            {"name": "tokenB", "type": "address"},
            {"name": "stable", "type": "bool"},
            {"name": "amountADesired", "type": "uint256"},
            {"name": "amountBDesired", "type": "uint256"},
            {"name": "amountAMin", "type": "uint256"},
            {"name": "amountBMin", "type": "uint256"},
            {"name": "to", "type": "address"},
            {"name": "deadline", "type": "uint256"}
        ],
        "outputs": [
            {"name": "amountA", "type": "uint256"},
            {"name": "amountB", "type": "uint256"},
            {"name": "liquidity", "type": "uint256"}
        ],
        "stateMutability": "nonpayable"
    }
]

PAIR_ABI = [
    {"constant": True, "inputs": [], "name": "getReserves", "outputs": [
        {"name": "_reserve0", "type": "uint112"},
        {"name": "_reserve1", "type": "uint112"},
        {"name": "_blockTimestampLast", "type": "uint32"}], "type": "function"},
    {"constant": True, "inputs": [], "name": "token0", "outputs": [{"name": "", "type": "address"}], "type": "function"},
    {"constant": True, "inputs": [], "name": "token1", "outputs": [{"name": "", "type": "address"}], "type": "function"}
]

LP_ABI = [
    {
        "inputs": [],
        "name": "claimFees",
        "outputs": [
            {"internalType": "uint256", "name": "claimed0", "type": "uint256"},
            {"internalType": "uint256", "name": "claimed1", "type": "uint256"}
        ],
        "stateMutability": "nonpayable",
        "type": "function"
    }
]

LOCK_ABI = [
    {
        "name": "create_lock",
        "type": "function",
        "stateMutability": "nonpayable",
        "inputs": [
            {"internalType": "uint256", "name": "_value", "type": "uint256"},
            {"internalType": "uint256", "name": "_lock_duration", "type": "uint256"},
            {"internalType": "bool", "name": "isSMNFT", "type": "bool"}
        ],
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}]
    },
    {
        "name": "increase_amount",
        "type": "function",
        "stateMutability": "nonpayable",
        "inputs": [
            {"internalType": "uint256", "name": "_tokenId", "type": "uint256"},
            {"internalType": "uint256", "name": "_value", "type": "uint256"}
        ],
        "outputs": []
    },
    {
        "name": "merge",
        "type": "function",
        "stateMutability": "nonpayable",
        "inputs": [
            {"internalType": "uint256", "name": "_from", "type": "uint256"},
            {"internalType": "uint256", "name": "_to", "type": "uint256"}
        ],
        "outputs": []
    },
    {
        "name": "balanceOf",
        "type": "function",
        "stateMutability": "view",
        "inputs": [{"internalType": "address", "name": "owner", "type": "address"}],
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}]
    },
    {
        "name": "tokenOfOwnerByIndex",
        "type": "function",
        "stateMutability": "view",
        "inputs": [
            {"internalType": "address", "name": "owner", "type": "address"},
            {"internalType": "uint256", "name": "index", "type": "uint256"}
        ],
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}]
    }
]

INCENTIVE_ABI = [
    {
        "name": "notifyRewardAmount",
        "type": "function",
        "stateMutability": "nonpayable",
        "inputs": [
            {"internalType": "address", "name": "_rewardsToken", "type": "address"},
            {"internalType": "uint256", "name": "reward", "type": "uint256"}
        ],
        "outputs": []
    }
]

router = w3.eth.contract(address=ROUTER, abi=ROUTER_ABI)
lock_contract = w3.eth.contract(address=LOCK_CONTRACT, abi=LOCK_ABI)
incentive_contract = w3.eth.contract(address=INCENTIVE_CONTRACT, abi=INCENTIVE_ABI)

def get_gas():
    gas_price = w3.eth.gas_price
    print(f"{Colors.YELLOW}⛽ Gas Price: {gas_price} wei{Colors.RESET}")
    return gas_price

def get_balance_and_allowance(token_addr):
    token = w3.eth.contract(address=token_addr, abi=ERC20_ABI)
    allowance = token.functions.allowance(ADDRESS, ROUTER).call()
    balance = token.functions.balanceOf(ADDRESS).call()
    decimals = token.functions.decimals().call()
    return balance, allowance, decimals

def do_swap(amount_black, to_token, pair_address, concentrated=False):
    balance, allowance, decimals = get_balance_and_allowance(BLACK)
    amount_in = int(amount_black * 10**decimals)
    min_out = 0

    if balance < amount_in:
        print(f"{Colors.RED}❌ Saldo BLACK tidak cukup.{Colors.RESET}")
        return False

    if allowance < amount_in:
        print(f"{Colors.RED}❌ Allowance kurang.{Colors.RESET}")
        return False

    symbol = {USDC: "USDC", BTCB: "BTC.b", SUPER: "SUPER"}.get(to_token, "Unknown")
    print(f"\n{Colors.CYAN}🔁 Swap {amount_black} BLACK → {symbol}{Colors.RESET}")

    route = [{
        'pair': pair_address,
        'from': BLACK,
        'to': to_token,
        'stable': False,
        'concentrated': concentrated,
        'receiver': ADDRESS
    }]
    nonce = w3.eth.get_transaction_count(ADDRESS)

    try:
        tx = router.functions.swapExactTokensForTokens(
            amount_in,
            min_out,
            route,
            ADDRESS,
            int(time.time()) + 300
        ).build_transaction({
            'from': ADDRESS,
            'nonce': nonce,
            'gas': 550000,
            'gasPrice': get_gas()
        })

        signed = w3.eth.account.sign_transaction(tx, PRIVATE_KEY)
        tx_hash = w3.eth.send_raw_transaction(signed.raw_transaction)
        print(f"{Colors.BLUE}📤 TX sent: {tx_hash.hex()}{Colors.RESET}")

        receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        if receipt.status == 1:
            print(f"{Colors.GREEN}✅ Swap sukses!{Colors.RESET}")
            return True
        else:
            print(f"{Colors.RED}❌ Swap gagal (status 0){Colors.RESET}")
            return False

    except Exception as e:
        print(f"{Colors.RED}💥 ERROR: {e}{Colors.RESET}")
        return False

def get_balances_allow():
    tok = w3.eth.contract(BLACK, abi=ERC20_ABI)
    balA, alfA, decA = tok.functions.balanceOf(ADDRESS).call(), tok.functions.allowance(ADDRESS, ROUTER).call(), tok.functions.decimals().call()
    tok2 = w3.eth.contract(USDC, abi=ERC20_ABI)
    balB, alfB, decB = tok2.functions.balanceOf(ADDRESS).call(), tok2.functions.allowance(ADDRESS, ROUTER).call(), tok2.functions.decimals().call()
    return balA, alfA, decA, balB, alfB, decB

def quote_amountB(amountA):
    pair = w3.eth.contract(PAIR_USDC, abi=PAIR_ABI)
    res0, res1, _ = pair.functions.getReserves().call()
    tok0 = pair.functions.token0().call()
    if tok0.lower() == BLACK.lower():
        reserveA, reserveB = res0, res1
    else:
        reserveA, reserveB = res1, res0
    return amountA * reserveB // reserveA

def add_liq_quote():
    balA, alfA, decA, balB, alfB, decB = get_balances_allow()
    if balA == 0 or balB == 0 or alfA == 0 or alfB == 0:
        print(f"{Colors.RED}❌ Need balance+allowance for BLACK and USDC{Colors.RESET}")
        return False

    amtA = int(0.001 * 10**decA)
    amtB = quote_amountB(amtA)
    minA = int(amtA * 0.95)
    minB = int(amtB * 0.95)
    print(f"{Colors.CYAN}💧 Adding Liquidity: {amtA/10**decA} BLACK + {amtB/10**decB} USDC{Colors.RESET}")

    try:
        tx = router.functions.addLiquidity(
            BLACK, USDC, False, amtA, amtB, minA, minB, ADDRESS, int(time.time())+300
        ).build_transaction({
            'from': ADDRESS, 
            'nonce': w3.eth.get_transaction_count(ADDRESS),
            'gas': 300000, 
            'gasPrice': get_gas()
        })
        
        signed = w3.eth.account.sign_transaction(tx, PRIVATE_KEY)
        tx_hash = w3.eth.send_raw_transaction(signed.raw_transaction)
        print(f"{Colors.BLUE}📤 TX: {tx_hash.hex()}{Colors.RESET}")
        
        rec = w3.eth.wait_for_transaction_receipt(tx_hash)
        if rec.status == 1:
            print(f"{Colors.GREEN}✅ Succeeded{Colors.RESET}")
            return True
        else:
            print(f"{Colors.RED}❌ Failed{Colors.RESET}")
            return False
            
    except Exception as e:
        print(f"{Colors.RED}❌ Error: {e}{Colors.RESET}")
        return False

def claim_fees():
    contract = w3.eth.contract(address=PAIR_USDC, abi=LP_ABI)
    nonce = w3.eth.get_transaction_count(ADDRESS)

    try:
        tx = contract.functions.claimFees().build_transaction({
            'from': ADDRESS,
            'nonce': nonce,
            'gas': 150000,
            'gasPrice': get_gas()
        })

        signed_tx = w3.eth.account.sign_transaction(tx, private_key=PRIVATE_KEY)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
        print(f"{Colors.BLUE}📤 Claim TX sent: {tx_hash.hex()}{Colors.RESET}")

        receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        if receipt.status == 1:
            print(f"{Colors.GREEN}✅ Claim sukses!{Colors.RESET}")
            return True
        else:
            print(f"{Colors.RED}❌ Claim gagal.{Colors.RESET}")
            return False
    except Exception as e:
        print(f"{Colors.RED}💥 Claim error: {e}{Colors.RESET}")
        return False

def get_latest_token_ids(address):
    balance = lock_contract.functions.balanceOf(address).call()
    if balance < 1:
        return []
    token_ids = []
    for i in range(balance):
        token_ids.append(lock_contract.functions.tokenOfOwnerByIndex(address, i).call())
    return token_ids

def send_tx(fn, args, gas=800000):
    try:
        tx = fn(*args).build_transaction({
            'from': ADDRESS,
            'nonce': w3.eth.get_transaction_count(ADDRESS),
            'gas': gas,
            'gasPrice': get_gas()
        })
        signed = w3.eth.account.sign_transaction(tx, PRIVATE_KEY)
        tx_hash = w3.eth.send_raw_transaction(signed.raw_transaction)
        print(f"{Colors.BLUE}📤 TX sent: {tx_hash.hex()}{Colors.RESET}")
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        if receipt.status == 1:
            print(f"{Colors.GREEN}✅ TX sukses!{Colors.RESET}")
            return True
        else:
            print(f"{Colors.RED}❌ TX gagal.{Colors.RESET}")
            return False
    except Exception as e:
        print(f"{Colors.RED}💥 TX error: {e}{Colors.RESET}")
        return False

def create_lock_and_merge():
    lock_seconds = 60 * 60 * 24 * 30  
    amount_black = round(random.uniform(0.001, 0.09), 6)
    value = w3.to_wei(amount_black, "ether")
    
    print(f"{Colors.CYAN}🔒 Membuat lock veBLACK sebanyak {amount_black} BLACK...{Colors.RESET}")
    if not send_tx(lock_contract.functions.create_lock, [value, lock_seconds, True]):
        return False

    time.sleep(10)
    token_ids = get_latest_token_ids(ADDRESS)
    if not token_ids:
        print(f"{Colors.YELLOW}❗ Tidak ada NFT ditemukan{Colors.RESET}")
        return False

    token_ids.sort()
    new_token = token_ids[-1]
    old_token = token_ids[0]

    if new_token == old_token:
        print(f"{Colors.YELLOW}❗ Tidak ada NFT untuk merge{Colors.RESET}")
        return True

    increase_amount = round(random.uniform(0.001, 0.05), 6)
    increase_value = w3.to_wei(increase_amount, "ether")
    print(f"{Colors.CYAN}💰 Menambah amount {increase_amount} BLACK ke NFT ID {new_token}...{Colors.RESET}")
    if not send_tx(lock_contract.functions.increase_amount, [new_token, increase_value]):
        return False

    time.sleep(5)
    print(f"{Colors.CYAN}🔗 Merge NFT {new_token} → {old_token}...{Colors.RESET}")
    return send_tx(lock_contract.functions.merge, [new_token, old_token])

def auto_merge_all_tokens():
    token_ids = get_latest_token_ids(ADDRESS)
    if len(token_ids) < 2:
        print(f"{Colors.YELLOW}❗ Minimal 2 NFT dibutuhkan untuk merge{Colors.RESET}")
        return True

    token_ids.sort()
    main_token = token_ids[0]
    print(f"{Colors.CYAN}🧩 Menggabungkan semua token ke ID utama: {main_token}{Colors.RESET}")

    success = True
    for token_id in token_ids[1:]:
        print(f"{Colors.CYAN}🔗 Merge token {token_id} → {main_token}...{Colors.RESET}")
        if not send_tx(lock_contract.functions.merge, [token_id, main_token]):
            success = False
        time.sleep(3)
    
    if success:
        print(f"{Colors.GREEN}✅ Semua token berhasil digabung!{Colors.RESET}")
    return success

def send_incentive():
    amount = round(random.uniform(0.001, 0.01), 6)
    reward = w3.to_wei(amount, "ether")
    print(f"{Colors.CYAN}🎁 Mengirim auto incentive: {amount} BLACK...{Colors.RESET}")
    return send_tx(incentive_contract.functions.notifyRewardAmount, [BLACK, reward], gas=120000)

def do_veblack_ops():
    print(f"\n{Colors.MAGENTA}===== Memulai operasi veBLACK =====")
    if not create_lock_and_merge():
        print(f"{Colors.RED}❌ Gagal pada create_lock_and_merge{Colors.RESET}")
    if not auto_merge_all_tokens():
        print(f"{Colors.RED}❌ Gagal pada auto_merge_all_tokens{Colors.RESET}")
    if not send_incentive():
        print(f"{Colors.RED}❌ Gagal pada send_incentive{Colors.RESET}")
    print(f"{Colors.MAGENTA}===== Operasi veBLACK selesai ====={Colors.RESET}")
    return True

def main_loop():
    operations = [
        ("SWAP", 4),
        ("LIQUIDITY", 2),
        ("CLAIM", 1),
        ("veBLACK", 3)
    ]
    
    while True:
        total_weight = sum(weight for _, weight in operations)
        r = random.uniform(0, total_weight)
        current = 0
        for op, weight in operations:
            current += weight
            if r < current:
                selected_op = op
                break
        
        print(f"\n{Colors.BOLD}{'='*50}{Colors.RESET}")
        print(f"{Colors.BOLD}Memilih operasi: {selected_op}{Colors.RESET}")
        print(f"{Colors.BOLD}{'='*50}{Colors.RESET}")
        
        try:
            if selected_op == "SWAP":
                pick = random.choice(["USDC", "BTCB", "SUPER"])
                if pick == "USDC":
                    amount = random.choice([0.01, 0.03, 0.05, 0.07, 0.09])
                    do_swap(amount, USDC, PAIR_USDC)
                elif pick == "BTCB":
                    amount = random.choice([0.05, 0.07, 0.09])
                    do_swap(amount, BTCB, PAIR_BTCB, concentrated=True)
                elif pick == "SUPER":
                    amount = random.choice([0.01, 0.03, 0.05])
                    do_swap(amount, SUPER, PAIR_SUPER)
            
            elif selected_op == "LIQUIDITY":
                add_liq_quote()
            
            elif selected_op == "CLAIM":
                claim_fees()
            
            elif selected_op == "veBLACK":
                do_veblack_ops()
        
        except Exception as e:
            print(f"{Colors.RED}💥 Error utama: {e}{Colors.RESET}")
        
        delay = random.randint(15, 30)
        print(f"\n{Colors.YELLOW}🕒 Menunggu {delay} detik...{Colors.RESET}")
        time.sleep(delay)

if __name__ == "__main__":
    show_banner()
    print(f"{Colors.GREEN}🚀 Memulai bot automasi...{Colors.RESET}")
    try:
        main_loop()
    except KeyboardInterrupt:
        print(f"\n{Colors.RED}🚫 Bot dihentikan oleh pengguna{Colors.RESET}")
        sys.exit(0)
