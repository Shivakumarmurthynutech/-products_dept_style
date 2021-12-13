

def get_query(style):
    queries ={
        'styleAggregation':[
    {
        '$match': {
            'isActive': True,
            'isDisplay': True,
            'siteAwareAssets.0': {
                '$exists': True
            },
            'style': {
                '$exists': True
            }
        }
    }, {
        '$group': {
            '_id': '$parentProductId',
            'style': {
                '$addToSet': '$style'
            },
            'dept': {
                '$addToSet': '$dept'
            }
        }
    }
]
    }
    return queries.get('styleAggregation')