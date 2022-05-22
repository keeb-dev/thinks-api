import logging
import datetime
from service.mongo import bubbles

logger = logging.getLogger(__name__)


def get_think_list():
    the_actual_list = []
    for thinks in bubbles.find():
        logger.debug("the thinks i got was %s" % thinks)
        logger.debug("deleting _id field")
        del thinks["_id"]
        logger.debug("resulting thinks is %s" % thinks)
        the_actual_list.append(thinks)
    return the_actual_list


def store_think(think):
    logger.debug("got think: %s " % think)
    logger.debug("building think record")
    post = {"text": think,
            "date": datetime.datetime.utcnow()}
    logger.debug("think record: ", post)
    bubbles.insert_one(post)


