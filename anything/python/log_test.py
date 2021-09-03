import logging

logger = logging.getLogger(__name__)

logger.error("Api call is failed")

logger.error({
    'action': 'create',
    'state': 'fail',
    'message': 'Api call is failed'
})


logger.error({
    'action': 'create',
    'csv_file': csv_file,
    'force': force,
    'state': 'run',
})
# do something
logger.error({
    'action': 'create',
    'csv_file': csv_file,
    'force': force,
    'state': 'success',
})
