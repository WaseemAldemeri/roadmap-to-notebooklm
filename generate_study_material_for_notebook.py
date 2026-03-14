import asyncio
from InquirerPy import inquirer
from notebooklm import NotebookLMClient
from config import STUDY_MATERIALS

async def main():
    print("🚀 Connecting to NotebookLM...")
    
    async with await NotebookLMClient.from_storage() as client:
        # 1. Fetch your existing Notebooks
        notebooks = await client.notebooks.list()
        
        if not notebooks:
            print("❌ No notebooks found in your account.")
            return

        # 2. Interactive Fuzzy Search: Choose the Notebook
        nb_choices = [{"name": nb.title, "value": nb} for nb in notebooks]
        
        target_nb = await inquirer.fuzzy(
            message="📚 Search and select a Notebook to study (type to fuzzy search):",
            choices=nb_choices,
            max_height="70%"  # Gives the list plenty of room on your terminal screen
        ).execute_async()

        if not target_nb:
            print("Canceled.")
            return

        # 3. Interactive Multi-Select: Choose what to generate
        # InquirerPy uses 'enabled' instead of 'checked' for default selections
        material_choices = [
            {"name": config["name"], "value": key, "enabled": True} 
            for key, config in STUDY_MATERIALS.items()
        ]
        
        selected_keys = await inquirer.checkbox(
            message="✨ Select the materials to generate (Space to toggle, Enter to confirm):",
            choices=material_choices
        ).execute_async()

        if not selected_keys:
            print("No materials selected. Exiting.")
            return

        print(f"\n🎯 Target Locked: '{target_nb.title}'")
        print("⚡ Firing generation requests to Google's servers...\n")

        # 4. Dynamically trigger the specific methods
        for key in selected_keys:
            config = STUDY_MATERIALS[key]
            method_name = config["method"]
            kwargs = config["kwargs"]
            
            try:
                print(f"  [+] Requesting {config['name']}...")
                
                # Retrieve the specific function
                target_function = getattr(client.artifacts, method_name)
                
                # Execute it using our strict Enums and instructions
                await target_function(notebook_id=target_nb.id, **kwargs)
                print("      ✅ Job queued successfully.")
                
                # A 2-second pause to avoid tripping API rate limits
                await asyncio.sleep(2)
                
            except Exception as e:
                print(f"      ❌ Failed to queue {config['name']}: {e}")

        print("\n🎉 All selected jobs dispatched! They are now rendering in the background.")

if __name__ == "__main__":
    asyncio.run(main())