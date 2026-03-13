import requests
import json
import re

# Direct URLs to the GitHub repository resources
ROADMAP_JSON_URL = "https://raw.githubusercontent.com/kamranahmedse/developer-roadmap/master/src/data/roadmaps/backend/backend.json"
GITHUB_API_CONTENT_URL = "https://api.github.com/repos/kamranahmedse/developer-roadmap/contents/src/data/roadmaps/backend/content"

def extract_links_from_md_text(content):
    """Parses markdown text to find [Title](URL) links."""
    links = re.findall(r'\[([^\]]+)\]\((https?://[^\)]+)\)', content)
    
    resources = []
    for title, url in links:
        resources.append({
            "title": title.strip(),
            "url": url.strip(),
            "type": "Video" if any(domain in url for domain in ["youtube.com", "youtu.be"]) else "Article"
        })
    return resources

def extract_all_nodes(data):
    """Recursively crawls the JSON to find all roadmap nodes."""
    nodes = []
    if isinstance(data, dict):
        if 'id' in data:
            title = data.get('title') or data.get('label')
            if 'data' in data and isinstance(data['data'], dict):
                title = title or data['data'].get('title') or data['data'].get('label')
            
            nodes.append({
                'id': data['id'],
                'title': title or "Unknown Topic"
            })
        for key, value in data.items():
            nodes.extend(extract_all_nodes(value))
    elif isinstance(data, list):
        for item in data:
            nodes.extend(extract_all_nodes(item))
    return nodes

def main():
    print("🚀 Fetching backend roadmap JSON...")
    json_response = requests.get(ROADMAP_JSON_URL)
    if json_response.status_code != 200:
        print("Error: Failed to fetch the roadmap JSON.")
        return
    roadmap_data = json_response.json()

    print("📁 Fetching file list from GitHub API...")
    # Using a custom User-Agent is good practice for the GitHub API
    headers = {"User-Agent": "Roadmap-Extractor-Script"}
    api_response = requests.get(GITHUB_API_CONTENT_URL, headers=headers)
    
    if api_response.status_code == 403:
        print("Error: GitHub API rate limit hit. Try again later or use the local clone method.")
        return
    elif api_response.status_code != 200:
        print(f"Error: Failed to fetch directory contents (Status {api_response.status_code}).")
        return

    # Create a mapping of filename -> raw download URL
    directory_files = api_response.json()
    file_map = {f['name']: f['download_url'] for f in directory_files if f['name'].endswith('.md')}

    # Find nodes and remove duplicates
    nodes = extract_all_nodes(roadmap_data)
    unique_nodes = {node['id']: node for node in nodes}.values()
    
    final_data = []
    print(f"🔍 Found {len(unique_nodes)} unique nodes. Downloading and parsing markdown files...")

    for node in unique_nodes:
        node_id = node['id']
        title = node['title']
        
        # Find the matching file in the API response
        target_url = None
        for filename, download_url in file_map.items():
            if node_id in filename:
                target_url = download_url
                break
        
        if target_url:
            # Download the raw markdown text
            md_response = requests.get(target_url)
            if md_response.status_code == 200:
                resources = extract_links_from_md_text(md_response.text)
                if resources:
                    final_data.append({
                        "topic": title,
                        "node_id": node_id,
                        "resources": resources
                    })
                    print(f"  [+] Extracted {len(resources)} links for '{title}'")

    output_file = 'github_extracted_backend_resources.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(final_data, f, indent=4)

    print(f"\n✅ Done! Extracted resources for {len(final_data)} topics.")
    print(f"Data saved to '{output_file}'.")

if __name__ == "__main__":
    main()
