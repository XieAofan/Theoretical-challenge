from WebSpider import *

def main(ID):
    web = Web()
    #web.login('ttest', '954321')
    web.cookie = {'JSESSIONID': ID}
    web.get_roomid()
    t11 = time.time()
    web.get_roompage()
    testid = web.get_testid()
    html = web.get_review()
    qs = web.get_ans(html)
    i = 0
    ut = 1.5
    for q in qs:
        r = random.random()-.5
        time.sleep(relu(1.72-ut+r*0.8))
        t1 = time.time()
        i += 1
        print(i)
        
        web.submit_ans(q[2], q[3], q[1])
        t2 = time.time()
        ut = t2-t1
        if i == 10:
            t33 = time.time()
            if t33-t11 < 20:
                time.sleep(relu(20-(t33-t11)+0.1))
            else:
                time.sleep(0.1)
        web.get_result(i+1)
        #print()
    t22 = time.time()
    print(f'TimeUsed: {t22-t11}')
    web.log(f'TimeUsed: {t22-t11}')
    web.close()
    #print(web.get_result())

if __name__ == '__main__':
    main('4A3CCD8E61E9262DCE96C97AC8196D5D')