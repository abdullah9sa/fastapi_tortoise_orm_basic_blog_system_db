from tortoise import Tortoise

async def init_tortoise(app):
    await Tortoise.init(
        db_url='sqlite://db.sqlite3',  # Change this to your database URL
        modules={'models': ['app.models.user', 'app.models.post']},  # List of model modules
    )
    await Tortoise.generate_schemas()
    
    app.state.db = Tortoise

async def close_tortoise(app):
    await app.state.db.close_connections()
    await app.state.db.close()

