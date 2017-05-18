'''
Created on Feb 25, 2017

@author: Gaurav BG
'''
from boto.mturk.connection import MTurkConnection

def cleanup():
    """Remove any boto test related HIT's"""
    
    ACCESS_ID ="DUMMY_FOR_GITHUB"
    SECRET_KEY = "DUMMY_FOR_GITHUB"
    HOST = 'mechanicalturk.sandbox.amazonaws.com'
    conn = MTurkConnection(aws_access_key_id=ACCESS_ID,
                      aws_secret_access_key=SECRET_KEY,
                      host=HOST)

    current_page = 1
    page_size = 10
    total_disabled = 0
    ignored = []

    while True:
        # reset the total for this loop
        disabled_count = 0

        # search all the hits in the sandbox
        search_rs = conn.search_hits(page_size=page_size, page_number=current_page)

        # success?
        if search_rs.status:
            for hit in search_rs:
                # delete any with Boto in the description
                if hit.Description.find('Tweets') != -1:
                    if hit.HITStatus != 'Reviewable':
                        disable_rs = conn.disable_hit(hit.HITId)
                        if disable_rs.status:
                            disabled_count += 1
                            # update the running total
                            total_disabled += 1
                        else:
                            print('Error when disabling')
                    else:
                        print('Disposing hit id:%s %s' %(hit.HITId, hit.Description))
                        dispose_rs = conn.dispose_hit(hit.HITId)
                        if dispose_rs.status:
                            disabled_count += 1
                            # update the running total
                            total_disabled += 1
                        else:
                            print('Error when disposing')

                else:
                    if hit.HITId not in ignored:
                        print('ignored:%s' %hit.HITId)
                        ignored.append(hit.HITId)

            # any more results?
            if int(search_rs.TotalNumResults) > current_page*page_size:
                # if we have disabled any HITs on this page
                # then we don't need to go to a new page
                # otherwise we do
                if not disabled_count:
                    current_page += 1
            else:
                # no, we're done
                break
        else:
            print('Error performing search, code:%s, message:%s' %(search_rs.Code, search_rs.Message))
            break

    total_ignored = len(ignored)
    print ('Processed: %d HITs, disabled/disposed: %d, ignored: %d' %(total_ignored + total_disabled, total_disabled, total_ignored))

if __name__ == '__main__':    
    cleanup()