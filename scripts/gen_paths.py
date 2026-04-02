import random
import os
import sys
import argparse

def make_generators():
    fs_roots = [
        "/home", "/var", "/usr", "/opt", "/srv", "/etc", "/data", "/mnt",
        "/run", "/media", "/storage", "/backup", "/archive",
        "/app", "/deploy", "/services", "/infrastructure",
    ]
    fs_segs = [
        "config", "nginx", "apache", "redis", "postgres", "mongodb", "kafka",
        "logs", "access", "error", "audit", "debug", "trace", "metrics",
        "data", "cache", "sessions", "uploads", "downloads", "exports", "imports",
        "backup", "archive", "snapshots", "checkpoints", "migrations",
        "src", "lib", "bin", "include", "share", "doc",
        "api", "v1", "v2", "v3", "internal", "external", "public", "private",
        "auth", "users", "accounts", "profiles", "settings", "preferences",
        "products", "catalog", "inventory", "orders", "payments", "shipping",
        "reports", "analytics", "dashboards", "charts", "events", "streams",
        "queues", "topics", "subscriptions", "notifications", "alerts",
        "workers", "schedulers", "jobs", "tasks", "pipelines", "workflows",
        "primary", "replica", "master", "leader", "follower",
        "us-east-1", "eu-west-2", "ap-southeast-1", "us-west-2", "ca-central-1",
        "production", "staging", "development", "testing", "qa", "canary",
        "cluster-01", "cluster-02", "cluster-03", "node-a", "node-b", "node-c",
        "2024", "2025", "01", "02", "03", "04", "05", "06",
    ]
    file_names = [
        "config.yaml", "config.json", "settings.toml", "app.properties",
        "nginx.conf", "redis.conf", "prometheus.yml",
        "access.log", "error.log", "audit.log", "app.log",
        "backup.tar.gz", "dump.sql.gz", "snapshot.rdb", "data.parquet",
        "schema.json", "manifest.json", "Makefile", "Dockerfile",
        "docker-compose.yml", "main.py", "app.rs", "server.go", "handler.cpp",
        "index.html", "bundle.js", "ca-bundle.crt", "server.pem",
        "item-12345", "record-98765", "doc-abcdef",
    ]

    url_prefixes = [
        "api", "v1", "v2", "v3", "rest", "graphql",
        "internal", "external", "public", "admin", "dashboard",
        "search", "browse", "explore", "discover", "feed",
        "account", "profile", "settings", "notifications",
        "checkout", "cart", "wishlist", "orders", "invoice",
        "docs", "help", "support", "status", "health",
    ]
    url_resources = [
        "users", "accounts", "sessions", "tokens", "permissions", "roles",
        "products", "categories", "collections", "variants", "attributes", "tags",
        "orders", "items", "shipments", "tracking", "returns", "refunds",
        "reports", "analytics", "metrics", "events", "logs", "traces",
        "projects", "workspaces", "organizations", "teams", "members", "invites",
        "pipelines", "stages", "runs", "artifacts", "deployments", "releases",
        "repositories", "branches", "commits", "pull-requests", "issues", "labels",
        "clusters", "nodes", "pods", "services", "endpoints", "namespaces",
        "topics", "partitions", "consumer-groups", "offsets", "schemas",
    ]
    url_actions = [
        "list", "search", "filter", "export", "import", "sync",
        "batch", "bulk", "stream", "subscribe", "publish",
        "validate", "transform", "aggregate", "summarize",
    ]

    category_roots = [
        "electronics/computers", "electronics/phones", "electronics/tablets",
        "electronics/cameras", "electronics/audio", "electronics/gaming",
        "electronics/wearables", "electronics/networking", "electronics/storage",
        "clothing/men", "clothing/women", "clothing/kids", "clothing/unisex",
        "clothing/sportswear", "clothing/formal", "clothing/casual",
        "sports/fitness", "sports/outdoor", "sports/team", "sports/water",
        "sports/winter", "sports/cycling", "sports/running", "sports/yoga",
        "books/programming", "books/science", "books/history", "books/fiction",
        "books/business", "books/self-help", "books/arts", "books/cooking",
        "food/organic", "food/beverages", "food/snacks", "food/dairy",
        "food/bakery", "food/meat", "food/seafood", "food/produce",
        "home/furniture", "home/kitchen", "home/bedding", "home/decor",
        "home/garden", "home/tools", "home/appliances", "home/lighting",
        "health/supplements", "health/equipment", "health/personal-care",
        "health/medical", "health/beauty", "health/wellness",
        "automotive/parts", "automotive/tools", "automotive/accessories",
        "automotive/electronics", "automotive/tires",
        "travel/flights", "travel/hotels", "travel/packages", "travel/cruises",
        "travel/rental-cars", "travel/activities", "travel/insurance",
    ]
    category_sub = [
        "laptops/gaming/high-end", "laptops/business/ultrabook", "laptops/budget/student",
        "smartphones/android/flagship", "smartphones/ios/premium",
        "shirts/formal/slim-fit", "shirts/casual/oversized",
        "shoes/running/trail", "shoes/basketball/indoor", "shoes/casual/sneakers",
        "jackets/winter/down-filled", "jackets/rain/waterproof",
        "supplements/protein/whey", "supplements/vitamins/d3",
        "cameras/dslr/full-frame", "cameras/mirrorless/aps-c",
        "headphones/over-ear/wireless", "headphones/in-ear/noise-canceling",
        "monitors/gaming/144hz", "monitors/professional/4k",
        "keyboards/mechanical/clicky", "keyboards/ergonomic/split",
        "chairs/gaming/ergonomic", "chairs/office/executive",
        "desks/standing/electric", "desks/gaming/l-shaped",
    ]
    category_extras = [
        "new-arrivals", "best-sellers", "clearance", "sale", "featured",
        "premium", "budget", "eco-friendly", "limited-edition", "bundle",
        "brand-a", "brand-b", "brand-c", "brand-xyz",
        "size-s", "size-m", "size-l", "size-xl", "size-xxl",
        "color-red", "color-blue", "color-black", "color-white",
        "in-stock", "pre-order", "discontinued", "refurbished",
    ]

    def rand_fs_path():
        root = random.choice(fs_roots)
        depth = random.randint(4, 9)
        segs = random.choices(fs_segs, k=depth)
        if random.random() < 0.5:
            segs.append(random.choice(file_names))
        return root + "/" + "/".join(segs)

    def rand_url_path():
        parts = [random.choice(url_prefixes)]
        depth = random.randint(3, 8)
        for _ in range(depth):
            r = random.random()
            if r < 0.6:
                parts.append(random.choice(url_resources))
            elif r < 0.8:
                parts.append(str(random.randint(100000, 9999999)))
            else:
                parts.append(random.choice(url_actions))
        return "/" + "/".join(parts)

    def rand_category():
        base = random.choice(category_roots + category_sub)
        parts = base.split("/")
        for _ in range(random.randint(0, 3)):
            parts.append(random.choice(category_extras))
        return "/" + "/".join(parts)

    return [
        (rand_fs_path,   0.40),
        (rand_url_path,  0.35),
        (rand_category,  0.25),
    ]


