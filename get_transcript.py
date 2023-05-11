import argparse
import re

from urllib.parse import parse_qs, urlparse

from youtube_transcript_api import YouTubeTranscriptApi

def get_transcript(url):
    # get the video ID from the URL
    video_id = parse_qs(urlparse(url).query).get('v')[0]

    # get the transcript of the video
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    print(type(transcript))
    # transcript = [str(item) for item in transcript] # convert all items to strings
    # print(type(transcript))
    # convert the list of strings to one long string

    transcript_as_string = ""
    for entry in transcript:
        transcript_as_string += entry['text']

    # transcript_as_string = '\n'.join(longstring)

    # make a regular expression pattern to remove line endings from all lines that don't start with ">>"
    pattern = re.compile(r'(?<!^>>)(\r?\n)', re.MULTILINE)

    # run the pattern on the transcript
    result = pattern.sub('', transcript_as_string)

    # now add newlines before ">>"
    pattern = re.compile(r'(>>)')
    result = pattern.sub('\n\\1',result)

    # now add newlines before "["
    pattern = re.compile(r'(\[)')
    result = pattern.sub('\n\\1',result)

    # and after "]."
    pattern = re.compile(r'(\].)')
    result = pattern.sub('\\1\n',result)

    return result, video_id

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch YouTube video transcripts.")
    parser.add_argument("url", help="URL of the YouTube video.")
    args = parser.parse_args()

    transcript, video_id = get_transcript(args.url)
    
    with open(f"{video_id}.txt", 'w') as f:
        # for entry in transcript:
            # print(entry['text'], file=f)
        print(transcript, file=f)
