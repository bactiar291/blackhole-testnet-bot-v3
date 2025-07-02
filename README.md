# blackhole-testnet-bot-v3
FULL FITUR
# 🕳️ blackhole-testnet-bot-v3

Automated bot for interacting with the [BlackHole Testnet](https://testnet.blackhole.xyz/) on Fuji (43113).  
Built using Python and Web3, this bot can perform multi-token swaps, liquidity actions, and staking operations automatically.

---

## 🚀 Features

- ✅ **Token Swap Automation**
  - Swap BLACK ➜ USDC
  - Swap BLACK ➜ BTC.b
  - Swap BLACK ➜ SUPER
  - Supports randomized BLACK amount per transaction for realistic simulation

- 💧 **Liquidity Management**
  - Add liquidity to BLACK/USDC vAMM pair
  - Approve and stake LP tokens
  - Claim LP fees before staking

- 🔒 **veToken Management (Vote-Escrow)**
  - Create veNFT lock using BLACK tokens
  - Increase locked amount
  - Merge veNFTs
  - Incentivize voting with rewards

- 🔄 **Loop Mode**
  - Auto-loop swap, stake, and liquidity processes
  - Randomized delays and amount for stealth operations
  - Clear terminal output status for each action

- 🌐 **Network**
  - Testnet: Fuji (43113)
  - Custom Router, LP token, and Gauge contract addresses integrated

---

## 📦 Installation

Clone the repository and install dependencies:

```
git clone https://github.com/bactiar291/blackhole-testnet-bot-v3.git
cd blackhole-testnet-bot-v3
pip install -r requirements.txt
```
