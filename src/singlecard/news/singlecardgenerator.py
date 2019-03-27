from models.newsroom import Newsroom
from time import time


class SingleCardGenerator:

    def getNewsObject(self, headline, chart_params, response_name, response_value, response_sentiment,
                      diff_abs, calculation_type, group_id, dataset_id, newsgroup_hash, config_id,
                      period_name_value, period_name = "monthly"):

        newsroom_obj = Newsroom(
            news_text="",
            news_text_l1="",
            news_text_l2="",
            news_text_l3="",
            headline=headline,
            subheadline="",
            chart_params=str(chart_params),
            news_type="single-card",
            response=response_name,
            response_value=response_value,
            factor_name_l1="",
            factor_value_l1="",
            factor_name_l3="",
            factor_value_l3="",
            sentiment=response_sentiment,
            tags="",
            response_change=diff_abs,
            calculation_type=calculation_type,
            news_score=0.00293,
            group_ID=group_id,
            user_ID=None,
            dataset_info_ID=dataset_id,
            newsgroup_hash=newsgroup_hash,
            news_date=int(round(time())),
            anna_question="",
            current=1,
            config_ID=config_id,
            period_name=period_name,
            period_name_value=period_name_value,
            other_key_name="",
            response_pct_change=0.0
        )

        newsroom_obj.generate_uuid()

        return newsroom_obj