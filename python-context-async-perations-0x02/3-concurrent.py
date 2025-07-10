import aiosqlite
import asyncio

# Async function to fetch all users
async def async_fetch_users():
    async with aiosqlite.connect("users.db") as db:
        async with db.execute("SELECT * FROM users") as cursor:
            users = await cursor.fetchall()
            print("[ALL USERS]")
            for user in users:
                print(user)
            return users

# Async function to fetch users older than 40
async def async_fetch_older_users():
    async with aiosqlite.connect("users.db") as db:
        async with db.execute("SELECT * FROM users WHERE age > ?", (40,)) as cursor:
            older_users = await cursor.fetchall()
            print("\n[USERS OLDER THAN 40]")
            for user in older_users:
                print(user)
            return older_users

# Run both queries concurrently
async def fetch_concurrently():
    await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )

# Start the event loop
if __name__ == "__main__":
    asyncio.run(fetch_concurrently())
