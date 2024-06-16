# here I'm just playing with some queries. If you want to try your,
# just replace the value of the `PINOT_QUERY` variable below

import time
from pinotdb import connect

conn = connect(host='localhost', port=8099, path='/query/sql', scheme='http')
curs = conn.cursor()

PINOT_QUERY = """
    SELECT
        COUNT(*) as processing_time_converted
    FROM
    sch_output_bytewax_enriched_rides_events
    WHERE
        DATETIMECONVERT(processing_time, '1:MILLISECONDS:SIMPLE_DATE_FORMAT:yyyy-MM-dd HH:mm:ss.SSSSSS', '1:MILLISECONDS:EPOCH', '1:MILLISECONDS') >= ago('PT1S')
"""

while True:
    curs.execute(PINOT_QUERY)
    for row in curs:
        print('processed in the last second: ', row[0])
    
    time.sleep(1)