from singlecard.sentiment.discoversentiment import DiscoverSentiment


def do_find_sentiment():
    print("==============do_find_sentiment=================")

    try:
        sentiment = DiscoverSentiment(response_change=0, response_type="")
    except Exception as e:
        assert str(e)  == "Response given  is not in proper format"

    sentiment = DiscoverSentiment(response_change=1, response_type="response_gain")
    assert sentiment.sentiment == "positive"
    assert sentiment.template_sentiment == "positive-gain"


if __name__ == '__main__':
    do_find_sentiment()