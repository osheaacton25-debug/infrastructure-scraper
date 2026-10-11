import asyncio
import httpx

async def check_domain(client, domain):
    domain = domain.strip()
    if not domain:
        return None
    url = f"https://{domain}"
    try:
        response = await client.get(url, timeout=5.0, follow_redirects=True)
        if response.status_code in [403, 500, 502, 504]:
            return (domain, response.status_code)
    except Exception:
        return (domain, "DEAD/TIMEOUT")
    return None

async def main():
    with open("manchester_domains.txt", "r") as f:
        domains = f.readlines()

    async with httpx.AsyncClient() as client:
        tasks = [check_domain(client, d) for d in domains]
        results = await asyncio.gather(*tasks)
        broken = [r for r in results if r is not None]
        print("Infrastructure Errors Found:", broken)

if __name__ == "__main__":
    asyncio.run(main())
  
