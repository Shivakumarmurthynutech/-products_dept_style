import pandas as pd
from ..lib.constants import STG_MONGO_URL, PRD_MONGO_URL, DEV_MONGO_URL
from ..lib.dbutils import runQuery
from .mongo_queries import get_query
from ..lib.slackUtils import send_slack_msg
from ..lib.s3utils import writeToS3FromDataFrame
from ..lib.constants import SLACK_ALERT_TEMPLATE




slack_data = SLACK_ALERT_TEMPLATE.copy()




def products_dept_style():
    slack_data['report'] = 'products_dept_style'
    style = list(runQuery(get_query('styleAggregation'),DEV_MONGO_URL,'atomic_pim','productvariants'))
    stylelist = []
    for styleinfo in style:
        for stl in styleinfo ['style']:
            styledict = dict()
            styledict['ProductId'] = styleinfo['_id']
            styledict['Style'] = stl
            styledict['Dept'] = styleinfo ['dept'][0]
            stylelist.append(styledict)
        report = pd.DataFrame(stylelist)
        if writeToS3FromDataFrame(report):
            slack_data['filename'] = 'productstyle'
            send_slack_msg(**slack_data)

















