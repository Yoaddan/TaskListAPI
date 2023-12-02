import logging as log

log.basicConfig(level=log.DEBUG,
                format='%(asctime)s: %(levelname)s \033[93m[%(filename)s:\033[91m%(lineno)s\033[0m\033[93m]\033[0m %(message)s',
                datefmt='%I:%M:%S %p',
                handlers = [
                    log.FileHandler('mongodb_api.log'),
                    log.StreamHandler()
                ])


if __name__ == '__main__':
    log.debug('Message level: DEBUG')
    log.info('Message level: INFO')
    log.warning('Message level: WARNING')
    log.error('Message level: ERROR')
    log.critical('Message level: CRITICAL')