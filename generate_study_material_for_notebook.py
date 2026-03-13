import asyncio
from InquirerPy import inquirer
from notebooklm import NotebookLMClient
from notebooklm.rpc.types import AudioLength, AudioFormat

# --- YOUR PREDEFINED PROMPTS & SETTINGS ---
STUDY_MATERIALS = {
    "audio": {
        "name": "Podcast (Audio Overview)",
        "method": "generate_audio",
        "kwargs": {
            "audio_length": AudioLength.LONG, 
            "audio_format": AudioFormat.DEEP_DIVE,
            "instructions": "You are two experienced backend engineers hosting a podcast. Your audience consists of working junior software developers who know how to code, but are new to the specific technology you are discussing today. Assume they have no prior knowledge of this specific tool or concept. Start by clearly explaining what it is and exactly why the industry uses it, bridging the gap between writing basic code and building scalable systems. Once the foundation is set, dive into how it is actually used in a modern production environment. Discuss real-world use cases, engineering trade-offs, and common pitfalls. Keep the banter engaging, encouraging, and highly educational."
        }
    },
    "slide-deck": {
        "name": "Slide Deck",
        "method": "generate_slide_deck",
        "kwargs": {
            "instructions": "Act as a Senior Engineer creating a technical presentation for junior developers who know how to code but are completely new to this technology. Start with a clear 'What is this and why do we use it?' summary. Follow with slides detailing its core architecture and how it bridges the gap to building scalable systems. Include dedicated slides for real-world production use cases, major engineering trade-offs, and the most common pitfalls developers make when implementing it. Keep the bullet points concise, technical, and focused on practical engineering context."
        }
    },
    "flashcards": {
        "name": "Flashcards",
        "method": "generate_flashcards",
        "kwargs": {
            "instructions": "Generate a set of flashcards tailored for a junior developer studying to understand this technology from the ground up. The cards should go beyond basic definitions. Include questions that test comprehension of why this tool is used, how it scales, its primary engineering trade-offs, and common production pitfalls. Keep the answers clear, technical, and focused on real-world engineering."
        }
    },
    "quiz": {
        "name": "Quiz",
        "method": "generate_quiz",
        "kwargs": {
            "instructions": "Create a quiz for a working junior developer who is learning this technology. Do not just test basic trivia or syntax. Structure the questions around practical engineering scenarios, architecture choices, scaling trade-offs, and real-world production pitfalls. Start with foundational concepts to test their understanding of what the tool is, then escalate to questions about its role in distributed systems. Provide highly detailed explanations for the correct answers that reinforce the engineering context."
        }
    },
    "video": {
        "name": "Video Overview",
        "method": "generate_video",
        "kwargs": {
            "instructions": "Create a video overview designed for working junior developers encountering this technology for the first time. Assume they know basic programming but have no prior knowledge of this specific tool. The narrative should start by demystifying what the tool is and the exact problem it solves in the industry. Transition into a practical breakdown of how it operates in a production environment to handle scale. Highlight real-world trade-offs and common implementation pitfalls. Keep the tone encouraging, highly educational, and focused on bridging the gap to advanced system design."
        }
    }
}

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