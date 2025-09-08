# See dhis2_client documentation for more details:
import argparse, asyncio
from dhis2_client import DHIS2AsyncClient, Settings

def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--base-url", required=True)
    p.add_argument("--username", required=True)
    p.add_argument("--password", required=True)
    return p.parse_args()

async def main():
    args = parse_args()
    settings = Settings(base_url=args.base_url, username=args.username, password=args.password)
    async with DHIS2AsyncClient.from_settings(settings) as client:
        info = await client.get_system_info()
        print("DHIS2:", info.version, info.contextPath)

if __name__ == "__main__":
    asyncio.run(main())
