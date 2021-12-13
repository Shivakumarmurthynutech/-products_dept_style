import pandas as pd
from ..lib.constants import STG_MONGO_URL, PRD_MONGO_URL, DEV_MONGO_URL
from ..lib.dbutils import runQuery
from .mongo_queries import get_query
from ..lib.s3utils import writeToS3FromDataFrame
from ..lib.constants import SLACK_ALERT_TEMPLATE
from ..lib.slackUtils import  send_slack_msg
from ..lib.constants import AWS_S3_BUCKET
from ..lib.timeutils import getDateStr


slack_data = SLACK_ALERT_TEMPLATE.copy()

def products_dept_style():
    try:
        slack_data['report'] = 'Products_dept_style'
        style = list(runQuery(get_query('styleAggregation'),DEV_MONGO_URL,'atomic_pim','productvariants'))
        stylelist = []
        if style is not None:
            for styleinfo in style:
                if styleinfo is not None:
                    for stl in styleinfo['style']:
                        for dept in styleinfo['dept']:
                            styledict = dict()
                            styledict['ProductId'] = styleinfo['_id']
                            styledict['Style'] = stl
                            styledict['Dept'] = dept
                            stylelist.append(styledict)
            report = pd.DataFrame(stylelist)
            date = getDateStr()
            if writeToS3FromDataFrame(report) == 200:
               slack_data['filename'] = f"products_dept_style_{date}.csv"
               slack_data['bucket'] = AWS_S3_BUCKET
               slack_data['total'] = len(report)
               send_slack_msg(**slack_data)
    except Exception as err:
        print(f"Error in fetch-operations: {err}")
        slack_data['alert_status'] = 'alert'
        slack_data['error'] = err
        send_slack_msg(**slack_data)