def main():
    parser = argparse.ArgumentParser(description="Generate path hierarchy dataset")
    parser.add_argument("-n", "--count", type=int, default=100_000,
                        help="Number of lines to generate (default: 100000)")
    parser.add_argument("-o", "--output", default="data/paths.txt",
                        help="Output file (default: data/paths.txt)")
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    random.seed(args.seed)
    generators = make_generators()

    os.makedirs(os.path.dirname(os.path.abspath(args.output)), exist_ok=True)

    lines = []
    for _ in range(args.count):
        r = random.random()
        acc = 0.0
        for gen, prob in generators:
            acc += prob
            if r < acc:
                lines.append(gen())
                break

    with open(args.output, "w") as f:
        for line in lines:
            f.write(line + "\n")

    lengths = [len(l) for l in lines]
    size_mb = os.path.getsize(args.output) / 1024 / 1024
    print(f"Written {len(lines):,} lines to {args.output}")
    print(f"File size : {size_mb:.2f} MB")
    print(f"Avg length: {sum(lengths)/len(lengths):.1f}  min: {min(lengths)}  max: {max(lengths)}")
    assert all(l.startswith("/") for l in lines), "BUG: non-slash lines found"
    print("All lines start with '/', compatible with Tantivy FacetTokenizer")


if __name__ == "__main__":
    main()
