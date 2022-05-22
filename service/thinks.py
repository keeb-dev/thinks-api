import logging
import datetime
from service.mongo import bubbles


def get_think_list():
    the_actual_list = []
    for thinks in bubbles.find():
        logging.debug("the thinks i got was", thinks)
        the_actual_list.append(thinks)
    return the_actual_list


def store_think(think):
    logging.debug("got think: %s " % think)
    logging.debug("building think record")
    post = {"text": think,
            "date": datetime.datetime.utcnow()}
    logging.debug("think record: ", post)
    bubbles.insert_one(post)


