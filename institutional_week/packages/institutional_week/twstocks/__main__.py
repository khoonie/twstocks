def main(args):
    # Version 1.0
    # Nov 5, 2024
    # Extracts from Yahoo website the institutional buys and sells of TW stocks
    # Fields include "名次","股名/股號","股價","漲跌","買進張數","賣出張數","買超張數","成交張數","外資持股張數","外資持股比率"

    from config import DB_USERNAME, DB_PASSWORD, DB_PORT, DB_URL
    from bs4 import BeautifulSoup
    import csv
    import urllib.request
    import mysql.connector

    url = "https://tw.stock.yahoo.com/rank/foreign-investor-buy?exchange=TAI&period=week"

    r = urllib.request.Request(url)
    res = urllib.request.urlopen(r)
    soup = BeautifulSoup(res, features='lxml')

    table_rows = []

    rows = soup.findAll('li', class_="List(n)")

    iter = 0

    for r in rows:

        for next_tag in r.children:

            num = next_tag.select('span.Fz\(24px\).Fw\(b\)')[0].get_text() # number
            name = next_tag.select('div.Lh\(20px\).Fw\(600\)')[0].get_text() # name
            code = next_tag.select('span.Fz\(14px\).C\(\#979ba7\)')[0].get_text() #code
            # color indicating up (red) or down (green), and no change (black)
            if (0 < len(next_tag.select('span.Mend\(4px\).Bds\(s\)'))):
                color = next_tag.select('span.Mend\(4px\).Bds\(s\)')[0]['style']
                if 'border-color:transparent' in color:
                    txt_color = "red"
                else:
                    txt_color = 'green'
            else:
                txt_color = "black"

            price = next_tag.select('span.Jc\(fe\)')[0].get_text() #price
            updown = next_tag.select('span.Jc\(fe\)')[1].get_text() #up and down
            if txt_color =='green':
                updown = '-' + updown
            buy = next_tag.select('span.Jc\(fe\)')[2].get_text() #buy
            sell = next_tag.select('span.Jc\(fe\)')[3].get_text() #sell
            over = next_tag.select('span.Jc\(fe\)')[4].get_text() #over
            traded = next_tag.select('span.Jc\(fe\)')[5].get_text() #traded
            hold = next_tag.select('span.Jc\(fe\)')[6].get_text() #hold
            ratio = next_tag.select('span.Jc\(fe\)')[7].get_text()  #ratio

          #  print('#:{} name:{} code:{} color:{} price:{} updown:{} buy:{} sell:{} over:{} traded:{} hold:{} ratio:{}'.format(
          #          num, name, code, txt_color, price, updown, buy ,sell, over, traded, hold, ratio
          #          )
          #      )
            table_rows.append(
                (int(num), 
                name, 
                code,
                float(price.replace(',' , '')),
                float(updown.replace(',' , '')),
                float(buy.replace(',' , '')),
                float(sell.replace(',' , '')),
                int(over.replace(',' , '')),
                int(traded.replace(',' , '')),
                int(hold.replace(',' , '').replace('.','').replace('M','000000')),
                float(ratio.replace('%' , '')) 
            ))

    cnx = mysql.connector.connect(
            host =DB_URL,
            port =DB_PORT,
            user=DB_USERNAME,
            password=DB_PASSWORD
        )
    cur = cnx.cursor()
    
    sql = "Insert into `defaultdb`.`institutional_week` (`rank`, `name`, `code`, `price`, `change`, `buy`, `sell`, `over`, `traded`, `hold`, `ratio`) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

    cur.executemany(
        sql,
        table_rows
    )
    cnx.commit()

    cur.close()
    cnx.close()

    return ({"items":len(table_rows)})

if __name__ =="__main__":
    print(main())
