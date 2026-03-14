# ============================================================
# ROADMAP CONFIGURATION — edit this to use a different roadmap
# ============================================================

ROADMAP_NAME = "backend"           # slug used for file/folder names
ROADMAP_DISPLAY_NAME = "Backend"   # shown in notebook titles and context files
ROADMAP_URL = "https://roadmap.sh/backend"

# GitHub source URLs — change both when switching roadmaps
# Pattern: .../roadmaps/<slug>/<slug>.json  and  .../roadmaps/<slug>/content
ROADMAP_JSON_URL = "https://raw.githubusercontent.com/kamranahmedse/developer-roadmap/master/src/data/roadmaps/backend/backend.json"
GITHUB_API_CONTENT_URL = "https://api.github.com/repos/kamranahmedse/developer-roadmap/contents/src/data/roadmaps/backend/content"

# Derived output paths (no need to change these)
RESOURCES_FILE = f"{ROADMAP_NAME}_resources.json"
CONTEXT_FILES_FOLDER = f"{ROADMAP_DISPLAY_NAME}_Context_Files"
NOTEBOOK_PREFIX = f"Roadmap.sh {ROADMAP_DISPLAY_NAME}"

# ============================================================
# STUDY MATERIAL PROMPTS — customise tone/audience if needed
# ============================================================
from notebooklm.rpc.types import AudioLength, AudioFormat

STUDY_MATERIALS = {
    "audio": {
        "name": "Podcast (Audio Overview)",
        "method": "generate_audio",
        "kwargs": {
            "audio_length": AudioLength.LONG,
            "audio_format": AudioFormat.DEEP_DIVE,
            "instructions": "You are two experienced engineers hosting a podcast. Your audience consists of working junior software developers who know how to code, but are new to the specific technology you are discussing today. Assume they have no prior knowledge of this specific tool or concept. Start by clearly explaining what it is and exactly why the industry uses it, bridging the gap between writing basic code and building scalable systems. Once the foundation is set, dive into how it is actually used in a modern production environment. Discuss real-world use cases, engineering trade-offs, and common pitfalls. Keep the banter engaging, encouraging, and highly educational."
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
