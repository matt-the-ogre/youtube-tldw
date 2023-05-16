import argparse
from urllib.parse import parse_qs, urlparse

import openai
from youtube_transcript_api import YouTubeTranscriptApi


def summarize_video(url, model, debug):
    video_id = parse_qs(urlparse(url).query).get('v')[0]
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    chunk_size_in_lines = 400

    for i in range(0, len(transcript), chunk_size_in_lines):
        context = "\n".join([t["text"] for t in transcript[i:i+chunk_size_in_lines]])
        prompt = f"Summarize this youtube video section's transcript with bullet points:\n---\n{context}"
        summary = openai.ChatCompletion.create(
            model=model,
            messages=[{"role": "system", "content": "You are a helpful assistant."},
                      {"role": "user", "content": prompt}]
        ).choices[0].message["content"]
        print(summary)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Summarize YouTube video transcripts.")
    parser.add_argument("url", help="URL of the YouTube video to summarize.")
    parser.add_argument("model", help="GPT Model name", default="gpt-3.5-turbo", nargs="?")
    # parser.add_argument("model", help="GPT Model name", default="gpt-4-32k", nargs="?")
    parser.add_argument("debug", help="Debug Boolean flag", default="false", nargs="?")
    args = parser.parse_args()

    summarize_video(args.url, args.model, args.debug)
