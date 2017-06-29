# -*-encoding:utf-8-*-
import api_invoice.config.profile as profile_config
import torndb

hostaddress = '127.0.0.1'
databasename = 'predict_img'
user = 'predict_img'
password = 'predict_img'

profile = profile_config.profile.get_profile()

if profile == profile_config.PROFILE_DEV:
    pass

if profile == profile_config.PROFILE_TEST:
    pass
if profile == profile_config.PROFILE_PRODUCT:

    pass


def get_db():
    db = torndb.Connection(hostaddress, databasename, user, password)
    return db






