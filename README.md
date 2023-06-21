Count the tokens after using the `tiktoken` BPE tokenizer on conversations in a Slack channel.

This does the following:
- pulls down all conversations from a Slack channel
- batch encodes them as BPE for OpenAI models (will use for embeddings) using `tiktoken`
- counts the number of tokens

### Why care about tokens?
Well, when you get an [embedding](https://platform.openai.com/docs/guides/embeddings/what-are-embeddings) from OpenAI you need to know the number of tokens you will be sending because:
- there are a max number of tokens you can send per request
- there is a [cost](https://openai.com/pricing) per 1k tokens

You can run this to get the total number of tokens with an existing conversation list or without:

```bash
# Without
SLACK_BOT_TOKEN=xxxxx python main.py

# With
python main.py -c existing_file.name
```

## Requirements
Obviously you need a Slack app w/ a token. Use the Slack documentation to sort that out (it's fairly straightforward).
A channel id containing the conversation history you wish to pull down.
