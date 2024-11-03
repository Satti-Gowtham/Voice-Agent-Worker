import logging, os
from livekit.agents import (
    AutoSubscribe,
    JobContext,
    JobProcess,
    WorkerOptions,
    cli,
    llm,
)
from livekit.agents.pipeline import VoicePipelineAgent
from livekit.plugins import openai, silero
from functions import AssistantFunctions

logger = logging.getLogger("Voice-agent")

def prewarm(proc: JobProcess):
    proc.userdata["vad"] = silero.VAD.load()

async def entrypoint(ctx: JobContext):
    initial_context = llm.ChatContext().append(
        role="system",
        text=(
            "You are a voice assistant designed specifically for tutoring. Your interaction with users will be entirely through voice. "
            "Use short and concise responses, avoiding any unpronounceable punctuation. "
            "You will utilize function calls to search the database only when absolutely necessary, particularly for medical topics. "
            "Since querying the database might take some time, feel free to use short fillers to maintain the flow of conversation. "
            "If you don't find relevant information, simply inform the user that you don't know. "
            "You must never provide false information and should treat users respectfully, adapting to their individual learning abilities."
        ),
    )

    logger.info(f"Connecting to room {ctx.room.name}")
    await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)

    participant = await ctx.wait_for_participant()
    logger.info(f"Starting voice assistant for participant {participant.identity}")
    function_context = AssistantFunctions()

    assistant = VoicePipelineAgent(
        vad=ctx.proc.userdata["vad"],
        stt=openai.STT.with_groq(api_key=os.getenv("GROQ_API_KEY")),
        llm=openai.LLM.with_groq(model="llama-3.2-90b-text-preview", api_key=os.getenv("GROQ_API_KEY")),
        tts=openai.TTS(),
        chat_ctx=initial_context,
        fnc_ctx=function_context,
    )

    assistant.start(ctx.room, participant)

if __name__ == "__main__":
    cli.run_app(
        WorkerOptions(
            entrypoint_fnc=entrypoint,
            prewarm_fnc=prewarm
        ),
    )

