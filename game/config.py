DOCS_ENABLED = True
ENV = "prod"

DB_CONFIG = {
    "USER": "sms_dev",
    "DBNAME": "smsdb",
    "PASSWORD": "sms@dev",
    "PORT": 5432,
    "HOST": "localhost"
}
if ENV=="local":
    DBURL = "postgres://"+DB_CONFIG["USER"]+":"+DB_CONFIG["PASSWORD"]+"@"+DB_CONFIG["HOST"]+":"+str(DB_CONFIG["PORT"])+"/"+DB_CONFIG["DBNAME"]
    MIGRATION_LOCATION = "./local_migrations"
    DEPLOYMENT_DETAILS = {
        "HOST": "localhost",
        "PORT": 8000
    }

if ENV=="prod":
    DBURL = "postgres://schooldb_kd4s_user:Ib8wfCVoCtMY5HNSlniT8W1jkgYUiKml@dpg-cefbki5a499e21q8d670-a.singapore-postgres.render.com/schooldb_kd4s"
    MIGRATION_LOCATION = "./prod_migrations"
    DEPLOYMENT_DETAILS = {
        "HOST": "0.0.0.0",
        "PORT": 10000
    }