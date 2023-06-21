from slack_sdk import WebClient

import argparse
import logging
import os
import pprint
import sys
import tiktoken

CONVO_FILENAME = "eng_conversation_history.txt"
CHANNEL_ID = "CC4N13E93"

logging.basicConfig(level=logging.DEBUG)

pp = pprint.PrettyPrinter(indent=4)


def read_file_into_list(file_name):
    with open(file_name, 'r') as f:
        lines = f.readlines()
    non_empty_lines = [line.strip() for line in lines if line.strip()]
    return non_empty_lines


def number_of_tokens_from_convos(file_name):
    encoding = tiktoken.encoding_for_model('gpt-3.5-turbo')

    messages = read_file_into_list(file_name)

    tokens_lists = encoding.encode_batch(messages)

    total_tokens = sum(len(tokens) for tokens in tokens_lists)

    return total_tokens


def main(file_name, count_only):
    logger = logging.getLogger(__name__)

    if not count_only:
        try:
            client = WebClient(token=os.environ["SLACK_BOT_TOKEN"])

            next_cursor = None
            message_count = 0

            with open(file_name, "w") as f:
                while True:
                    result = client.conversations_history(
                        channel=CHANNEL_ID, cursor=next_cursor)
                    conversation_history = result["messages"]

                    for message in conversation_history:
                        if "text" in message:
                            f.write(message["text"] + ' ')
                            message_count += 1

                    next_cursor = result.get(
                        "response_metadata", {}).get("next_cursor")

                    if not next_cursor:
                        break

            logger.info("{} messages found in {}".format(
                message_count, CHANNEL_ID))

        except Exception as e:
            print(e)

    logger.info("Tokenizing & counting tokens...")

    num_tokens = number_of_tokens_from_convos(file_name)

    logger.info("Number of tokens: {}".format(num_tokens))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "filename", help="The filename to store conversation history")
    parser.add_argument(
        "-c", "--count", help="Count tokens only, does not download conversation history", action="store_true")
    args = parser.parse_args()

    main(args.filename, args.count)
