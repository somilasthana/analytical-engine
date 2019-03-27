from models.newsroom_headline import Newsroom_headline
from utils.db_utils import create_db_session
import math
import random


class SingleCardHeadline:

    def __init__(self, sentiment, response_name, calculation_type, diff_pct):
        self.sentiment = sentiment
        self.response_name = response_name
        self.calculation_type = calculation_type
        self.diff_pct = diff_pct

        self.transform = {"sum": "total", "mean": "average"}

    @staticmethod
    def to_percent(num_value):
        if num_value % 1 == 0:
            return "{0:,.0f}".format(num_value) + "%"
        elif num_value >= 0.01:
            return "{0:,.2f}".format(num_value) + "%"
        elif num_value < 0.01:
            return "less than 0.01%"

    def make_headline(self):

        def get_random_title_template(sentiment="", style="long"):
            """
            Read the title templates from MySQL and randomly pick one
            :return: title template picked
            """

            session = create_db_session()
            news_title = session.query(Newsroom_headline). \
                filter_by(sentiment=sentiment, style=style)

            record = news_title[math.floor(random.random() * news_title.count())]
            session.close()
            return record

        insight_params = {
            "<response name>": self.response_name,
            "<percent difference>": self.to_percent(abs(self.diff_pct)),
            "<calc value>": self.transform[self.calculation_type] if self.calculation_type in self.transform else "unknown"
        }

        news_headline = get_random_title_template(self.sentiment)
        news_headline_text = news_headline.headline_text

        for tag, value in insight_params.items():
            news_headline_text = news_headline_text.replace(str(tag), str(value))

        return news_headline_text
