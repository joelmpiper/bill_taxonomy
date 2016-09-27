
def formatted_query(query_results, col):

    bills = []
    for i in range(0, query_results.shape[0]):
        bills.append(dict(bill_num=query_results.iloc[i]['bill_num'],
                          bill_name=query_results.iloc[i]['bill_name'],
                          score=query_results.iloc[i][col]))
    seen = set()
    uniq_bills = dict()
    for bill in bills:
        if bill['bill_name'] not in seen:
            uniq_bills[bill['bill_name']] = dict(bill_num=[bill['bill_num']],
                                                 bill_name=bill['bill_name'],
                                                 score=bill['score'])
            seen.add(bill['bill_name'])
        else:
            b1 = uniq_bills[bill['bill_name']]
            b1['score'] = (b1['score'] * len(b1['bill_num']) +
                           bill['score']) / (len(b1['bill_num']) + 1)
            b1['bill_num'].append(bill['bill_num'])

    sorted_bills = sorted(uniq_bills.values(), key=lambda a: -a['score'])
    for bill in sorted_bills:
        bill['score'] = "{0:2.2g}".format(bill['score'])
        bill['bill_num'] = ", ".join(bill['bill_num'])
    return sorted_bills

def create_histogram(query_frame):
    return 0
