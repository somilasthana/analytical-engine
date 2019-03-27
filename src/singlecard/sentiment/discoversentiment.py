

class DiscoverSentiment:

    def __init__(self, response_change, response_type):
        self.response_change = response_change
        self.response_type = response_type

        if '_' not in self.response_type:
            raise Exception("Response given {} is not in proper format".format(self.response_type))
        self.set_sentiment_normal()

    @property
    def sentiment(self): return self.response_sentiment

    @property
    def adjective(self): return self.sentiment_adjective

    @property
    def adverb(self): return self.sentiment_adverb

    @property
    def change_verb(self): return self.response_change_verb

    @property
    def template_sentiment(self):
        response_template_sentiment =  self.response_sentiment + "-" + self.response_change_verb if (self.response_type == 'other_key' or
                                                                             self.response_type == 'response_neutral') \
            else self.response_sentiment + "-" + self.response_type.split('_')[1]
        return response_template_sentiment

    def set_sentiment_normal(self):
        """
        Set the sentiment when the response is normal (revenue increasing from 100 to 500)
        :return:
        """
        if self.response_change < 0 and self.response_type == 'response_gain':
            self.response_sentiment = 'negative'
            self.sentiment_adjective = "disappointing"
            self.sentiment_adverb = "disappointingly"
            self.response_change_verb = "dropped"
        elif self.response_change < 0 and self.response_type == 'response_loss':
            self.response_sentiment = 'positive'
            self.sentiment_adjective = "pleasing"
            self.sentiment_adverb = "pleasingly"
            self.response_change_verb = "dropped"
        elif self.response_change > 0 and self.response_type == 'response_gain':
            self.response_sentiment = 'positive'
            self.sentiment_adjective = "pleasing"
            self.sentiment_adverb = "pleasingly"
            self.response_change_verb = "climbed"
        elif self.response_change > 0 and self.response_type == 'response_loss':
            self.response_sentiment = 'negative'
            self.sentiment_adjective = "disappointing"
            self.sentiment_adverb = "disappointingly"
            self.response_change_verb = "climbed"
        elif self.response_change > 0 and (self.response_type == 'other_key' or
                                                   self.response_type == 'response_neutral'):
            self.response_sentiment = 'neutral'
            self.sentiment_adjective = ""
            self.sentiment_adverb = ""
            self.response_change_verb = "climbed"
        elif self.response_change < 0 and (self.response_type == 'other_key' or
                                                   self.response_type == 'response_neutral'):
            self.response_sentiment = 'neutral'
            self.sentiment_adjective = ""
            self.sentiment_adverb = ""
            self.response_change_verb = "dropped"
