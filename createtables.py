from models import *
from configuration import DbConfiguration

engine = DbConfiguration.getengine(
    *DbConfiguration.get_service_config('jwtserver'))
dbsession = DbConfiguration.newsession(engine)
ModelBase.metadata.create_all(engine)
print('Tables created.')
