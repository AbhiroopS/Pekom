# Pekom - A Discord Bot 🥕

A Discord bot with a Pekora-themed personality. Built with discord.py, featuring AI-powered message summarization, permission management and more to come...

![Python](https://img.shields.io/badge/python-3.12-blue)
![discord.py](https://img.shields.io/badge/discord.py-2.5+-blue.svg)
![Docker](https://img.shields.io/badge/Docker-ready-blue.svg)

## Features ✨

### Core Commands
- `/ping` - Ping the bot and get latency info
- `/echo` - Make the bot echo your message
- `/botstatus` - Check bot status and info

### Permission Management
- `/getperms` - Get permissions for a member or role
- `/getpermschannel` - Get permissions in a specific channel

### AI Summarization (The Fun Part)
- `/summarize` - Generate a hilarious AI-powered comedic recap of recent channel messages using OpenRouter

### Bot Features
- Rotating comedic status messages (Pekora-themed!)
- Slash commands with Discord's modern command system
- Guild-specific command syncing for testing
- Global command promotion for production

## Setup 🚀

### Prerequisites
- Python 3.12+
- Discord Bot Token
- OpenRouter API Key (optional, for summarize command)

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/AbhiroopS/Pekom.git
   cd Pekom
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   
   Create a `.env` file in the root directory:
   ```env
   TOKEN = your_discord_bot_token
   CLIENT_ID = your_client_id
   OWNER_ID = your_user_id
   TEST_GUILD_ID = your_test_server_id
   OPENROUTER_API_KEY = sk-your-key-here     # Optional
   ALLOWED_SUMMARIZE_USERS = your_user_id    # Comma-separated for multiple users
   ```

5. **Run the bot**
   ```bash
   python app.py
   ```

### Docker Deployment

1. **Build and run with Docker Compose**
   ```bash
   docker-compose up --build
   ```

## Project Structure 📁

```
Pekom/
├── app.py              # Main bot file with commands
├── cogs/               # Bot modules/cogs
│   ├── permissions.py  # Permission management commands
│   └── utility.py      # Utility commands (ping, echo, summarize)
├── Dockerfile          # Docker image configuration
├── docker-compose.yml  # Docker Compose configuration
├── requirements.txt    # Python dependencies
└── .env                # Environment variables
```

## Commands Reference 📖

| Command | Description | Owner Only |
|---------|-------------|------------|
| `/ping` | Get bot latency | No |
| `/echo [message]` | Echo a message | No |
| `/botstatus` | Check bot status | No |
| `/getperms [target]` | Get member/role permissions | No |
| `/getpermschannel [channel] [member]` | Get channel permissions | No |
| `/summarize [count]` | AI comedic summary | Yes* |
| `/sync [clear]` | Sync commands to test server | Yes |
| `/promote` | Promote commands globally | Yes |

*`/summarize` is restricted to users listed in `ALLOWED_SUMMARIZE_USERS`

## Acknowledgments 🙏

- [Pekora](https://www.youtube.com/@usadapekora) - The inspiration for this bot's name
- [discord.py](https://discordpy.readthedocs.io/) - The best Discord library
- [OpenRouter](https://openrouter.ai/) - For the AI summarization feature

---
