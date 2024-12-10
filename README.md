# CSFloat Bot

A Discord bot for monitoring new CS:GO item listings based on specific search parameters. This bot checks for new items, alerts only for unseen items, and supports dynamic configuration via Discord commands.

## Features ✨
- **Track Listings:** Monitor CS:GO item listings from CSFloat.
- **Dynamic Configuration:** Update search parameters, such as item name, rarity, and price, directly through Discord commands.
- **Database Integration:** Keep track of seen listings using SQLite, ensuring notifications are only sent for new items.
- **Batch Notifications:** Efficiently send alerts to Discord while respecting rate limits.

---

## Setup 🛠️

### Prerequisites
1. **Python 3.10+**
   - Install Python from the [official website](https://www.python.org/downloads/).
2. **Dependencies**
   - Use `pip` to install the required dependencies.

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/csfloat-bot.git
   cd csfloat-bot

1.  Install the dependencies:

    bash

    Copy code

    `pip install -r requirements.txt`

2.  Configure the bot:

    -   Update the `config.py` file with your API tokens, Discord bot token, and webhook URL.
3.  Initialize the database:

    -   The database (`csfloat_bot.db`) is automatically created when you run the bot.
4.  Run the bot:

    bash

    Copy code

    `python bot.py`

* * * * *

Commands 📋
-----------

| Command | Description |
| --- | --- |
| `!set_parameter <param> <value>` | Set search parameters dynamically. |
| `!set_frequency <seconds>` | Update the monitoring interval (minimum 10 secs). |
| `!check` | Manually trigger a listing check. |
| `!all` | Fetch and display all available listings. |
| `!bot_help` | Display a list of all available commands. |

* * * * *

Search Parameters 🔍
--------------------

You can set the following search parameters dynamically:

-   `market_hash_name`: The name of the item (e.g., `★ M9 Bayonet | Fade`).
-   `min_float`: Minimum float value.
-   `max_float`: Maximum float value.
-   `rarity`: Item rarity.
-   `paint_seed`: Specific paint seed.
-   `paint_index`: Specific paint index.
-   `user_id`: Listings by a specific user.
-   `collection`: Item collection (e.g., `set_bravo_ii`).
-   `min_price`: Minimum price (in cents).
-   `max_price`: Maximum price (in cents).

**Example:**

`
   !set_var market_hash_name ★ M9 Bayonet | Fade
`
`
   !set_var max_price 10000
`

* * * * *

Database 📂
-----------

The bot uses an SQLite database (`csfloat_bot.db`) to track seen listings:

-   Listings are stored by their unique `listing_id`.
-   Alerts are only sent for new, unseen items.

* * * * *

Contributing 🤝
---------------

Contributions are welcome! Feel free to submit issues or pull requests.

1.  Fork the repository.
2.  Create a new branch:

    bash



    `git checkout -b feature-name`

3.  Commit your changes:

    bash

    Copy code

    `git commit -m "Add new feature"`

4.  Push to your branch:

    bash

    Copy code

    `git push origin feature-name`

5.  Open a pull request.

* * * * *

License 📜
----------

This project is licensed under the MIT License.
