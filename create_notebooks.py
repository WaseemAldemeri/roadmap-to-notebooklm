import json
import os
import asyncio
from notebooklm import NotebookLMClient

INPUT_FILE = 'github_extracted_backend_resources.json'
MD_FOLDER = 'Backend_Context_Files'

async def main():
    if not os.path.exists(INPUT_FILE):
        print(f"Error: Could not find {INPUT_FILE}")
        return

    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)

    os.makedirs(MD_FOLDER, exist_ok=True)

    print(f"🚀 Preparing to create {len(data)} Notebooks. Connecting to NotebookLM...")
    
    # Initialize using your saved login session
    async with await NotebookLMClient.from_storage() as client:
        
        for index, item in enumerate(data):
            topic = item['topic']
            resources = item['resources']
            
            notebook_title = f"Roadmap.sh Backend: {topic}"
            
            print(f"\n[{index + 1}/{len(data)}] 📁 Creating Notebook: '{notebook_title}'")
            
            try:
                # 1. Create the Notebook
                nb = await client.notebooks.create(notebook_title)
                print(f"  └── Created successfully (ID: {nb.id})")
                
                # 2. Create the enriched local Markdown context file
                safe_title = topic.replace('/', '-').replace(' ', '_')
                md_path = os.path.join(MD_FOLDER, f"{safe_title}.md")
                
                # --- NEW ENRICHED MARKDOWN CONTEXT ---
                md_content = f"""# Backend Developer Roadmap: {topic}

**Source:** [roadmap.sh/backend](https://roadmap.sh/backend)

## Context
This notebook covers the fundamental concepts, articles, and video tutorials for mastering **{topic}** as part of a complete backend engineering curriculum. 

The resources ingested into this notebook are community-curated materials designed to explain the core mechanics, practical applications, and industry standards related to this specific node on the roadmap.
"""
                with open(md_path, 'w', encoding='utf-8') as f:
                    f.write(md_content)

                # 3. Upload the Context Markdown File
                print(f"  └── Uploading context file...")
                await client.sources.add_file(nb.id, md_path)

                # 4. Upload all the URLs explicitly
                for res in resources:
                    url = res['url']
                    print(f"  └── Adding URL: {url} ...")
                    try:
                        # wait=True ensures NotebookLM fully reads the webpage before moving on
                        await client.sources.add_url(nb.id, url, wait=True)
                        print("      ✅ Successfully ingested.")
                    except Exception as url_error:
                        print(f"      ❌ Failed to ingest URL. Error: {url_error}")
                
                print(f"✅ Finished provisioning '{notebook_title}'!")

                # 5. Rate Limit Protection
                if index < len(data) - 1:
                    print("  ⏳ Pausing for 5 seconds to prevent rate limiting...")
                    await asyncio.sleep(5)

            except Exception as e:
                print(f"❌ Error creating notebook for {topic}: {e}")

    print("\n🎉 All done! Your backend roadmap is fully loaded into NotebookLM.")

if __name__ == "__main__":
    asyncio.run(main())
