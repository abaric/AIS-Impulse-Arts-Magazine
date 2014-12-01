from gluon.tools import Auth, Crud
#from gluon.contrib.populate import populate

db=DAL('sqlite://storage.sqlite')
auth=Auth(db)
crud=Crud(db)

auth.define_tables()

db.define_table('image',
                Field('title'),
                Field('file','upload'),
                Field('author_id','reference auth_user'),
                Field('approved','boolean'),
                format='%(title)s')

db.define_table('image_comment',
   Field('image_id', 'reference image'),
   Field('author_id','reference auth_user'),
   Field('email'),
   Field('body', 'text'),
   Field('date_of_entry','datetime'),
   format='%(author_id)s')

db.image.title.requires = IS_NOT_IN_DB(db, db.image.title)
db.image_comment.image_id.requires = IS_IN_DB(db, db.image.id, '%(title)s')
db.image_comment.email.requires = IS_EMAIL()
db.image_comment.body.requires = IS_NOT_EMPTY()
db.image_comment.image_id.writable = db.image_comment.image_id.readable = False

db.define_table('writing',
   Field('title'),
   Field('body','text'),
   Field('author_id','reference auth_user'),
   Field('approved','boolean'),
   format = '%(title)s')

db.define_table('writing_comment',
   Field('writing_id', 'reference writing'),
   Field('author_id','reference auth_user'),
   Field('email'),
   Field('body', 'text'),
   Field('date_of_entry','datetime'),
   format='%(author_id)s')

db.writing.title.requires = IS_NOT_IN_DB(db, db.writing.title)
db.writing_comment.writing_id.requires = IS_IN_DB(db, db.writing.id, '%(title)s')
db.writing_comment.email.requires = IS_EMAIL()
db.writing_comment.body.requires = IS_NOT_EMPTY()
db.writing_comment.writing_id.writable = db.writing_comment.writing_id.readable = False

db.define_table('video',
   Field('title'),
   Field('url_str'),
   Field('author_id','reference auth_user'),
   Field('approved','boolean'),
   format='%(title)s')
   
db.define_table('video_comment',
   Field('video_id', 'reference video'),
   Field('author_id','reference auth_user'),
   Field('email'),
   Field('body', 'text'),
   Field('date_of_entry','datetime'),
   format='%(author_id)s')
   
db.video.title.requires = IS_NOT_IN_DB(db, db.video.title)
db.video_comment.video_id.requires = IS_IN_DB(db, db.video.id, '%(title)s')
#db.video_comment.author_id.requires = IS_IN_DB(db, db.auth_user.id, '%(author_id)s')
#db.video_comment.author_id.requires = IS_NOT_EMPTY()
db.video_comment.email.requires = IS_EMAIL()
db.video_comment.body.requires = IS_NOT_EMPTY()
db.video_comment.video_id.writable = db.video_comment.video_id.readable = False
