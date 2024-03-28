# Telegram Bot

This is a Telegram bot implemented using Python's aiogram library. The bot handles user authorization, admin privileges, and various commands for communication and user management.

## Installation

1. Clone the repository:

    ```bash
    git clone <repository_url>
    ```

2. Navigate to the cloned directory:

    ```bash
    cd <cloned_directory>
    ```

3. Install dependencies using `requirements.txt`:

    ```bash
    pip install -r requirements.txt
    ```

4. Docker setup:

    Docker configuration is already included in the repository. You can directly build and run the Docker container if you prefer to deploy using Docker.

    - Build Docker image:

        ```bash
        docker build -t telegram-bot .
        ```

    - Run Docker container:

        ```bash
        docker run -d telegram-bot
        ```

## Usage

1. Obtain a bot token from Bot Father on Telegram.
2. Set the obtained token in the `TOKEN` variable within the code.
3. Set the `creator` variable to your Telegram user ID.
4. Customize admin usernames and any other configurations as needed.
5. Run the bot script:

    ```bash
    python <bot_script_name>.py
    ```

## Commands

- `/allow <user_id>`: Authorize a user.
- `/deny <user_id>`: Deny authorization for a user.
- `/help`: Display help message.
- `/admin <user_id>`: Grant admin privileges to a user (only accessible to the creator).
- `/text <message>`: Send a message to all authorized users.
- `/textto <user_id> <message>`: Send a message to a specific user.
- `/users`: Display list of authorized users.
- `/all`: Display all user nicknames.
- `/banned`: Display list of banned users.
- `/save`: Save data to files.
- `/ban <user_id>`: Ban a user.
- `/free <user_id>`: Release a user from ban.
- `/delete <user_id>`: Delete a user.

## Contributions

Contributions to improve and extend the functionality of this bot are welcome. If you find any issues or have suggestions for improvements, feel free to open an issue or submit a pull request.

## License

This project is licensed under the [Author's Terms](LICENSE). Modification and redistribution are only permitted with the author's consent.



