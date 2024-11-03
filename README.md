# AI Voice Agent Worker

This repository contains a Dockerized setup for an AI voice agent worker written in Python. The voice agent is capable of making function calls and utilizes a vector database for context when available.

## Getting Started

### Prerequisites

Make sure you have the following installed:

- Docker
- Docker Compose (optional, if you use it in your setup)
- Livekit API_KEY, SECRET and URL (https://cloud.livekit.io)

### Setup Instructions

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/yourusername/your-repo-name.git
   cd your-repo-name

2. **Configure Environment Variables:**

    Copy the example environment file and rename it:
    
    `cp .env.example .env`

    Open the `.env` file and fill in the required variables based on the template provided.
    
3. **Install Dependencies:**

    Make sure to install the required Python packages from requirements.txt. You can do this by running:
    
    ```bash
    pip install -r requirements.txt
    
4. **Add Vector Database (Optional):**

    If you have a vector database with embeddings that you want to use as context, copy it to the `DB` folder in this repository. This will enable the voice agent to utilize the data.

5. **Run the Application:**

    You can start the application using the following command:

    ```bash
    python agent.py dev
    
### Frontend Interaction

To interact with the AI voice agent via a frontend, you can use:

- **LiveKit Agent Playground (Next.js Frontend)**: This can be set up locally to connect to your agent.
- **LiveKit Sandbox**: A cloud-based option that allows you to interact with the agent.

## Usage
Once the application is running, you can interact with the AI voice agent. The agent is designed to process voice commands and can make function calls based on user input.